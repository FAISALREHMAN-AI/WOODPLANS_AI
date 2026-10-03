import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import (
    Project, Reference, Analysis, Component, CutListItem, Material, Hardware, Instruction, Diagram, GeneratedFile
)
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, ReanalyzeRequest
)
from app.services.storage.storage_service import storage_service
from app.services.ai.orchestrator import orchestrator
from app.services.pdf.pdf_generator import pdf_generator
from app.services.diagrams.blueprint_generator import blueprint_generator

router = APIRouter(prefix="/projects", tags=["projects"])

# In-memory progress tracker for live progress bar
PROJECT_PROGRESS = {}

@router.post("", response_model=ProjectResponse)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(
        name=payload.name or "New Woodworking Plan",
        description=payload.description or "",
        status="draft"
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}")
def delete_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully", "id": project_id}

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, payload: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = payload.model_dump(exclude_unset=True)
    
    # Simple scalar field update
    scalar_fields = [
        "name", "description", "product_type", "overall_width", "overall_depth", "overall_height",
        "dimension_unit", "width_status", "depth_status", "height_status", "scale_anchor_desc",
        "scale_confidence", "waste_percentage", "difficulty_level", "estimated_build_time", "primary_wood_species"
    ]
    for field in scalar_fields:
        if field in update_data:
            setattr(project, field, update_data[field])

    # If components / cut list updated, replace items
    if "components" in update_data and update_data["components"] is not None:
        db.query(Component).filter(Component.project_id == project_id).delete()
        for c in update_data["components"]:
            db.add(Component(project_id=project_id, **c))

    if "cut_list_items" in update_data and update_data["cut_list_items"] is not None:
        db.query(CutListItem).filter(CutListItem.project_id == project_id).delete()
        for item in update_data["cut_list_items"]:
            db.add(CutListItem(project_id=project_id, **item))

    if "materials" in update_data and update_data["materials"] is not None:
        db.query(Material).filter(Material.project_id == project_id).delete()
        for m in update_data["materials"]:
            db.add(Material(project_id=project_id, **m))

    if "hardware" in update_data and update_data["hardware"] is not None:
        db.query(Hardware).filter(Hardware.project_id == project_id).delete()
        for h in update_data["hardware"]:
            db.add(Hardware(project_id=project_id, **h))

    if "instructions" in update_data and update_data["instructions"] is not None:
        db.query(Instruction).filter(Instruction.project_id == project_id).delete()
        for inst in update_data["instructions"]:
            db.add(Instruction(project_id=project_id, **inst))

    # Regenerate diagrams to match updated dimensions
    if project.overall_width and project.overall_height:
        db.query(Diagram).filter(Diagram.project_id == project_id).delete()
        new_diagrams = blueprint_generator.generate_all_diagrams(
            product_name=project.name,
            width_in=project.overall_width,
            height_in=project.overall_height,
            depth_in=project.overall_depth or 36.0,
            components=[c.__dict__ for c in project.components]
        )
        for d in new_diagrams:
            db.add(Diagram(project_id=project_id, **d))

    db.commit()
    db.refresh(project)
    return project

@router.post("/{project_id}/upload")
async def upload_reference(
    project_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    saved_info = await storage_service.save_upload(file, project_id)

    # Check if this is the first reference
    is_first = db.query(Reference).filter(Reference.project_id == project_id).count() == 0
    ref_type = "pdf" if "pdf" in saved_info["file_type"] else "image"
    
    reference = Reference(
        project_id=project_id,
        file_type=saved_info["file_type"],
        file_name=saved_info["file_name"],
        file_path=saved_info["file_path"],
        file_size=saved_info["file_size"],
        file_url=saved_info["url"],
        is_primary=is_first
    )
    db.add(reference)
    
    # Auto-update project name from filename if default
    if project.name in ["New Woodworking Plan", "Untitled Woodworking Project"]:
        base_name = os.path.splitext(saved_info["file_name"])[0].replace("-", " ").replace("_", " ").title()
        project.name = base_name

    project.reference_type = ref_type
    db.commit()
    db.refresh(reference)
    
    return {
        "message": "Reference uploaded successfully",
        "reference": {
            "id": reference.id,
            "file_name": reference.file_name,
            "file_type": reference.file_type,
            "file_url": reference.file_url,
            "file_size": reference.file_size
        }
    }

@router.delete("/{project_id}/references/{ref_id}")
def delete_reference(project_id: str, ref_id: str, db: Session = Depends(get_db)):
    ref = db.query(Reference).filter(Reference.id == ref_id, Reference.project_id == project_id).first()
    if not ref:
        raise HTTPException(status_code=404, detail="Reference not found")
    
    if os.path.exists(ref.file_path):
        try:
            os.remove(ref.file_path)
        except Exception:
            pass

    db.delete(ref)
    db.commit()
    return {"message": "Reference removed"}

@router.get("/{project_id}/progress")
def get_analysis_progress(project_id: str):
    prog = PROJECT_PROGRESS.get(project_id, {"step": "Idle", "percentage": 0})
    return prog

@router.post("/{project_id}/analyze")
async def analyze_project(
    project_id: str,
    background_tasks: BackgroundTasks,
    scale_anchor_type: Optional[str] = Form(None),
    scale_anchor_value: Optional[float] = Form(None),
    scale_anchor_axis: Optional[str] = Form("width"),
    custom_width: Optional[float] = Form(None),
    custom_depth: Optional[float] = Form(None),
    custom_height: Optional[float] = Form(None),
    waste_percentage: Optional[float] = Form(15.0),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    references = db.query(Reference).filter(Reference.project_id == project_id).all()
    if not references:
        raise HTTPException(status_code=400, detail="Please upload at least one image or PDF reference before analysis.")

    scale_anchor = None
    if scale_anchor_type:
        scale_anchor = {
            "anchor_type": scale_anchor_type,
            "anchor_dimension_value": scale_anchor_value or 0.0,
            "anchor_axis": scale_anchor_axis or "width"
        }

    custom_dims = None
    if custom_width or custom_depth or custom_height:
        custom_dims = {
            "custom_width": custom_width,
            "custom_depth": custom_depth,
            "custom_height": custom_height
        }

    ref_payload = [
        {"file_path": r.file_path, "file_type": r.file_type, "file_name": r.file_name}
        for r in references
    ]

    project.status = "analyzing"
    db.commit()

    async def progress_hook(step: str, percentage: int):
        PROJECT_PROGRESS[project_id] = {"step": step, "percentage": percentage}

    # Execute analysis
    plan = await orchestrator.analyze_project(
        project_id=project_id,
        project_name=project.name,
        references=ref_payload,
        scale_anchor=scale_anchor,
        custom_dims=custom_dims,
        waste_percentage=waste_percentage or 15.0,
        progress_callback=progress_hook
    )

    # Persist results in DB
    project.product_type = plan.get("product_type")
    project.overall_width = plan.get("overall_width")
    project.overall_depth = plan.get("overall_depth")
    project.overall_height = plan.get("overall_height")
    project.width_status = plan.get("width_status", "ESTIMATED")
    project.depth_status = plan.get("depth_status", "ESTIMATED")
    project.height_status = plan.get("height_status", "ESTIMATED")
    project.scale_anchor_desc = plan.get("scale_anchor_desc")
    project.scale_confidence = plan.get("scale_confidence", "MEDIUM")
    project.scale_warning = plan.get("scale_warning")
    project.difficulty_level = plan.get("difficulty_level", "Intermediate")
    project.estimated_build_time = plan.get("estimated_build_time", "1-2 Days")
    project.primary_wood_species = plan.get("primary_wood_species", "Pine / Softwood")
    project.waste_percentage = plan.get("waste_percentage", 15.0)
    project.status = "analyzed"

    # Analysis record
    db.query(Analysis).filter(Analysis.project_id == project_id).delete()
    an_data = plan.get("analysis", {})
    analysis_record = Analysis(
        project_id=project_id,
        product_summary=an_data.get("product_summary"),
        construction_method=an_data.get("construction_method"),
        detected_features=an_data.get("detected_features", []),
        symmetry_notes=an_data.get("symmetry_notes"),
        scale_inference_log=an_data.get("scale_inference_log"),
        ai_provider=an_data.get("ai_provider")
    )
    db.add(analysis_record)

    # Components
    db.query(Component).filter(Component.project_id == project_id).delete()
    for c in plan.get("components", []):
        db.add(Component(project_id=project_id, **c))

    # Cut list items
    db.query(CutListItem).filter(CutListItem.project_id == project_id).delete()
    for item in plan.get("cut_list_items", []):
        db.add(CutListItem(project_id=project_id, **item))

    # Materials
    db.query(Material).filter(Material.project_id == project_id).delete()
    for m in plan.get("materials", []):
        db.add(Material(project_id=project_id, **m))

    # Hardware
    db.query(Hardware).filter(Hardware.project_id == project_id).delete()
    for h in plan.get("hardware", []):
        db.add(Hardware(project_id=project_id, **h))

    # Instructions
    db.query(Instruction).filter(Instruction.project_id == project_id).delete()
    for inst in plan.get("instructions", []):
        db.add(Instruction(project_id=project_id, **inst))

    # Diagrams
    db.query(Diagram).filter(Diagram.project_id == project_id).delete()
    for d in plan.get("diagrams", []):
        db.add(Diagram(project_id=project_id, **d))

    db.commit()
    db.refresh(project)

    PROJECT_PROGRESS[project_id] = {"step": "Complete", "percentage": 100}

    return {"message": "Project analyzed successfully", "project_id": project_id}

@router.post("/{project_id}/reanalyze")
async def reanalyze_project(
    project_id: str,
    payload: ReanalyzeRequest,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    references = db.query(Reference).filter(Reference.project_id == project_id).all()
    ref_payload = [
        {"file_path": r.file_path, "file_type": r.file_type, "file_name": r.file_name}
        for r in references
    ]

    scale_anchor = payload.scale_anchor.model_dump() if payload.scale_anchor else None
    custom_dims = {
        "custom_width": payload.custom_width,
        "custom_depth": payload.custom_depth,
        "custom_height": payload.custom_height
    }

    plan = await orchestrator.analyze_project(
        project_id=project_id,
        project_name=project.name,
        references=ref_payload,
        scale_anchor=scale_anchor,
        custom_dims=custom_dims,
        waste_percentage=payload.waste_percentage or project.waste_percentage or 15.0
    )

    # Save to db
    project.overall_width = plan.get("overall_width")
    project.overall_depth = plan.get("overall_depth")
    project.overall_height = plan.get("overall_height")
    project.width_status = plan.get("width_status")
    project.depth_status = plan.get("depth_status")
    project.height_status = plan.get("height_status")
    project.waste_percentage = plan.get("waste_percentage")
    project.scale_confidence = plan.get("scale_confidence")
    project.scale_warning = plan.get("scale_warning")
    if payload.wood_species:
        project.primary_wood_species = payload.wood_species

    # Update cut list, materials, diagrams
    db.query(Component).filter(Component.project_id == project_id).delete()
    for c in plan.get("components", []):
        db.add(Component(project_id=project_id, **c))

    db.query(CutListItem).filter(CutListItem.project_id == project_id).delete()
    for item in plan.get("cut_list_items", []):
        db.add(CutListItem(project_id=project_id, **item))

    db.query(Material).filter(Material.project_id == project_id).delete()
    for m in plan.get("materials", []):
        db.add(Material(project_id=project_id, **m))

    db.query(Diagram).filter(Diagram.project_id == project_id).delete()
    for d in plan.get("diagrams", []):
        db.add(Diagram(project_id=project_id, **d))

    db.commit()
    db.refresh(project)
    return project

@router.post("/{project_id}/generate-pdf")
def generate_project_pdf(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    pdf_path = storage_service.get_pdf_path(project_id)
    
    # Serialize project
    proj_dict = {
        "name": project.name,
        "description": project.description,
        "product_type": project.product_type,
        "overall_width": project.overall_width,
        "overall_depth": project.overall_depth,
        "overall_height": project.overall_height,
        "width_status": project.width_status,
        "depth_status": project.depth_status,
        "height_status": project.height_status,
        "waste_percentage": project.waste_percentage,
        "difficulty_level": project.difficulty_level,
        "estimated_build_time": project.estimated_build_time,
        "primary_wood_species": project.primary_wood_species,
        "analysis": {
            "product_summary": project.analysis.product_summary if project.analysis else "",
            "construction_method": project.analysis.construction_method if project.analysis else ""
        },
        "components": [c.__dict__ for c in project.components],
        "cut_list_items": [i.__dict__ for i in project.cut_list_items],
        "materials": [m.__dict__ for m in project.materials],
        "hardware": [h.__dict__ for h in project.hardware],
        "instructions": [inst.__dict__ for inst in project.instructions]
    }

    pdf_generator.generate_plan_pdf(proj_dict, pdf_path)
    return {"message": "PDF generated successfully", "pdf_url": f"/api/projects/{project_id}/pdf"}

@router.get("/{project_id}/pdf")
def download_project_pdf(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    pdf_path = storage_service.get_pdf_path(project_id)
    if not os.path.exists(pdf_path):
        # Auto-generate if missing
        generate_project_pdf(project_id, db)

    clean_filename = f"{project.name.replace(' ', '_')}_woodplan.pdf"
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=clean_filename
    )
