import os
import json
import base64
import httpx
from typing import Dict, Any, List, Optional
from app.config import settings

class GeminiProvider:
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.model = settings.VISION_MODEL or "gemini-1.5-flash"

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    async def analyze_multimodal(
        self,
        image_paths: List[str],
        pdf_texts: List[str],
        product_name: str,
        scale_anchor: Optional[Dict[str, Any]] = None,
        custom_notes: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        if not self.is_configured():
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        prompt = """You are an expert master carpenter and structural woodworking engineer for WOODPLAN AI.
Analyze the provided reference woodworking image(s) or plans.
Extract and calculate the exact structural components, nominal lumber sizing, finished dimensions in inches, cut list, materials list with 15% waste allowance, hardware classifications, joinery details, and step-by-step build instructions.

CRITICAL INSTRUCTIONS:
- Do NOT invent exact dimensions if not confirmed by visual scale.
- Classify dimension status as: "CONFIRMED", "ESTIMATED", "INFERRED", or "USER_PROVIDED".
- Provide confidence level: "HIGH", "MEDIUM", or "LOW".
- Return ONLY valid JSON with no markdown wrapping or preamble, matching this exact structure:
{
  "product_type": "string",
  "overall_width": 72.0,
  "overall_depth": 36.0,
  "overall_height": 48.0,
  "width_status": "ESTIMATED",
  "depth_status": "ESTIMATED",
  "height_status": "ESTIMATED",
  "scale_confidence": "MEDIUM",
  "scale_warning": "AI ESTIMATE — VERIFY BEFORE CUTTING",
  "difficulty_level": "Intermediate",
  "estimated_build_time": "1-2 Days",
  "primary_wood_species": "Pine / Softwood",
  "product_summary": "Description of the woodworking product",
  "construction_method": "Pocket hole and face clamp joinery",
  "detected_features": ["Side Panels", "Corner Legs", "Support Rails", "Slats"],
  "symmetry_notes": "Symmetrical across center",
  "components": [
    {
      "part_id": "A",
      "part_name": "Corner Leg Posts",
      "material": "Pine",
      "nominal_lumber_size": "2x4",
      "finished_length": 48.0,
      "finished_width": 3.5,
      "finished_thickness": 1.5,
      "quantity": 4,
      "cut_type": "Crosscut",
      "angles": "90°",
      "joinery": "Pocket holes",
      "hardware": "2-1/2\" pocket screws",
      "purpose": "Primary uprights",
      "confidence": "HIGH"
    }
  ],
  "hardware": [
    {
      "item_name": "Pocket Screws",
      "quantity": "1 box (100ct)",
      "status": "REFERENCE_VISIBLE",
      "purpose": "Joining frames",
      "size_spec": "1-1/4\" Coarse"
    }
  ],
  "instructions": [
    {
      "step_number": 1,
      "title": "Frame Assembly",
      "objective": "Assemble outer frames",
      "parts_used": "Part A",
      "tools": "Miter saw, Drill, Clamps",
      "cuts": "Cut 4 legs to 48 inches",
      "assembly": "Glue and clamp",
      "fasteners": "2-1/2\" screws",
      "measurements": "Square diagonals",
      "checkpoint": "Check for 90-degree square",
      "safety_note": "Wear eye protection"
    }
  ]
}
"""
        parts = [{"text": prompt}]

        if scale_anchor:
            parts.append({"text": f"USER SCALE ANCHOR: {json.dumps(scale_anchor)}"})
        if custom_notes:
            parts.append({"text": f"USER NOTES: {custom_notes}"})
        if pdf_texts:
            parts.append({"text": f"EXTRACTED PDF SOURCE CONTENT:\n{' '.join(pdf_texts)[:4000]}"})

        for img_path in image_paths:
            if os.path.exists(img_path):
                try:
                    with open(img_path, "rb") as f:
                        data = base64.b64encode(f.read()).decode("utf-8")
                    mime = "image/jpeg"
                    if img_path.lower().endswith(".png"):
                        mime = "image/png"
                    elif img_path.lower().endswith(".webp"):
                        mime = "image/webp"
                    parts.append({
                        "inline_data": {
                            "mime_type": mime,
                            "data": data
                        }
                    })
                except Exception:
                    pass

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(url, json={"contents": [{"parts": parts}]})
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text_resp = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        clean_json = text_resp.strip()
                        if clean_json.startswith("```json"):
                            clean_json = clean_json[7:]
                        if clean_json.startswith("```"):
                            clean_json = clean_json[3:]
                        if clean_json.endswith("```"):
                            clean_json = clean_json[:-3]
                        return json.loads(clean_json.strip())
        except Exception:
            pass

        return None

gemini_provider = GeminiProvider()
