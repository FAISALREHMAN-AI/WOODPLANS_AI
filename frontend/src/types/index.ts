export type DimensionStatus = 'CONFIRMED' | 'ESTIMATED' | 'INFERRED' | 'USER_PROVIDED' | 'UNKNOWN';
export type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW';
export type HardwareStatus = 'REFERENCE_VISIBLE' | 'REFERENCE_INFERRED' | 'OPTIONAL';

export interface ReferenceItem {
  id: string;
  project_id: string;
  file_type: string;
  file_name: string;
  file_path: string;
  file_size: number;
  file_url?: string;
  is_primary: boolean;
  created_at: string;
}

export interface ComponentItem {
  id?: string;
  part_id: string;
  part_name: string;
  material: string;
  nominal_lumber_size: string;
  finished_length: number;
  finished_width: number;
  finished_thickness: number;
  quantity: number;
  cut_type: string;
  angles: string;
  joinery: string;
  hardware?: string;
  purpose?: string;
  confidence: ConfidenceLevel;
}

export interface CutListItem {
  id?: string;
  part_id: string;
  part_name: string;
  quantity: number;
  material: string;
  lumber_size: string;
  length: number;
  width: number;
  thickness: number;
  angle: string;
  notes?: string;
  confidence: DimensionStatus;
}

export interface MaterialItem {
  id?: string;
  category: string;
  description: string;
  standard_length: number;
  required_board_length: number;
  waste_percentage: number;
  calculated_boards: number;
  notes?: string;
}

export interface HardwareItem {
  id?: string;
  item_name: string;
  quantity: string;
  status: HardwareStatus;
  purpose?: string;
  size_spec?: string;
}

export interface InstructionStep {
  id?: string;
  step_number: number;
  title: string;
  objective?: string;
  materials?: string;
  parts_used?: string;
  tools?: string;
  cuts?: string;
  assembly?: string;
  fasteners?: string;
  measurements?: string;
  checkpoint?: string;
  safety_note?: string;
}

export interface DiagramItem {
  id?: string;
  view_type: 'front' | 'side' | 'top' | 'rear' | 'exploded' | 'component' | 'joinery';
  title: string;
  description?: string;
  svg_content: string;
  sort_order: number;
}

export interface AnalysisData {
  id?: string;
  product_summary?: string;
  construction_method?: string;
  detected_features: string[];
  symmetry_notes?: string;
  scale_inference_log?: string;
  ai_provider?: string;
  created_at?: string;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  product_type?: string;
  status: 'draft' | 'analyzing' | 'analyzed' | 'completed' | 'failed';
  reference_type: 'image' | 'multi_image' | 'pdf';
  overall_width?: number;
  overall_depth?: number;
  overall_height?: number;
  dimension_unit: string;
  width_status: DimensionStatus;
  depth_status: DimensionStatus;
  height_status: DimensionStatus;
  scale_anchor_desc?: string;
  scale_confidence: ConfidenceLevel;
  scale_warning?: string;
  waste_percentage: number;
  difficulty_level: string;
  estimated_build_time: string;
  primary_wood_species: string;
  created_at: string;
  updated_at: string;
  references: ReferenceItem[];
  analysis?: AnalysisData;
  components: ComponentItem[];
  cut_list_items: CutListItem[];
  materials: MaterialItem[];
  hardware: HardwareItem[];
  instructions: InstructionStep[];
  diagrams: DiagramItem[];
}

export interface ScaleAnchorData {
  anchor_type: string;
  anchor_dimension_value: number;
  anchor_axis: 'width' | 'depth' | 'height';
  description?: string;
}

export interface ProgressState {
  step: string;
  percentage: number;
}
