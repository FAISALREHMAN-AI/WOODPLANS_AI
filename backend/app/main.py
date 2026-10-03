import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.models.project import Project
from app.api.projects import router as projects_router
from app.services.ai.fallback_analyzer import WoodworkingKnowledgeEngine
from app.services.diagrams.blueprint_generator import blueprint_generator
from app.models.project import Component, CutListItem, Material, Hardware, Instruction, Diagram, Analysis

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="WOODPLAN AI — Woodworking Product Analyzer & DIY Plan Generator",
    version="1.0.0"
)

# CORS Configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://localhost:3000",
    "https://*.vercel.app",
    "https://*.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all during dev/demo, production restricts via FRONTEND_URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file routes for uploads, diagrams, and PDFs
app.mount("/api/files/uploads", StaticFiles(directory=os.path.join(settings.STORAGE_DIR, "uploads")), name="uploads")
app.mount("/api/files/diagrams", StaticFiles(directory=os.path.join(settings.STORAGE_DIR, "diagrams")), name="diagrams")

# Include Routers
app.include_router(projects_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "service": "WOODPLAN AI API",
        "tagline": "From Reference to Ready-to-Build",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "storage": os.path.exists(settings.STORAGE_DIR),
        "ai_provider": settings.AI_PROVIDER
    }

def seed_demo_project_if_empty():
    db = SessionLocal()
    try:
        count = db.query(Project).count()
        if count == 0:
            print("Seeding demo woodworking project: Twin House Bed...")
            demo_plan = WoodworkingKnowledgeEngine.generate_plan(
                product_name="Montessori Twin House Bed",
                category="house_bed",
                scale_anchor={"anchor_type": "mattress_twin", "anchor_dimension_value": 75.0, "anchor_axis": "width", "description": "Twin Mattress Anchor 38x75\""},
                custom_dims={"custom_width": 79.5, "custom_depth": 42.0, "custom_height": 72.0},
                waste_pct=15.0
            )

            p = Project(
                name="Montessori Twin House Bed",
                description="Modern Scandinavian-style floor bed with pitched gable roof framing. Built using 2x6 base rails, 2x4 uprights, and 1x4 infill pickets with pocket-hole joinery.",
                product_type="Twin House Bed",
                status="analyzed",
                reference_type="image",
                overall_width=79.5,
                overall_depth=42.0,
                overall_height=72.0,
                width_status="USER_PROVIDED",
                depth_status="USER_PROVIDED",
                height_status="ESTIMATED",
                scale_anchor_desc="Standard Twin Mattress (38\" × 75\")",
                scale_confidence="HIGH",
                scale_warning="ANCHORED TO STANDARD TWIN MATTRESS (38\" × 75\")",
                waste_percentage=15.0,
                difficulty_level="Intermediate",
                estimated_build_time="2-3 Days",
                primary_wood_species="Select Pine / Douglas Fir"
            )
            db.add(p)
            db.flush()

            # Add analysis
            an = demo_plan.get("analysis", {})
            db.add(Analysis(
                project_id=p.id,
                product_summary=an.get("product_summary"),
                construction_method=an.get("construction_method"),
                detected_features=an.get("detected_features", []),
                symmetry_notes=an.get("symmetry_notes"),
                scale_inference_log=an.get("scale_inference_log"),
                ai_provider="WOODPLAN AI Structural Vision Engine"
            ))

            for comp in demo_plan.get("components", []):
                db.add(Component(project_id=p.id, **comp))

            for cl in demo_plan.get("cut_list_items", []):
                db.add(CutListItem(project_id=p.id, **cl))

            for m in demo_plan.get("materials", []):
                db.add(Material(project_id=p.id, **m))

            for h in demo_plan.get("hardware", []):
                db.add(Hardware(project_id=p.id, **h))

            for inst in demo_plan.get("instructions", []):
                db.add(Instruction(project_id=p.id, **inst))

            diagrams = blueprint_generator.generate_all_diagrams(
                product_name="Montessori Twin House Bed",
                width_in=79.5,
                height_in=72.0,
                depth_in=42.0,
                components=demo_plan.get("components", [])
            )
            for d in diagrams:
                db.add(Diagram(project_id=p.id, **d))

            db.commit()
            print("Demo project seeded successfully.")
    except Exception as e:
        print(f"Error seeding demo project: {e}")
        db.rollback()
    finally:
        db.close()

seed_demo_project_if_empty()
