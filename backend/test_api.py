import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from app.services.diagrams.blueprint_generator import blueprint_generator
from app.services.pdf.pdf_generator import pdf_generator
from app.services.ai.fallback_analyzer import WoodworkingKnowledgeEngine

client = TestClient(app)

class TestWoodPlanAPI(unittest.TestCase):
    def test_01_health_and_root(self):
        res = client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["service"], "WOODPLAN AI API")

        res_health = client.get("/health")
        self.assertEqual(res_health.status_code, 200)

    def test_02_projects_list_and_seed(self):
        res = client.get("/api/projects")
        self.assertEqual(res.status_code, 200)
        projects = res.json()
        self.assertGreater(len(projects), 0, "Projects should exist in database")
        
        # Find house bed project or any analyzed project
        demo = next((p for p in projects if "Twin House Bed" in p.get("name", "")), projects[0])
        self.assertTrue(len(demo["name"]) > 0)
        self.assertIn(demo["status"], ["analyzed", "draft"])

    def test_03_create_and_delete_project(self):
        create_res = client.post("/api/projects", json={
            "name": "Test Modern Dining Table",
            "description": "Test build with oak and breadboard ends"
        })
        self.assertEqual(create_res.status_code, 200)
        proj = create_res.json()
        proj_id = proj["id"]
        self.assertEqual(proj["name"], "Test Modern Dining Table")

        # Fetch it
        get_res = client.get(f"/api/projects/{proj_id}")
        self.assertEqual(get_res.status_code, 200)

        # Delete it
        del_res = client.delete(f"/api/projects/{proj_id}")
        self.assertEqual(del_res.status_code, 200)

    def test_04_blueprint_generator_multiviews(self):
        views = blueprint_generator.generate_all_diagrams(
            product_name="Test Workbench",
            width_in=60.0,
            height_in=36.0,
            depth_in=30.0,
            components=[
                {"part_id": "A", "part_name": "Legs", "nominal_lumber_size": "4x4", "quantity": 4}
            ]
        )
        self.assertEqual(len(views), 5)
        view_types = [v["view_type"] for v in views]
        self.assertIn("front", view_types)
        self.assertIn("side", view_types)
        self.assertIn("top", view_types)
        self.assertIn("exploded", view_types)
        self.assertIn("joinery", view_types)
        for v in views:
            self.assertTrue(v["svg_content"].startswith("<svg"))
            self.assertTrue(v["svg_content"].endswith("</svg>"))
            self.assertIn("TIMBER SHOP BY FAISAL", v["svg_content"])

    def test_05_strict_bw_pdf_generator(self):
        test_plan = WoodworkingKnowledgeEngine.generate_plan(
            product_name="DIY Kids House Bed — Twin Size",
            category="house_bed",
            scale_anchor={"anchor_type": "mattress_twin", "anchor_dimension_value": 75.0, "anchor_axis": "width"},
            custom_dims={"custom_width": 79.5, "custom_depth": 42.0, "custom_height": 72.0},
            waste_pct=15.0
        )
        test_pdf_path = os.path.join("storage", "pdfs", "test_bw_blueprint_plan.pdf")
        os.makedirs(os.path.dirname(test_pdf_path), exist_ok=True)
        pdf_generator.generate_plan_pdf(test_plan, test_pdf_path)
        self.assertTrue(os.path.exists(test_pdf_path))
        self.assertGreater(os.path.getsize(test_pdf_path), 8000, "PDF should be generated with rich content")

if __name__ == "__main__":
    unittest.main()
