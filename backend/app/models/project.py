import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False, default="Untitled Woodworking Project")
    description = Column(Text, nullable=True)
    product_type = Column(String(100), nullable=True) # bed, table, chair, shelf, workbench, etc.
    status = Column(String(50), default="draft") # draft, analyzing, analyzed, completed, failed
    reference_type = Column(String(50), default="image") # image, multi_image, pdf
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Project specifications
    overall_width = Column(Float, nullable=True)
    overall_depth = Column(Float, nullable=True)
    overall_height = Column(Float, nullable=True)
    dimension_unit = Column(String(10), default="inches")
    width_status = Column(String(50), default="ESTIMATED") # CONFIRMED, ESTIMATED, USER_PROVIDED, UNKNOWN
    depth_status = Column(String(50), default="ESTIMATED")
    height_status = Column(String(50), default="ESTIMATED")
    scale_anchor_desc = Column(String(255), nullable=True)
    scale_confidence = Column(String(20), default="MEDIUM") # HIGH, MEDIUM, LOW
    scale_warning = Column(Text, nullable=True)
    waste_percentage = Column(Float, default=15.0)
    difficulty_level = Column(String(50), default="Intermediate")
    estimated_build_time = Column(String(100), default="1-2 Days")
    primary_wood_species = Column(String(100), default="Pine / Softwood")

    # Relationships
    references = relationship("Reference", back_populates="project", cascade="all, delete-orphan")
    analysis = relationship("Analysis", back_populates="project", uselist=False, cascade="all, delete-orphan")
    components = relationship("Component", back_populates="project", cascade="all, delete-orphan")
    cut_list_items = relationship("CutListItem", back_populates="project", cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="project", cascade="all, delete-orphan")
    hardware = relationship("Hardware", back_populates="project", cascade="all, delete-orphan")
    instructions = relationship("Instruction", back_populates="project", cascade="all, delete-orphan")
    diagrams = relationship("Diagram", back_populates="project", cascade="all, delete-orphan")
    generated_files = relationship("GeneratedFile", back_populates="project", cascade="all, delete-orphan")

class Reference(Base):
    __tablename__ = "references"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    file_type = Column(String(20), nullable=False) # image/jpeg, image/png, application/pdf
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    file_url = Column(String(500), nullable=True)
    is_primary = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="references")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True)
    product_summary = Column(Text, nullable=True)
    construction_method = Column(Text, nullable=True)
    detected_features = Column(JSON, default=list) # panels, stretchers, slats, legs, etc.
    symmetry_notes = Column(Text, nullable=True)
    scale_inference_log = Column(Text, nullable=True)
    ai_provider = Column(String(50), nullable=True)
    raw_response = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="analysis")

class Component(Base):
    __tablename__ = "components"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    part_id = Column(String(20), nullable=False) # A, B, C1, etc.
    part_name = Column(String(255), nullable=False)
    material = Column(String(100), default="Pine")
    nominal_lumber_size = Column(String(50), default="1x4")
    finished_length = Column(Float, nullable=False)
    finished_width = Column(Float, nullable=False)
    finished_thickness = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    cut_type = Column(String(100), default="Crosscut") # Miter, Bevel, Rip, Crosscut
    angles = Column(String(100), default="90°")
    joinery = Column(String(255), default="Pocket holes")
    hardware = Column(String(255), nullable=True)
    purpose = Column(Text, nullable=True)
    confidence = Column(String(20), default="MEDIUM") # HIGH, MEDIUM, LOW

    project = relationship("Project", back_populates="components")

class CutListItem(Base):
    __tablename__ = "cut_lists"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    part_id = Column(String(20), nullable=False)
    part_name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=1)
    material = Column(String(100), default="Pine")
    lumber_size = Column(String(50), default="1x4")
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    thickness = Column(Float, nullable=False)
    angle = Column(String(50), default="0°")
    notes = Column(Text, nullable=True)
    confidence = Column(String(20), default="CONFIRMED") # CONFIRMED, ESTIMATED, INFERRED, USER_PROVIDED

    project = relationship("Project", back_populates="cut_list_items")

class Material(Base):
    __tablename__ = "materials"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(50), nullable=False) # 1x2, 1x4, 2x4, Plywood, etc.
    description = Column(String(255), nullable=False)
    standard_length = Column(Float, default=96.0) # 8ft standard board in inches
    required_board_length = Column(Float, nullable=False)
    waste_percentage = Column(Float, default=15.0)
    calculated_boards = Column(Integer, default=1)
    notes = Column(Text, nullable=True)

    project = relationship("Project", back_populates="materials")

class Hardware(Base):
    __tablename__ = "hardware"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(String(50), nullable=False) # e.g. "48", "1 box (50ct)", "1 bottle"
    status = Column(String(50), default="REFERENCE_VISIBLE") # REFERENCE_VISIBLE, REFERENCE_INFERRED, OPTIONAL
    purpose = Column(Text, nullable=True)
    size_spec = Column(String(100), nullable=True) # e.g. "1-1/4\" Coarse pocket screws"

    project = relationship("Project", back_populates="hardware")

class Instruction(Base):
    __tablename__ = "instructions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    objective = Column(Text, nullable=True)
    materials = Column(Text, nullable=True)
    parts_used = Column(String(255), nullable=True) # "A, B, C1"
    tools = Column(Text, nullable=True) # "Table saw, Drill, Clamps, Pocket-hole jig"
    cuts = Column(Text, nullable=True)
    assembly = Column(Text, nullable=True)
    fasteners = Column(Text, nullable=True)
    measurements = Column(Text, nullable=True)
    checkpoint = Column(Text, nullable=True)
    safety_note = Column(Text, nullable=True)

    project = relationship("Project", back_populates="instructions")

class Diagram(Base):
    __tablename__ = "diagrams"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    view_type = Column(String(50), nullable=False) # front, side, top, rear, exploded, component, joinery
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    svg_content = Column(Text, nullable=False)
    sort_order = Column(Integer, default=0)

    project = relationship("Project", back_populates="diagrams")

class GeneratedFile(Base):
    __tablename__ = "generated_files"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    file_type = Column(String(50), nullable=False) # pdf, export_json, highres_diagram
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="generated_files")
