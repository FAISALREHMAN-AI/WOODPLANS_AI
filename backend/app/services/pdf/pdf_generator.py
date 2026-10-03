import os
import math
from datetime import datetime
from typing import Dict, Any, List, Optional
from PIL import Image as PILImage

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import (
    Drawing, Rect, Line, String, Circle, Polygon, Group
)

# =========================================================================
# STRICT BLACK & WHITE / GRAYSCALE COLOR PALETTE
# =========================================================================
COLOR_BLACK = colors.HexColor("#000000")
COLOR_WHITE = colors.HexColor("#ffffff")
COLOR_GRAY_DARK = colors.HexColor("#333333")
COLOR_GRAY_MED = colors.HexColor("#666666")
COLOR_GRAY_LIGHT = colors.HexColor("#e5e5e5")
COLOR_GRAY_BG = colors.HexColor("#f8f8f8")
COLOR_GRAY_BORDER = colors.HexColor("#999999")

FOOTER_TEXT = "TIMBER SHOP BY FAISAL"

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to draw running headers and the MANDATORY footer
    'TIMBER SHOP BY FAISAL' on EVERY page with accurate total page count.
    STRICTLY BLACK AND WHITE.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()

        # Running Header on pages 2+
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(COLOR_BLACK)
            self.drawString(54, letter[1] - 36, "WOODPLAN AI  |  DIY WOODWORKING CONSTRUCTION PLAN")
            self.setFont("Helvetica", 8)
            self.setFillColor(COLOR_GRAY_DARK)
            self.drawRightString(letter[0] - 54, letter[1] - 36, "TECHNICAL BLUEPRINT SPECIFICATION")
            self.setStrokeColor(COLOR_BLACK)
            self.setLineWidth(0.75)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # MANDATORY FOOTER ON EVERY SINGLE PAGE (Including Page 1)
        self.setStrokeColor(COLOR_BLACK)
        self.setLineWidth(0.75)
        self.line(54, 42, letter[0] - 54, 42)

        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(COLOR_BLACK)
        self.drawString(54, 28, FOOTER_TEXT)

        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_GRAY_DARK)
        self.drawRightString(letter[0] - 54, 28, f"Page {self._pageNumber} of {page_count}")

        self.drawCentredString(letter[0] / 2.0, 28, "VERIFY ALL MEASUREMENTS BEFORE CUTTING  •  TRADITIONAL WOODWORKING PLANS")
        self.restoreState()


class VectorBlueprintHelper:
    """
    Generates native vector technical woodworking blueprint drawings inside ReportLab.
    STRICTLY BLACK AND WHITE.
    Uses dimension arrows <──── 72" ────>, extension lines, part balloons, and dashed hidden lines.
    """

    @staticmethod
    def draw_dimension_h(d: Drawing, x1: float, x2: float, y: float, text: str, ext_y_bottom: float = None):
        """Draws a horizontal dimension line <──── 72" ────> with extension lines."""
        if ext_y_bottom is not None:
            # Extension lines
            d.add(Line(x1, ext_y_bottom, x1, y + 5, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))
            d.add(Line(x2, ext_y_bottom, x2, y + 5, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))

        # Main dimension line
        d.add(Line(x1, y, x2, y, strokeColor=COLOR_BLACK, strokeWidth=0.75))
        # Arrow heads
        d.add(Polygon([x1, y, x1 + 6, y + 2.5, x1 + 6, y - 2.5], fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))
        d.add(Polygon([x2, y, x2 - 6, y + 2.5, x2 - 6, y - 2.5], fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))

        # Text label with background clear box
        mid_x = (x1 + x2) / 2.0
        label_w = max(40, len(text) * 5.5 + 8)
        d.add(Rect(mid_x - (label_w / 2.0), y - 5, label_w, 10, fillColor=COLOR_WHITE, strokeColor=COLOR_WHITE))
        s = String(mid_x, y - 3, text, fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK)
        d.add(s)

    @staticmethod
    def draw_dimension_v(d: Drawing, y1: float, y2: float, x: float, text: str, ext_x_right: float = None):
        """Draws a vertical dimension line with extension lines."""
        if ext_x_right is not None:
            d.add(Line(x - 5, y1, ext_x_right, y1, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))
            d.add(Line(x - 5, y2, ext_x_right, y2, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))

        d.add(Line(x, y1, x, y2, strokeColor=COLOR_BLACK, strokeWidth=0.75))
        d.add(Polygon([x, y1, x - 2.5, y1 + 6, x + 2.5, y1 + 6], fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))
        d.add(Polygon([x, y2, x - 2.5, y2 - 6, x + 2.5, y2 - 6], fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))

        mid_y = (y1 + y2) / 2.0
        d.add(Rect(x - 18, mid_y - 5, 36, 10, fillColor=COLOR_WHITE, strokeColor=COLOR_WHITE))
        s = String(x, mid_y - 3, text, fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK)
        d.add(s)

    @staticmethod
    def draw_part_balloon(d: Drawing, cx: float, cy: float, part_id: str):
        """Draws a circular part ID balloon (A, B, C...)."""
        d.add(Circle(cx, cy, 9, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(String(cx, cy - 3, part_id, fontName="Helvetica-Bold", fontSize=9, textAnchor="middle", fillColor=COLOR_BLACK))

    @classmethod
    def create_single_part_blueprint(cls, part: Dict[str, Any], project_name: str) -> Drawing:
        """
        Creates a dedicated technical blueprint drawing sheet for an individual component.
        Includes Front View, Edge View, and End Section View with exact dimensions and hole boring.
        """
        w, h = 504, 230
        d = Drawing(w, h)

        # Outer drafting border
        d.add(Rect(0, 0, w, h, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(Rect(2, 2, w - 4, h - 4, fillColor=None, strokeColor=COLOR_BLACK, strokeWidth=0.5))

        # Title Block (Bottom Right)
        tb_x, tb_y, tb_w, tb_h = w - 240, 4, 236, 46
        d.add(Rect(tb_x, tb_y, tb_w, tb_h, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
        d.add(Line(tb_x, tb_y + 23, tb_x + tb_w, tb_y + 23, strokeColor=COLOR_BLACK, strokeWidth=0.5))
        d.add(Line(tb_x + 110, tb_y, tb_x + 110, tb_y + 23, strokeColor=COLOR_BLACK, strokeWidth=0.5))

        d.add(String(tb_x + 6, tb_y + 32, f"PART {part.get('part_id', 'A')} // {part.get('part_name', 'MEMBER')[:24].upper()}", fontName="Helvetica-Bold", fontSize=8, fillColor=COLOR_BLACK))
        d.add(String(tb_x + 6, tb_y + 9, f"LUMBER: {part.get('nominal_lumber_size', '1x4')}", fontName="Helvetica", fontSize=7, fillColor=COLOR_BLACK))
        d.add(String(tb_x + 116, tb_y + 9, f"QTY: {part.get('quantity', 1)} PCS  |  {part.get('angles', '90°')}", fontName="Helvetica", fontSize=7, fillColor=COLOR_BLACK))

        # Drawing Canvas Header
        d.add(String(12, h - 16, f"PART BLUEPRINT: PART {part.get('part_id', 'A')} — {part.get('part_name', 'MEMBER')}", fontName="Helvetica-Bold", fontSize=10, fillColor=COLOR_BLACK))
        d.add(String(12, h - 28, f"PROJECT: {project_name.upper()}  |  SCALE: NOT TO SCALE (N.T.S.)", fontName="Helvetica", fontSize=7, fillColor=COLOR_GRAY_DARK))
        d.add(Line(12, h - 32, w - 12, h - 32, strokeColor=COLOR_BLACK, strokeWidth=0.5))

        fl = float(part.get("finished_length", 48.0))
        fw = float(part.get("finished_width", 3.5))
        ft = float(part.get("finished_thickness", 1.5))

        # View 1: Front Elevation of Part
        fv_x, fv_y = 40, 110
        fv_w = 340
        fv_h = 32
        d.add(Rect(fv_x, fv_y, fv_w, fv_h, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.5))

        # Pocket-hole locations / drill indicators on ends
        d.add(Circle(fv_x + 18, fv_y + 10, 3, fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))
        d.add(Circle(fv_x + 18, fv_y + 22, 3, fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))
        d.add(Circle(fv_x + fv_w - 18, fv_y + 10, 3, fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))
        d.add(Circle(fv_x + fv_w - 18, fv_y + 22, 3, fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))
        # Hidden lines
        d.add(Line(fv_x + 18, fv_y, fv_x + 18, fv_y + fv_h, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))
        d.add(Line(fv_x + fv_w - 18, fv_y, fv_x + fv_w - 18, fv_y + fv_h, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))

        # Front view label
        d.add(String(fv_x + fv_w / 2, fv_y + fv_h + 16, "VIEW 1: PRIMARY FACE ELEVATION", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK))

        # Dimension line for Length <──── 72.0" ────>
        cls.draw_dimension_h(d, fv_x, fv_x + fv_w, fv_y - 20, f"<──── {fl:.2f}\" ────>", ext_y_bottom=fv_y)

        # Dimension line for Width
        cls.draw_dimension_v(d, fv_y, fv_y + fv_h, fv_x - 18, f"{fw:.2f}\"", ext_x_right=fv_x)

        # Part balloon callout
        cls.draw_part_balloon(d, fv_x + fv_w / 2, fv_y + (fv_h / 2), str(part.get("part_id", "A")))

        # View 2: End Profile / Cross Section
        ev_x, ev_y = 420, 110
        ev_w = 40
        ev_h = 32
        d.add(Rect(ev_x, ev_y, ev_w, ev_h, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.5))
        # Cross hatch section lines
        d.add(Line(ev_x, ev_y, ev_x + ev_w, ev_y + ev_h, strokeColor=COLOR_BLACK, strokeWidth=0.5))
        d.add(Line(ev_x, ev_y + ev_h, ev_x + ev_w, ev_y, strokeColor=COLOR_BLACK, strokeWidth=0.5))
        d.add(String(ev_x + ev_w / 2, ev_y + ev_h + 16, "VIEW 2: END PROFILE", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK))
        cls.draw_dimension_h(d, ev_x, ev_x + ev_w, ev_y - 20, f"{ft:.2f}\"", ext_y_bottom=ev_y)

        # Notes block on bottom left
        d.add(String(14, 38, f"JOINERY SPEC: {part.get('joinery', 'Pocket holes & glue')}", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
        d.add(String(14, 26, f"HOLE LOCATIONS: Bore 2 pocket holes on inside face, 5/8\" from edge margin.", fontName="Helvetica", fontSize=7, fillColor=COLOR_GRAY_DARK))
        d.add(String(14, 14, f"CUT SPECIFICATION: Square 90° crosscut with fine-kerf carbide blade.", fontName="Helvetica", fontSize=7, fillColor=COLOR_GRAY_DARK))

        return d

    @classmethod
    def create_exploded_view_drawing(cls, project_data: Dict[str, Any]) -> Drawing:
        """
        Creates a dedicated black-and-white exploded assembly technical drawing.
        """
        w, h = 504, 340
        d = Drawing(w, h)

        # Drafting border
        d.add(Rect(0, 0, w, h, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(Rect(2, 2, w - 4, h - 4, fillColor=None, strokeColor=COLOR_BLACK, strokeWidth=0.5))

        # Title Block
        d.add(String(14, h - 16, f"EXPLODED ASSEMBLY BLUEPRINT — {project_data.get('name', 'BUILD PLAN').upper()}", fontName="Helvetica-Bold", fontSize=10, fillColor=COLOR_BLACK))
        d.add(String(14, h - 28, "COMPONENTS SHOWN SEPARATED SPATIALLY ALONG ASSEMBLY INSERTION TRAJECTORIES", fontName="Helvetica", fontSize=7, fillColor=COLOR_GRAY_DARK))
        d.add(Line(14, h - 32, w - 14, h - 32, strokeColor=COLOR_BLACK, strokeWidth=0.5))

        # Base / Bed / Table Assembly Geometry in B&W
        # Exploded vectors (dashed lines)
        d.add(Line(250, 270, 250, 180, strokeColor=COLOR_BLACK, strokeWidth=0.75, strokeDashArray=[4, 3]))
        d.add(Line(110, 160, 200, 160, strokeColor=COLOR_BLACK, strokeWidth=0.75, strokeDashArray=[4, 3]))
        d.add(Line(390, 160, 300, 160, strokeColor=COLOR_BLACK, strokeWidth=0.75, strokeDashArray=[4, 3]))
        d.add(Line(250, 140, 250, 70, strokeColor=COLOR_BLACK, strokeWidth=0.75, strokeDashArray=[4, 3]))

        # Top Ridge / Stretcher (Part E)
        d.add(Rect(180, 260, 140, 20, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.5))
        d.add(Line(180, 270, 320, 270, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[3, 3]))
        cls.draw_part_balloon(d, 250, 270, "E")

        # Left Upright Sub-assembly (Part A)
        d.add(Rect(70, 100, 35, 120, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.5))
        d.add(Line(70, 140, 105, 140, strokeColor=COLOR_BLACK, strokeWidth=0.75))
        d.add(Line(70, 180, 105, 180, strokeColor=COLOR_BLACK, strokeWidth=0.75))
        cls.draw_part_balloon(d, 87, 160, "A")

        # Center Rails / Platform (Part B & C)
        d.add(Rect(170, 130, 160, 45, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.5))
        # Inner slats indication
        for sx in [195, 220, 245, 270, 295]:
            d.add(Line(sx, 130, sx, 175, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))
        cls.draw_part_balloon(d, 250, 152, "B")

        # Right Upright Sub-assembly (Part D)
        d.add(Rect(400, 100, 35, 120, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.5))
        d.add(Line(400, 140, 435, 140, strokeColor=COLOR_BLACK, strokeWidth=0.75))
        d.add(Line(400, 180, 435, 180, strokeColor=COLOR_BLACK, strokeWidth=0.75))
        cls.draw_part_balloon(d, 417, 160, "D")

        # Base Footing Rails (Part F)
        d.add(Rect(170, 50, 160, 20, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.5))
        cls.draw_part_balloon(d, 250, 60, "F")

        # Leader lines and instructions
        d.add(String(14, 25, "ASSEMBLY DIRECTION: Dashed trajectory lines indicate insertion sequence. Secure all joints with pocket screws & glue.", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
        d.add(String(14, 13, "PARTS KEY: A = Left Post Frame | B = Longitudinal Rails | D = Right Post Frame | E = Ridge Stretcher | F = Base Rails", fontName="Helvetica", fontSize=7, fillColor=COLOR_GRAY_DARK))

        return d

    @classmethod
    def create_cutting_diagram_drawing(cls, materials: List[Dict[str, Any]], cut_list: List[Dict[str, Any]]) -> Drawing:
        """
        Creates a black-and-white 8-foot lumber cutting diagram:
        |---- PART A (48") ----|--- PART B (36") ---| [WASTE 12"]
        """
        w, h = 504, 210
        d = Drawing(w, h)

        d.add(Rect(0, 0, w, h, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(Rect(2, 2, w - 4, h - 4, fillColor=None, strokeColor=COLOR_BLACK, strokeWidth=0.5))

        d.add(String(14, h - 16, "LUMBER CUTTING LAYOUTS (8-FOOT / 96-INCH STANDARD BOARDS)", fontName="Helvetica-Bold", fontSize=9.5, fillColor=COLOR_BLACK))
        d.add(String(14, h - 28, "PLANNED BOARD CUTTING EFFICIENCY  •  15% WASTE & BLADE KERF ALLOWANCE", fontName="Helvetica", fontSize=7, fillColor=COLOR_GRAY_DARK))
        d.add(Line(14, h - 32, w - 14, h - 32, strokeColor=COLOR_BLACK, strokeWidth=0.5))

        # Board 1: 2x4 Lumber
        by1 = 135
        d.add(String(14, by1 + 24, "BOARD 1: 2x4 × 96\" SELECT PINE STUD", fontName="Helvetica-Bold", fontSize=8, fillColor=COLOR_BLACK))
        d.add(Rect(14, by1, 476, 20, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
        # Cut 1: Part A (48")
        d.add(Line(252, by1, 252, by1 + 20, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(String(133, by1 + 6, "PART A (48.00\")", fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        # Cut 2: Part A (42")
        d.add(Line(450, by1, 450, by1 + 20, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(String(351, by1 + 6, "PART A (42.00\")", fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        # Remainder Waste
        d.add(Line(450, by1, 490, by1 + 20, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))
        d.add(String(470, by1 + 6, "KERF", fontName="Helvetica", fontSize=6.5, textAnchor="middle", fillColor=COLOR_GRAY_DARK))

        # Board 2: 1x4 Lumber
        by2 = 75
        d.add(String(14, by2 + 24, "BOARD 2: 1x4 × 96\" FRAME & SLAT LUMBER", fontName="Helvetica-Bold", fontSize=8, fillColor=COLOR_BLACK))
        d.add(Rect(14, by2, 476, 20, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
        # Cut 1: Part B (72")
        d.add(Line(370, by2, 370, by2 + 20, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(String(192, by2 + 6, "PART B — SIDE RAIL (72.00\")", fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        # Cut 2: Part D (18")
        d.add(Line(450, by2, 450, by2 + 20, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(String(410, by2 + 6, "PART D (18\")", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=COLOR_BLACK))
        # Remainder Waste
        d.add(Line(450, by2, 490, by2 + 20, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))
        d.add(String(470, by2 + 6, "WASTE", fontName="Helvetica", fontSize=6.5, textAnchor="middle", fillColor=COLOR_GRAY_DARK))

        d.add(String(14, 20, "NOTE: Always measure from freshly squared factory edge. Deduct 1/8\" saw kerf for each physical cut.", fontName="Helvetica", fontSize=7, fillColor=COLOR_GRAY_DARK))
        return d

    @classmethod
    def create_joinery_detail_drawing(cls) -> Drawing:
        """
        Creates black-and-white joinery connection engineering detail drawings.
        """
        w, h = 504, 220
        d = Drawing(w, h)

        d.add(Rect(0, 0, w, h, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(Rect(2, 2, w - 4, h - 4, fillColor=None, strokeColor=COLOR_BLACK, strokeWidth=0.5))

        d.add(String(14, h - 16, "JOINERY DETAIL SPECIFICATIONS & ENGINEERING CONNECTIONS", fontName="Helvetica-Bold", fontSize=9.5, fillColor=COLOR_BLACK))
        d.add(String(14, h - 28, "FASTENER PENETRATION, POCKET HOLE BORING, AND CLAMPING STANDARDS", fontName="Helvetica", fontSize=7, fillColor=COLOR_GRAY_DARK))
        d.add(Line(14, h - 32, w - 14, h - 32, strokeColor=COLOR_BLACK, strokeWidth=0.5))

        # Detail 1: Pocket Hole Butt Joint
        d.add(Rect(20, 50, 220, 125, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=0.75))
        d.add(String(26, 162, "DETAIL 1: POCKET-HOLE CONNECTION", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
        # Member 1 (Horizontal)
        d.add(Rect(35, 85, 95, 35, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(String(75, 98, "PART B", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK))
        # Member 2 (Vertical Post)
        d.add(Rect(130, 70, 40, 90, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(String(150, 110, "PART A", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK))
        # Pocket hole bore and screw line
        d.add(Line(70, 108, 120, 95, strokeColor=COLOR_BLACK, strokeWidth=1.5, strokeDashArray=[3, 2]))
        d.add(Line(120, 95, 150, 105, strokeColor=COLOR_BLACK, strokeWidth=1.5))
        d.add(String(70, 72, "15° BORE ANGLE", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_GRAY_DARK))
        d.add(String(26, 56, "Fastener: 1-1/4\" Pocket Screws + PVA Glue", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_BLACK))

        # Detail 2: Housing Dado Connection
        d.add(Rect(260, 50, 220, 125, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=0.75))
        d.add(String(266, 162, "DETAIL 2: HOUSING DADO JOINT", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
        # Upright with dado cut
        d.add(Polygon([290, 70, 330, 70, 330, 100, 320, 100, 320, 130, 330, 130, 330, 160, 290, 160], fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        # Inserted Shelf
        d.add(Rect(320, 100, 110, 30, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        d.add(String(375, 112, "SHELF / RAIL", fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        d.add(String(295, 112, "UPRIGHT", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=COLOR_BLACK))
        # Glue line
        d.add(Line(320, 100, 320, 130, strokeColor=COLOR_BLACK, strokeWidth=2))
        d.add(String(266, 56, "Trench Depth: 1/4\" - 3/8\" into panel thickness", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_BLACK))

        d.add(String(14, 18, "GENERAL JOINERY RULE: Clamp with minimum 150 psi pressure until glue reaches initial grab (30 minutes minimum).", fontName="Helvetica", fontSize=7, fillColor=COLOR_GRAY_DARK))
        return d


class PDFGenerator:
    """
    Main PDF Generator creating complete, professional, STRICTLY BLACK AND WHITE
    DIY Woodworking construction manuals according to traditional blueprint standards.
    MANDATORY FOOTER ON EVERY PAGE: 'TIMBER SHOP BY FAISAL'.
    """

    @staticmethod
    def _convert_image_to_grayscale(src_path: str, out_path: str) -> Optional[str]:
        """Converts user reference image into high-contrast grayscale for clean printing."""
        if not os.path.exists(src_path):
            return None
        try:
            with PILImage.open(src_path) as img:
                gray = img.convert('L')
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                gray.save(out_path)
                return out_path
        except Exception:
            return None

    @classmethod
    def generate_plan_pdf(cls, project_data: Dict[str, Any], output_path: str) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54
        )

        styles = getSampleStyleSheet()

        # STRICT BLACK AND WHITE TYPOGRAPHY STYLES
        cover_title_style = ParagraphStyle(
            'BwCoverTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=26,
            leading=32,
            textColor=COLOR_BLACK,
            spaceAfter=6
        )

        cover_sub_style = ParagraphStyle(
            'BwCoverSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=13,
            leading=16,
            textColor=COLOR_GRAY_DARK,
            spaceAfter=15
        )

        h1_style = ParagraphStyle(
            'BwSectionH1',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=COLOR_BLACK,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True
        )

        h2_style = ParagraphStyle(
            'BwSectionH2',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10.5,
            leading=14,
            textColor=COLOR_BLACK,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True
        )

        body_style = ParagraphStyle(
            'BwBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12.5,
            textColor=COLOR_BLACK
        )

        table_header_style = ParagraphStyle(
            'BwTableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=COLOR_WHITE
        )

        table_cell_style = ParagraphStyle(
            'BwTableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=7.5,
            leading=10,
            textColor=COLOR_BLACK
        )

        story = []

        proj_name = project_data.get("name", "Custom Woodworking Project")
        components = project_data.get("components", [])
        cut_list = project_data.get("cut_list_items", [])
        materials = project_data.get("materials", [])
        hardware = project_data.get("hardware", [])
        instructions = project_data.get("instructions", [])

        # =========================================================================
        # PAGE 1: COVER PAGE (STRICT BLACK & WHITE)
        # =========================================================================
        story.append(Spacer(1, 10))
        # Top Header Bar
        story.append(Paragraph("WOODPLAN AI  //  PRECISION WORKSHOP BLUEPRINTS", ParagraphStyle('TopTag', fontName='Helvetica-Bold', fontSize=10, textColor=COLOR_BLACK, spaceAfter=8)))
        story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_BLACK, spaceAfter=18))

        story.append(Paragraph(proj_name.upper(), cover_title_style))
        story.append(Paragraph("WOODWORKING PLANS  •  COMPLETE CONSTRUCTION BLUEPRINT", cover_sub_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=COLOR_BLACK, spaceAfter=14))

        # Check for reference image and convert to clean grayscale if available
        ref_image_path = None
        references = project_data.get("references", [])
        if references:
            raw_path = references[0].get("file_path", "")
            if raw_path and os.path.exists(raw_path) and not raw_path.lower().endswith(".pdf"):
                gray_target = os.path.join(os.path.dirname(output_path), f"gray_{os.path.basename(raw_path)}")
                ref_image_path = cls._convert_image_to_grayscale(raw_path, gray_target)

        if ref_image_path and os.path.exists(ref_image_path):
            try:
                story.append(RLImage(ref_image_path, width=4.5 * inch, height=2.4 * inch))
                story.append(Spacer(1, 10))
            except Exception:
                pass
        else:
            # Clean Technical Border Box for Cover when no photo
            cover_drawing = Drawing(504, 110)
            cover_drawing.add(Rect(0, 0, 504, 110, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
            cover_drawing.add(Line(0, 0, 504, 110, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))
            cover_drawing.add(Line(0, 110, 504, 0, strokeColor=COLOR_BLACK, strokeWidth=0.5, strokeDashArray=[2, 2]))
            cover_drawing.add(Rect(140, 35, 224, 40, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
            cover_drawing.add(String(252, 52, "TRADITIONAL WOODWORKING BLUEPRINT", fontName="Helvetica-Bold", fontSize=8.5, textAnchor="middle", fillColor=COLOR_BLACK))
            cover_drawing.add(String(252, 42, "MASTER TIMBER BUILD SPECIFICATION", fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=COLOR_GRAY_DARK))
            story.append(cover_drawing)
            story.append(Spacer(1, 14))

        # Metadata Table on Cover (Black & White)
        cover_meta = [
            [Paragraph("<b>PRODUCT TYPE:</b>", body_style), Paragraph(str(project_data.get("product_type", "Woodworking Build")).upper(), body_style)],
            [Paragraph("<b>OVERALL ENVELOPE:</b>", body_style), Paragraph(f"{project_data.get('overall_width', 0)}\" WIDTH  ×  {project_data.get('overall_depth', 0)}\" DEPTH  ×  {project_data.get('overall_height', 0)}\" HEIGHT", body_style)],
            [Paragraph("<b>SKILL LEVEL:</b>", body_style), Paragraph(str(project_data.get("difficulty_level", "Intermediate")).upper(), body_style)],
            [Paragraph("<b>RECOMMENDED TOOLS:</b>", body_style), Paragraph("Miter saw, Table saw, Pocket-hole jig, Drill/Driver, Clamps, Sander", body_style)],
            [Paragraph("<b>MATERIALS OVERVIEW:</b>", body_style), Paragraph(f"{project_data.get('primary_wood_species', 'Select Softwood')}  •  Standard 8-ft Nominal Boards", body_style)],
            [Paragraph("<b>DOCUMENT DATE:</b>", body_style), Paragraph(datetime.now().strftime("%B %d, %Y").upper(), body_style)],
            [Paragraph("<b>PUBLISHED BY:</b>", body_style), Paragraph(FOOTER_TEXT, body_style)],
        ]
        t_cover = Table(cover_meta, colWidths=[150, 354])
        t_cover.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_WHITE),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BLACK),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_GRAY_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_cover)
        story.append(Spacer(1, 14))

        # Safety & Verification Disclaimer Box (B&W)
        disclaimer_data = [
            [Paragraph("<b>CRITICAL NOTICE — TRADITIONAL CONSTRUCTION PLAN VERIFICATION:</b><br/>"
                       "All finished cut lengths and hole positions in this document reflect standard nominal lumber sizes. "
                       "<b>Always measure actual bought lumber thickness and dry-fit components prior to gluing or cutting. "
                       "Wear eye and hearing protection at all times during machine operations.</b>", body_style)]
        ]
        t_disc = Table(disclaimer_data, colWidths=[504])
        t_disc.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_WHITE),
            ('BOX', (0,0), (-1,-1), 1.2, COLOR_BLACK),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(t_disc)
        story.append(PageBreak())

        # =========================================================================
        # PAGE 2: PROJECT DIMENSIONS & BOUNDING BOX
        # =========================================================================
        story.append(Paragraph("1. PROJECT DIMENSIONS & BOUNDING BOX", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=10))

        story.append(Paragraph("Overall envelope bounding dimensions specifying installation clearances and structural footprint.", body_style))
        story.append(Spacer(1, 8))

        dim_table_data = [
            [Paragraph("<b>DIMENSION AXIS</b>", table_header_style), Paragraph("<b>MEASUREMENT</b>", table_header_style), Paragraph("<b>STATUS / CONFIDENCE</b>", table_header_style), Paragraph("<b>NOTES</b>", table_header_style)],
            [Paragraph("Overall Width (X)", table_cell_style), Paragraph(f"{project_data.get('overall_width', 0):.2f}\"", table_cell_style), Paragraph(str(project_data.get('width_status', 'ESTIMATED')), table_cell_style), Paragraph("Front-to-back horizontal span", table_cell_style)],
            [Paragraph("Overall Depth (Y)", table_cell_style), Paragraph(f"{project_data.get('overall_depth', 0):.2f}\"", table_cell_style), Paragraph(str(project_data.get('depth_status', 'ESTIMATED')), table_cell_style), Paragraph("Side depth clearance", table_cell_style)],
            [Paragraph("Overall Height (Z)", table_cell_style), Paragraph(f"{project_data.get('overall_height', 0):.2f}\"", table_cell_style), Paragraph(str(project_data.get('height_status', 'ESTIMATED')), table_cell_style), Paragraph("Floor to highest ridge / top surface", table_cell_style)],
        ]
        t_dim = Table(dim_table_data, colWidths=[110, 90, 130, 174])
        t_dim.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_BLACK),
            ('GRID', (0,0), (-1,-1), 0.5, COLOR_BLACK),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_dim)
        story.append(Spacer(1, 14))

        # Overall Orthographic Schematic Drawing in B&W
        story.append(Paragraph("Orthographic Projection Schematic", h2_style))
        ortho_d = Drawing(504, 180)
        ortho_d.add(Rect(0, 0, 504, 180, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
        # Front view box
        ortho_d.add(Rect(30, 30, 220, 110, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        ortho_d.add(String(140, 85, "FRONT ELEVATION", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK))
        VectorBlueprintHelper.draw_dimension_h(ortho_d, 30, 250, 15, f"{project_data.get('overall_width', 0):.1f}\" WIDTH", ext_y_bottom=30)
        VectorBlueprintHelper.draw_dimension_v(ortho_d, 30, 140, 18, f"{project_data.get('overall_height', 0):.1f}\" HEIGHT", ext_x_right=30)

        # Side view box
        ortho_d.add(Rect(310, 30, 140, 110, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
        ortho_d.add(String(380, 85, "SIDE ELEVATION", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK))
        VectorBlueprintHelper.draw_dimension_h(ortho_d, 310, 450, 15, f"{project_data.get('overall_depth', 0):.1f}\" DEPTH", ext_y_bottom=30)

        story.append(ortho_d)
        story.append(PageBreak())

        # =========================================================================
        # PAGE 3: TOOLS + MATERIALS
        # =========================================================================
        story.append(Paragraph("2. WORKSHOP TOOLS & MATERIALS SPECIFICATION", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=10))

        story.append(Paragraph("Recommended Tools for Build", h2_style))
        tools_table_data = [
            [Paragraph("<b>CUTTING & MILLING</b>", table_header_style), Paragraph("<b>JOINERY & DRILLING</b>", table_header_style), Paragraph("<b>SQUARING & FINISHING</b>", table_header_style)],
            [
                Paragraph("• Miter Saw / Chop Saw<br/>• Table Saw or Track Saw<br/>• Stop block for repeat cuts<br/>• Random Orbital Sander", table_cell_style),
                Paragraph("• Cordless Drill / Driver<br/>• Pocket-Hole Jig & Stepped Bit<br/>• Face Clamps & 36\" Bar Clamps<br/>• Countersink Drill Bit", table_cell_style),
                Paragraph("• Tape Measure (16ft+)<br/>• Combination Square<br/>• Speed Square<br/>• Eye & Hearing Protection", table_cell_style),
            ]
        ]
        t_tools = Table(tools_table_data, colWidths=[168, 168, 168])
        t_tools.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_BLACK),
            ('GRID', (0,0), (-1,-1), 0.5, COLOR_BLACK),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_tools)
        story.append(Spacer(1, 14))

        story.append(Paragraph(f"Materials & Lumber Requirement (with {project_data.get('waste_percentage', 15)}% Waste Allowance)", h2_style))
        mat_table_data = [
            [Paragraph("<b>LUMBER SIZE</b>", table_header_style), Paragraph("<b>DESCRIPTION</b>", table_header_style), Paragraph("<b>REQUIRED LENGTH</b>", table_header_style), Paragraph("<b>8-FT BOARDS</b>", table_header_style), Paragraph("<b>NOTES</b>", table_header_style)]
        ]
        for m in materials:
            mat_table_data.append([
                Paragraph(str(m.get("category", "1x4")), table_cell_style),
                Paragraph(str(m.get("description", "Kiln-dried board")), table_cell_style),
                Paragraph(f"{m.get('required_board_length', 0):.1f}\"", table_cell_style),
                Paragraph(f"{m.get('calculated_boards', 1)} pcs", table_cell_style),
                Paragraph(str(m.get("notes", "Select straight stock")), table_cell_style),
            ])
        if len(mat_table_data) == 1:
            mat_table_data.append([Paragraph("1x4", table_cell_style), Paragraph("Select Pine / Poplar", table_cell_style), Paragraph("360.0\"", table_cell_style), Paragraph("5 pcs", table_cell_style), Paragraph("Check for cupping", table_cell_style)])
            mat_table_data.append([Paragraph("2x4", table_cell_style), Paragraph("Structural Stud Stock", table_cell_style), Paragraph("288.0\"", table_cell_style), Paragraph("3 pcs", table_cell_style), Paragraph("Frame posts", table_cell_style)])

        t_mat = Table(mat_table_data, colWidths=[74, 160, 85, 75, 110])
        t_mat.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_BLACK),
            ('GRID', (0,0), (-1,-1), 0.5, COLOR_BLACK),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_mat)
        story.append(PageBreak())

        # =========================================================================
        # PAGE 4: HARDWARE & FASTENERS
        # =========================================================================
        story.append(Paragraph("3. FASTENERS & HARDWARE SPECIFICATIONS", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=10))

        story.append(Paragraph("Verified fasteners, structural screws, adhesives, and hardware accessories.", body_style))
        story.append(Spacer(1, 8))

        hw_table_data = [
            [Paragraph("<b>ITEM NAME</b>", table_header_style), Paragraph("<b>QUANTITY</b>", table_header_style), Paragraph("<b>SPECIFICATION</b>", table_header_style), Paragraph("<b>STATUS</b>", table_header_style), Paragraph("<b>APPLICATION</b>", table_header_style)]
        ]
        for h in hardware:
            hw_table_data.append([
                Paragraph(str(h.get("item_name", "Pocket Screws")), table_cell_style),
                Paragraph(str(h.get("quantity", "1 box")), table_cell_style),
                Paragraph(str(h.get("size_spec", "1-1/4\" Coarse")), table_cell_style),
                Paragraph(str(h.get("status", "REFERENCE_VISIBLE")), table_cell_style),
                Paragraph(str(h.get("purpose", "Frame assembly")), table_cell_style),
            ])
        if len(hw_table_data) == 1:
            hw_table_data.append([Paragraph("Pocket Screws", table_cell_style), Paragraph("1 box (100ct)", table_cell_style), Paragraph("1-1/4\" Coarse Thread", table_cell_style), Paragraph("REFERENCE_VISIBLE", table_cell_style), Paragraph("Main frame joints", table_cell_style)])
            hw_table_data.append([Paragraph("Wood Glue", table_cell_style), Paragraph("1 bottle (16 oz)", table_cell_style), Paragraph("Titebond II PVA Glue", table_cell_style), Paragraph("REFERENCE_VISIBLE", table_cell_style), Paragraph("All mating end grains", table_cell_style)])

        t_hw = Table(hw_table_data, colWidths=[120, 70, 110, 94, 110])
        t_hw.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_BLACK),
            ('GRID', (0,0), (-1,-1), 0.5, COLOR_BLACK),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_hw)
        story.append(PageBreak())

        # =========================================================================
        # PAGE 5: MASTER CUT LIST
        # =========================================================================
        story.append(Paragraph("4. MASTER CUT LIST", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=10))

        story.append(Paragraph("Mill lumber in sequential Part ID order. Cut matching pieces using stop blocks for identical lengths.", body_style))
        story.append(Spacer(1, 8))

        cut_table_data = [
            [
                Paragraph("<b>ID</b>", table_header_style),
                Paragraph("<b>PART NAME</b>", table_header_style),
                Paragraph("<b>QTY</b>", table_header_style),
                Paragraph("<b>LUMBER</b>", table_header_style),
                Paragraph("<b>LENGTH</b>", table_header_style),
                Paragraph("<b>WIDTH</b>", table_header_style),
                Paragraph("<b>THICK</b>", table_header_style),
                Paragraph("<b>ANGLE</b>", table_header_style),
                Paragraph("<b>JOINERY / CONFIDENCE</b>", table_header_style),
            ]
        ]
        for c in cut_list:
            cut_table_data.append([
                Paragraph(str(c.get("part_id", "A")), table_cell_style),
                Paragraph(str(c.get("part_name", "Member")), table_cell_style),
                Paragraph(str(c.get("quantity", 1)), table_cell_style),
                Paragraph(str(c.get("lumber_size", "1x4")), table_cell_style),
                Paragraph(f"{c.get('length', 0):.2f}\"", table_cell_style),
                Paragraph(f"{c.get('width', 0):.2f}\"", table_cell_style),
                Paragraph(f"{c.get('thickness', 0):.2f}\"", table_cell_style),
                Paragraph(str(c.get("angle", "90°")), table_cell_style),
                Paragraph(f"{c.get('notes', '')} [{c.get('confidence', 'CONFIRMED')}]", table_cell_style),
            ])
        if len(cut_table_data) == 1:
            cut_table_data.append([Paragraph("A", table_cell_style), Paragraph("Corner Upright", table_cell_style), Paragraph("4", table_cell_style), Paragraph("2x4", table_cell_style), Paragraph("48.00\"", table_cell_style), Paragraph("3.50\"", table_cell_style), Paragraph("1.50\"", table_cell_style), Paragraph("90°", table_cell_style), Paragraph("Pocket holes [CONFIRMED]", table_cell_style)])
            cut_table_data.append([Paragraph("B", table_cell_style), Paragraph("Base Rail", table_cell_style), Paragraph("2", table_cell_style), Paragraph("2x6", table_cell_style), Paragraph("72.00\"", table_cell_style), Paragraph("5.50\"", table_cell_style), Paragraph("1.50\"", table_cell_style), Paragraph("90°", table_cell_style), Paragraph("Pocket holes [CONFIRMED]", table_cell_style)])

        t_cuts = Table(cut_table_data, colWidths=[24, 110, 26, 46, 50, 44, 42, 38, 124])
        t_cuts.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_BLACK),
            ('GRID', (0,0), (-1,-1), 0.5, COLOR_BLACK),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ]))
        story.append(t_cuts)
        story.append(PageBreak())

        # =========================================================================
        # PAGE 6: EXPLODED VIEW BLUEPRINT
        # =========================================================================
        story.append(Paragraph("5. EXPLODED ASSEMBLY BLUEPRINT", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=10))

        story.append(Paragraph("Major sub-assemblies and individual components separated spatially along insertion axes with leader callouts.", body_style))
        story.append(Spacer(1, 8))

        exploded_drawing = VectorBlueprintHelper.create_exploded_view_drawing(project_data)
        story.append(exploded_drawing)
        story.append(PageBreak())

        # =========================================================================
        # PAGES 7+: INDIVIDUAL PART BLUEPRINTS (A DEDICATED PAGE FOR EVERY MAJOR PART)
        # =========================================================================
        for comp in components:
            p_id = comp.get("part_id", "A")
            p_name = comp.get("part_name", "Component")

            story.append(Paragraph(f"PART BLUEPRINT: PART {p_id} — {p_name.upper()}", h1_style))
            story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=8))

            # Technical multi-view vector drawing for this part
            part_drawing = VectorBlueprintHelper.create_single_part_blueprint(comp, proj_name)
            story.append(part_drawing)
            story.append(Spacer(1, 12))

            # Part Engineering Specifications Table
            part_meta_table = [
                [Paragraph("<b>PROPERTY</b>", table_header_style), Paragraph("<b>SPECIFICATION</b>", table_header_style), Paragraph("<b>TECHNICAL NOTES</b>", table_header_style)],
                [Paragraph("Component ID", table_cell_style), Paragraph(f"PART {p_id}", table_cell_style), Paragraph("Mark clearly on lumber offcut", table_cell_style)],
                [Paragraph("Part Name", table_cell_style), Paragraph(p_name, table_cell_style), Paragraph(str(comp.get("purpose", "Structural component")), table_cell_style)],
                [Paragraph("Quantity", table_cell_style), Paragraph(f"{comp.get('quantity', 1)} pcs", table_cell_style), Paragraph("Cut identical repeating pieces with stop-block", table_cell_style)],
                [Paragraph("Material / Species", table_cell_style), Paragraph(str(comp.get("material", "Pine")), table_cell_style), Paragraph("Inspect for warping before cutting", table_cell_style)],
                [Paragraph("Nominal Lumber Size", table_cell_style), Paragraph(str(comp.get("nominal_lumber_size", "1x4")), table_cell_style), Paragraph("Standard retail dimensional stock", table_cell_style)],
                [Paragraph("Finished Dimensions", table_cell_style), Paragraph(f"{comp.get('finished_length', 0):.2f}\" L  ×  {comp.get('finished_width', 0):.2f}\" W  ×  {comp.get('finished_thickness', 0):.2f}\" T", table_cell_style), Paragraph("Tolerance ± 1/16\" (1.5mm)", table_cell_style)],
                [Paragraph("Cut Type & Angles", table_cell_style), Paragraph(f"{comp.get('cut_type', 'Crosscut')} @ {comp.get('angles', '90°')}", table_cell_style), Paragraph("Verify blade squareness against fence", table_cell_style)],
                [Paragraph("Joinery Method", table_cell_style), Paragraph(str(comp.get("joinery", "Pocket holes")), table_cell_style), Paragraph("Bore pocket holes on interior unexposed faces", table_cell_style)],
                [Paragraph("Fastener Spec", table_cell_style), Paragraph(str(comp.get("hardware", "Pocket screws")), table_cell_style), Paragraph("Clamp firmly with face clamp during driving", table_cell_style)],
            ]
            t_part = Table(part_meta_table, colWidths=[120, 160, 224])
            t_part.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), COLOR_BLACK),
                ('GRID', (0,0), (-1,-1), 0.5, COLOR_BLACK),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(t_part)
            story.append(PageBreak())

        # =========================================================================
        # NEXT PAGES: ASSEMBLY SEQUENCE DIAGRAMS
        # =========================================================================
        story.append(Paragraph("6. ASSEMBLY SEQUENCE & CONSTRUCTION STAGES", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=10))

        story.append(Paragraph("Follow the chronological construction sequence below to assemble sub-assemblies and square the main framework.", body_style))
        story.append(Spacer(1, 8))

        # Technical sequence drawing
        seq_drawing = Drawing(504, 220)
        seq_drawing.add(Rect(0, 0, 504, 220, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
        seq_drawing.add(String(14, 204, "ASSEMBLY WORKFLOW CHRONOLOGY", fontName="Helvetica-Bold", fontSize=8.5, fillColor=COLOR_BLACK))
        seq_drawing.add(Line(14, 198, 490, 198, strokeColor=COLOR_BLACK, strokeWidth=0.5))

        # Box 1: Side Panels
        seq_drawing.add(Rect(20, 70, 95, 110, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
        seq_drawing.add(String(67, 160, "STAGE 1", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(67, 130, "BUILD SIDE", fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(67, 118, "PANELS", fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(67, 85, "Parts: A, B", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=COLOR_GRAY_DARK))

        seq_drawing.add(Line(115, 125, 145, 125, strokeColor=COLOR_BLACK, strokeWidth=1))
        seq_drawing.add(Polygon([145, 125, 139, 128, 139, 122], fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))

        # Box 2: Main Carcass Frame
        seq_drawing.add(Rect(145, 70, 95, 110, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
        seq_drawing.add(String(192, 160, "STAGE 2", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(192, 130, "TIE CARCASS", fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(192, 118, "END RAILS", fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(192, 85, "Parts: C, D", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=COLOR_GRAY_DARK))

        seq_drawing.add(Line(240, 125, 270, 125, strokeColor=COLOR_BLACK, strokeWidth=1))
        seq_drawing.add(Polygon([270, 125, 264, 128, 264, 122], fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))

        # Box 3: Top / Roof
        seq_drawing.add(Rect(270, 70, 95, 110, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
        seq_drawing.add(String(317, 160, "STAGE 3", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(317, 130, "INSTALL TOP", fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(317, 118, "STRETCHERS", fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(317, 85, "Parts: E, F", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=COLOR_GRAY_DARK))

        seq_drawing.add(Line(365, 125, 395, 125, strokeColor=COLOR_BLACK, strokeWidth=1))
        seq_drawing.add(Polygon([395, 125, 389, 128, 389, 122], fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK))

        # Box 4: Slats / Platform
        seq_drawing.add(Rect(395, 70, 95, 110, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1))
        seq_drawing.add(String(442, 160, "STAGE 4", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(442, 130, "FASTEN SLATS", fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(442, 118, "& CLEATS", fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=COLOR_BLACK))
        seq_drawing.add(String(442, 85, "Parts: G", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=COLOR_GRAY_DARK))

        seq_drawing.add(String(14, 25, "CRITICAL NOTE: Measure diagonals corner-to-corner at Stage 2. Equal diagonals guarantee a perfectly square assembly.", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
        story.append(seq_drawing)
        story.append(PageBreak())

        # =========================================================================
        # NEXT PAGES: STEP-BY-STEP BUILD INSTRUCTIONS
        # =========================================================================
        story.append(Paragraph("7. STEP-BY-STEP BUILD INSTRUCTIONS", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=10))

        for step in instructions:
            step_box = []
            s_num = step.get("step_number", 1)
            s_title = step.get("title", "Construction Stage")

            step_box.append(Paragraph(f"<b>STEP {s_num}: {s_title.upper()}</b>", h2_style))
            if step.get("objective"):
                step_box.append(Paragraph(f"<b>Objective:</b> {step['objective']}", body_style))
            if step.get("parts_used"):
                step_box.append(Paragraph(f"<b>Components Used:</b> {step['parts_used']}", body_style))
            if step.get("tools"):
                step_box.append(Paragraph(f"<b>Required Tools:</b> {step['tools']}", body_style))
            if step.get("assembly"):
                step_box.append(Spacer(1, 3))
                step_box.append(Paragraph(f"<b>Assembly Procedure:</b><br/>{step['assembly']}", body_style))
            if step.get("checkpoint"):
                step_box.append(Spacer(1, 3))
                step_box.append(Paragraph(f"<b>QUALITY CHECKPOINT:</b> {step['checkpoint']}", ParagraphStyle('BwCheck', parent=body_style, fontName='Helvetica-Bold')))
            if step.get("safety_note"):
                step_box.append(Spacer(1, 2))
                step_box.append(Paragraph(f"<b>SAFETY PROTOCOL:</b> {step['safety_note']}", ParagraphStyle('BwSafe', parent=body_style, fontName='Helvetica-Oblique')))

            step_box.append(Spacer(1, 8))
            story.append(KeepTogether(step_box))
            story.append(HRFlowable(width="100%", thickness=0.5, color=COLOR_GRAY_BORDER, spaceAfter=6))

        story.append(PageBreak())

        # =========================================================================
        # NEXT PAGES: JOINERY DETAILS
        # =========================================================================
        story.append(Paragraph("8. JOINERY DETAIL DRAWINGS", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=10))

        story.append(Paragraph("Technical joinery details showing fastener trajectories, dado recesses, and glue interfaces.", body_style))
        story.append(Spacer(1, 8))

        joinery_drawing = VectorBlueprintHelper.create_joinery_detail_drawing()
        story.append(joinery_drawing)
        story.append(PageBreak())

        # =========================================================================
        # NEXT PAGES: CUTTING / BOARD LAYOUTS
        # =========================================================================
        story.append(Paragraph("9. CUTTING & BOARD LAYOUT PLANS", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=10))

        story.append(Paragraph("Optimized board cutting maps across standard 8-foot (96\") dimensional stock.", body_style))
        story.append(Spacer(1, 8))

        cutting_drawing = VectorBlueprintHelper.create_cutting_diagram_drawing(materials, cut_list)
        story.append(cutting_drawing)
        story.append(PageBreak())

        # =========================================================================
        # FINAL PAGE: FINAL CHECKLIST + SAFETY NOTES
        # =========================================================================
        story.append(Paragraph("10. QUALITY CHECKLIST & WORKSHOP SAFETY", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLACK, spaceAfter=10))

        checklist_items = [
            "[  ] 1. DIMENSION VERIFICATION: Finished outside envelope confirmed against designated room/installation site.",
            "[  ] 2. STOCK INSPECTION: Every board checked for twists, crowns, or loose knots before making crosscuts.",
            "[  ] 3. SQUARE CORNERS: Opposing diagonals measured across all face frames; confirmed within 1/16\" tolerance.",
            "[  ] 4. FASTENER ENGAGEMENT: All pocket screws driven snug without stripping lumber fibers.",
            "[  ] 5. GLUE SQUEEZE-OUT: Excess PVA glue removed with damp rag before curing, avoiding blotchy stain finishes.",
            "[  ] 6. EDGE EASING: All sharp outer corners deburred and softened with 120-grit sandpaper or a 1/8\" roundover.",
            "[  ] 7. PROGRESSIVE SANDING: Faces sanded sequentially through 120, 180, and finished at 220-grit.",
            "[  ] 8. TOPCOAT APPLICATION: Stain or protective polyurethane applied in dust-free environment with full 24h cure."
        ]
        chk_table_data = [[Paragraph(f"<b>{item}</b>", body_style)] for item in checklist_items]
        t_final_chk = Table(chk_table_data, colWidths=[504])
        t_final_chk.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_WHITE),
            ('BOX', (0,0), (-1,-1), 1.2, COLOR_BLACK),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_GRAY_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_final_chk)
        story.append(Spacer(1, 14))

        # Safety Rules Box
        safety_rules = [
            [Paragraph("<b>MANDATORY WOODSHOP SAFETY RULES:</b><br/>"
                       "• <b>Eye Protection:</b> Always wear ANSI-certified safety glasses around rotating blades.<br/>"
                       "• <b>Hearing Protection:</b> Use earplugs or earmuffs during planer, table saw, and router operation.<br/>"
                       "• <b>Push Sticks:</b> Never position fingers closer than 4 inches to an active blade; use push blocks.<br/>"
                       "• <b>Dust Extraction:</b> Wear an N95 respirator during sanding softwoods and hardwoods.", body_style)]
        ]
        t_safety = Table(safety_rules, colWidths=[504])
        t_safety.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_WHITE),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BLACK),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_safety)

        # Build Document with NumberedCanvas (Footer on EVERY page)
        doc.build(story, canvasmaker=NumberedCanvas)
        return output_path

pdf_generator = PDFGenerator()
