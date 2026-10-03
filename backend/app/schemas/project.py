from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class ReferenceSchema(BaseModel):
    id: str
    project_id: str
    file_type: str
    file_name: str
    file_path: str
    file_size: int
    file_url: Optional[str] = None
    is_primary: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

class ComponentSchema(BaseModel):
    id: Optional[str] = None
    part_id: str
    part_name: str
    material: str = "Pine"
    nominal_lumber_size: str = "1x4"
    finished_length: float
    finished_width: float
    finished_thickness: float
    quantity: int = 1
    cut_type: str = "Crosscut"
    angles: str = "90°"
    joinery: str = "Pocket holes"
    hardware: Optional[str] = None
    purpose: Optional[str] = None
    confidence: str = "MEDIUM"

    class Config:
        from_attributes = True

class CutListItemSchema(BaseModel):
    id: Optional[str] = None
    part_id: str
    part_name: str
    quantity: int = 1
    material: str = "Pine"
    lumber_size: str = "1x4"
    length: float
    width: float
    thickness: float
    angle: str = "0°"
    notes: Optional[str] = None
    confidence: str = "CONFIRMED"

    class Config:
        from_attributes = True

class MaterialSchema(BaseModel):
    id: Optional[str] = None
    category: str # 1x4, 2x4, Plywood
    description: str
    standard_length: float = 96.0
    required_board_length: float
    waste_percentage: float = 15.0
    calculated_boards: int = 1
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class HardwareSchema(BaseModel):
    id: Optional[str] = None
    item_name: str
    quantity: str
    status: str = "REFERENCE_VISIBLE" # REFERENCE_VISIBLE, REFERENCE_INFERRED, OPTIONAL
    purpose: Optional[str] = None
    size_spec: Optional[str] = None

    class Config:
        from_attributes = True

class InstructionSchema(BaseModel):
    id: Optional[str] = None
    step_number: int
    title: str
    objective: Optional[str] = None
    materials: Optional[str] = None
    parts_used: Optional[str] = None
    tools: Optional[str] = None
    cuts: Optional[str] = None
    assembly: Optional[str] = None
    fasteners: Optional[str] = None
    measurements: Optional[str] = None
    checkpoint: Optional[str] = None
    safety_note: Optional[str] = None

    class Config:
        from_attributes = True

class DiagramSchema(BaseModel):
    id: Optional[str] = None
    view_type: str # front, side, top, rear, exploded, component, joinery
    title: str
    description: Optional[str] = None
    svg_content: str
    sort_order: int = 0

    class Config:
        from_attributes = True

class AnalysisSchema(BaseModel):
    id: Optional[str] = None
    product_summary: Optional[str] = None
    construction_method: Optional[str] = None
    detected_features: List[str] = []
    symmetry_notes: Optional[str] = None
    scale_inference_log: Optional[str] = None
    ai_provider: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str = "Untitled Woodworking Project"
    description: Optional[str] = None
    product_type: Optional[str] = None
    overall_width: Optional[float] = None
    overall_depth: Optional[float] = None
    overall_height: Optional[float] = None
    dimension_unit: str = "inches"
    width_status: str = "ESTIMATED"
    depth_status: str = "ESTIMATED"
    height_status: str = "ESTIMATED"
    scale_anchor_desc: Optional[str] = None
    scale_confidence: str = "MEDIUM"
    scale_warning: Optional[str] = "AI ESTIMATE — VERIFY BEFORE CUTTING"
    waste_percentage: float = 15.0
    difficulty_level: str = "Intermediate"
    estimated_build_time: str = "1-2 Days"
    primary_wood_species: str = "Pine / Softwood"

class ProjectCreate(BaseModel):
    name: Optional[str] = "New Woodworking Plan"
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    product_type: Optional[str] = None
    overall_width: Optional[float] = None
    overall_depth: Optional[float] = None
    overall_height: Optional[float] = None
    dimension_unit: Optional[str] = None
    width_status: Optional[str] = None
    depth_status: Optional[str] = None
    height_status: Optional[str] = None
    scale_anchor_desc: Optional[str] = None
    scale_confidence: Optional[str] = None
    waste_percentage: Optional[float] = None
    difficulty_level: Optional[str] = None
    estimated_build_time: Optional[str] = None
    primary_wood_species: Optional[str] = None
    components: Optional[List[ComponentSchema]] = None
    cut_list_items: Optional[List[CutListItemSchema]] = None
    materials: Optional[List[MaterialSchema]] = None
    hardware: Optional[List[HardwareSchema]] = None
    instructions: Optional[List[InstructionSchema]] = None

class ProjectResponse(ProjectBase):
    id: str
    status: str
    reference_type: str
    created_at: datetime
    updated_at: datetime
    references: List[ReferenceSchema] = []
    analysis: Optional[AnalysisSchema] = None
    components: List[ComponentSchema] = []
    cut_list_items: List[CutListItemSchema] = []
    materials: List[MaterialSchema] = []
    hardware: List[HardwareSchema] = []
    instructions: List[InstructionSchema] = []
    diagrams: List[DiagramSchema] = []

    class Config:
        from_attributes = True

class ScaleAnchorRequest(BaseModel):
    anchor_type: str # mattress_twin, mattress_full, mattress_queen, sheet_plywood, 2x4_stud, custom
    anchor_dimension_value: float # dimension in inches
    anchor_axis: str # width, depth, height
    description: Optional[str] = None

class ReanalyzeRequest(BaseModel):
    scale_anchor: Optional[ScaleAnchorRequest] = None
    custom_width: Optional[float] = None
    custom_depth: Optional[float] = None
    custom_height: Optional[float] = None
    material_thickness: Optional[float] = None
    wood_species: Optional[str] = None
    waste_percentage: Optional[float] = None
    additional_notes: Optional[str] = None
