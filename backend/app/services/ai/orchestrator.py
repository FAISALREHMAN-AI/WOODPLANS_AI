import os
import math
from typing import Dict, Any, List, Optional
from app.services.ai.gemini_provider import gemini_provider
from app.services.ai.fallback_analyzer import WoodworkingKnowledgeEngine
from app.services.pdf.pdf_extractor import pdf_extractor
from app.services.diagrams.blueprint_generator import blueprint_generator
from app.services.pdf.pdf_generator import pdf_generator
from app.services.storage.storage_service import storage_service

class WoodworkingAIOrchestrator:
    """
    Coordinates multi-modal vision decomposition, scale anchoring,
    cut-list derivation, lumber optimization, and automated blueprint drafting.
    """

    async def analyze_project(
        self,
        project_id: str,
        project_name: str,
        references: List[Dict[str, Any]],
        scale_anchor: Optional[Dict[str, Any]] = None,
        custom_dims: Optional[Dict[str, Any]] = None,
        waste_percentage: float = 15.0,
        progress_callback=None
    ) -> Dict[str, Any]:
        
        async def update_progress(step: str, percentage: int):
            if progress_callback:
                await progress_callback(step, percentage)

        # Stage 1: Inspect references
        await update_progress("Detecting Product & Materials", 15)
        
        img_paths = []
        pdf_texts = []
        ref_names = []

        for ref in references:
            fpath = ref.get("file_path", "")
            ftype = ref.get("file_type", "")
            fname = ref.get("file_name", "")
            ref_names.append(fname)

            if "pdf" in ftype.lower() or fpath.lower().endswith(".pdf"):
                extracted = pdf_extractor.extract_pdf_data(fpath)
                pdf_texts.append(extracted.get("full_text", ""))
            else:
                img_paths.append(fpath)

        # Stage 2: Category Detection & Vision Analysis
        await update_progress("Analyzing Components & Geometry", 35)
        
        detected_category = WoodworkingKnowledgeEngine.detect_category(
            " ".join(ref_names),
            " ".join(pdf_texts)
        )

        # Try Gemini if active
        gemini_result = None
        if gemini_provider.is_configured():
            try:
                gemini_result = await gemini_provider.analyze_multimodal(
                    image_paths=img_paths,
                    pdf_texts=pdf_texts,
                    product_name=project_name,
                    scale_anchor=scale_anchor,
                    custom_notes=f"Woodworking category: {detected_category}"
                )
            except Exception:
                gemini_result = None

        await update_progress("Estimating Dimensions & Scale Anchor", 55)

        # If Gemini returned valid structure, integrate it; otherwise use the KnowledgeEngine
        if gemini_result and gemini_result.get("components"):
            plan_data = gemini_result
            # Add lumber calculations with waste %
            cls_cut_list = []
            for comp in plan_data.get("components", []):
                cls_cut_list.append({
                    "part_id": comp["part_id"],
                    "part_name": comp["part_name"],
                    "quantity": comp.get("quantity", 1),
                    "material": comp.get("material", "Pine"),
                    "lumber_size": comp.get("nominal_lumber_size", "1x4"),
                    "length": float(comp.get("finished_length", 36.0)),
                    "width": float(comp.get("finished_width", 3.5)),
                    "thickness": float(comp.get("finished_thickness", 0.75)),
                    "angle": comp.get("angles", "90°"),
                    "notes": f"Joinery: {comp.get('joinery', 'Pocket holes')}",
                    "confidence": comp.get("confidence", "CONFIRMED")
                })
            plan_data["cut_list_items"] = cls_cut_list
            plan_data["waste_percentage"] = waste_percentage
            
            # Group materials
            board_groups = {}
            for c in cls_cut_list:
                size = c["lumber_size"]
                tot_len = c["length"] * c["quantity"]
                board_groups[size] = board_groups.get(size, 0.0) + tot_len
            
            materials = []
            for size, total_in in board_groups.items():
                req_with_waste = total_in * (1.0 + (waste_percentage / 100.0))
                num_boards = math.ceil(req_with_waste / 96.0)
                materials.append({
                    "category": size,
                    "description": f"{size} Kiln-Dried Select Stock (8-ft boards)",
                    "standard_length": 96.0,
                    "required_board_length": round(req_with_waste, 1),
                    "waste_percentage": waste_percentage,
                    "calculated_boards": num_boards,
                    "notes": f"Yields cuts with {waste_percentage}% waste allowance"
                })
            plan_data["materials"] = materials
        else:
            plan_data = WoodworkingKnowledgeEngine.generate_plan(
                product_name=project_name,
                category=detected_category,
                scale_anchor=scale_anchor,
                custom_dims=custom_dims,
                waste_pct=waste_percentage
            )

        # Stage 3: Building Cut List & Instructions
        await update_progress("Building Cut List & Joinery Sequence", 75)

        # Stage 4: Creating Technical Diagrams
        await update_progress("Creating Technical Blueprint Diagrams", 88)
        
        w = float(plan_data.get("overall_width", 60.0))
        h = float(plan_data.get("overall_height", 48.0))
        d = float(plan_data.get("overall_depth", 36.0))
        name = plan_data.get("product_type") or project_name

        diagrams = blueprint_generator.generate_all_diagrams(
            product_name=name,
            width_in=w,
            height_in=h,
            depth_in=d,
            components=plan_data.get("components", [])
        )
        plan_data["diagrams"] = diagrams

        # Stage 5: Preparing PDF
        await update_progress("Generating Printable Woodworking Plan PDF", 96)
        
        pdf_path = storage_service.get_pdf_path(project_id)
        try:
            pdf_generator.generate_plan_pdf(plan_data, pdf_path)
            plan_data["pdf_path"] = pdf_path
        except Exception as e:
            print(f"Error generating PDF: {e}")

        await update_progress("Plan Complete", 100)
        return plan_data

orchestrator = WoodworkingAIOrchestrator()
