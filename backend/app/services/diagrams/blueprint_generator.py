from typing import List, Dict, Any

class BlueprintGenerator:
    """
    Generates precision technical woodworking blueprints and CAD-style SVG diagrams.
    STRICTLY BLACK AND WHITE ONLY (White background, crisp black lines, black dimension arrows).
    Title block includes the mandatory attribution: TIMBER SHOP BY FAISAL.
    """

    @staticmethod
    def _svg_wrapper(inner_svg: str, width: int = 900, height: int = 560, title: str = "", subtitle: str = "") -> str:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" class="blueprint-svg">
  <defs>
    <!-- Technical Black Arrowheads -->
    <marker id="arrow-start" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 8 2 L 2 5 L 8 8 z" fill="#000000" />
    </marker>
    <marker id="arrow-end" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 2 2 L 8 5 L 2 8 z" fill="#000000" />
    </marker>
    <marker id="arrow-vector" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 2 2 L 8 5 L 2 8 z" fill="#000000" />
    </marker>
  </defs>

  <!-- Pure White Background Canvas -->
  <rect width="{width}" height="{height}" fill="#ffffff" stroke="#000000" stroke-width="1.5" />

  <!-- Outer Double Drafting Border -->
  <rect x="18" y="18" width="{width - 36}" height="{height - 36}" fill="none" stroke="#000000" stroke-width="1.2" />
  <rect x="22" y="22" width="{width - 44}" height="{height - 44}" fill="none" stroke="#666666" stroke-width="0.5" />

  <!-- Technical Drawing Title Block (Bottom Right) -->
  <g transform="translate({width - 340}, {height - 76})">
    <rect width="315" height="52" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
    <line x1="0" y1="26" x2="315" y2="26" stroke="#000000" stroke-width="0.75" />
    <line x1="160" y1="26" x2="160" y2="52" stroke="#000000" stroke-width="0.75" />
    <text x="12" y="17" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold" letter-spacing="0.5">TIMBER SHOP BY FAISAL // CAD</text>
    <text x="12" y="42" fill="#444444" font-family="'JetBrains Mono', Courier, monospace" font-size="9">SCALE: N.T.S. (INCHES)</text>
    <text x="172" y="42" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="9" font-weight="bold">{title.upper()[:16]}</text>
  </g>

  <!-- Top Header Block -->
  <g transform="translate(36, 44)">
    <text x="0" y="0" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="15" font-weight="bold">{title.upper()}</text>
    <text x="0" y="16" fill="#555555" font-family="'JetBrains Mono', Courier, monospace" font-size="10">{subtitle.upper()}</text>
    <line x1="0" y1="22" x2="{width - 72}" y2="22" stroke="#000000" stroke-width="0.75" />
  </g>

  <!-- Bottom Attribution Footer -->
  <text x="36" y="{height - 30}" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="8.5" font-weight="bold">TIMBER SHOP BY FAISAL  •  BLACK &amp; WHITE TECHNICAL DRAFTING SPECIFICATION</text>

  <!-- Content -->
  {inner_svg}
</svg>"""

    @classmethod
    def generate_front_view(cls, product_name: str, width_in: float, height_in: float, depth_in: float, components: List[Dict[str, Any]]) -> str:
        w_in = width_in or 60.0
        h_in = height_in or 48.0

        scale = min(480 / max(w_in, 1), 280 / max(h_in, 1))
        dw = w_in * scale
        dh = h_in * scale

        ox = 450 - (dw / 2)
        oy = 110 + (280 - dh) / 2

        dim_y = oy + dh + 35
        dim_x = ox - 40

        inner = f"""
  <!-- Front Elevation Orthographic Silhouette (Pure B&W) -->
  <g id="front-elevation" stroke="#000000" stroke-width="1.8" fill="#ffffff">
    <!-- Main Outer Framework -->
    <rect x="{ox}" y="{oy}" width="{dw}" height="{dh}" stroke="#000000" stroke-width="2" />

    <!-- Vertical Stile Posts -->
    <rect x="{ox + 6}" y="{oy + 6}" width="{dw * 0.08}" height="{dh - 12}" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
    <rect x="{ox + dw - (dw * 0.08) - 6}" y="{oy + 6}" width="{dw * 0.08}" height="{dh - 12}" fill="#ffffff" stroke="#000000" stroke-width="1.5" />

    <!-- Horizontal Rails -->
    <rect x="{ox + 6}" y="{oy + dh * 0.25}" width="{dw - 12}" height="{dh * 0.08}" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
    <rect x="{ox + 6}" y="{oy + dh * 0.72}" width="{dw - 12}" height="{dh * 0.08}" fill="#ffffff" stroke="#000000" stroke-width="1.2" />

    <!-- Center Stretcher / Divider -->
    <line x1="{ox + (dw/2)}" y1="{oy + dh * 0.25}" x2="{ox + (dw/2)}" y2="{oy + dh * 0.72}" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" />

    <!-- Part Balloons (A, B, C) -->
    <g transform="translate({ox + dw*0.04 + 6}, {oy + dh*0.5})">
      <circle cx="0" cy="0" r="12" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="0" y="4" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">A</text>
    </g>
    <g transform="translate({ox + dw*0.5}, {oy + dh*0.25 + dh*0.04})">
      <circle cx="0" cy="0" r="12" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="0" y="4" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">B</text>
    </g>
    <g transform="translate({ox + dw*0.5}, {oy + dh*0.72 + dh*0.04})">
      <circle cx="0" cy="0" r="12" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="0" y="4" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">C</text>
    </g>
  </g>

  <!-- Horizontal Dimension Line <──── 72.0" ────> -->
  <g id="dim-width">
    <line x1="{ox}" y1="{oy + dh + 4}" x2="{ox}" y2="{dim_y + 8}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{ox + dw}" y1="{oy + dh + 4}" x2="{ox + dw}" y2="{dim_y + 8}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{ox}" y1="{dim_y}" x2="{ox + dw}" y2="{dim_y}" stroke="#000000" stroke-width="1" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
    <rect x="{ox + (dw/2) - 55}" y="{dim_y - 8}" width="110" height="16" fill="#ffffff" stroke="#ffffff" />
    <text x="{ox + (dw/2)}" y="{dim_y + 4}" fill="#000000" text-anchor="middle" font-family="'JetBrains Mono', Courier, monospace" font-size="11" font-weight="bold">&lt;──── {w_in:.1f}\" OVERALL ────&gt;</text>
  </g>

  <!-- Vertical Dimension Line -->
  <g id="dim-height">
    <line x1="{ox - 4}" y1="{oy}" x2="{dim_x - 8}" y2="{oy}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{ox - 4}" y1="{oy + dh}" x2="{dim_x - 8}" y2="{oy + dh}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{dim_x}" y1="{oy}" x2="{dim_x}" y2="{oy + dh}" stroke="#000000" stroke-width="1" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
    <g transform="translate({dim_x - 8}, {oy + (dh/2)}) rotate(-90)">
      <rect x="-45" y="-8" width="90" height="16" fill="#ffffff" stroke="#ffffff" />
      <text x="0" y="4" fill="#000000" text-anchor="middle" font-family="'JetBrains Mono', Courier, monospace" font-size="11" font-weight="bold">&lt;── {h_in:.1f}\" HEIGHT ──&gt;</text>
    </g>
  </g>
"""
        return cls._svg_wrapper(inner, 900, 560, f"FRONT ELEVATION — {product_name}", f"Overall Width {w_in:.1f}\" × Height {h_in:.1f}\" [Black & White Orthographic Blueprint]")

    @classmethod
    def generate_side_view(cls, product_name: str, depth_in: float, height_in: float, width_in: float) -> str:
        d_in = depth_in or 36.0
        h_in = height_in or 48.0

        scale = min(400 / max(d_in, 1), 280 / max(h_in, 1))
        dd = d_in * scale
        dh = h_in * scale

        ox = 450 - (dd / 2)
        oy = 110 + (280 - dh) / 2

        dim_y = oy + dh + 35
        dim_x = ox - 40

        inner = f"""
  <g id="side-elevation" stroke="#000000" stroke-width="1.8" fill="#ffffff">
    <rect x="{ox}" y="{oy}" width="{dd}" height="{dh}" stroke="#000000" stroke-width="2" />
    <rect x="{ox + 6}" y="{oy + 6}" width="{dd * 0.12}" height="{dh - 12}" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
    <rect x="{ox + dd - (dd * 0.12) - 6}" y="{oy + 6}" width="{dd * 0.12}" height="{dh - 12}" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
    <rect x="{ox + 6}" y="{oy + dh * 0.3}" width="{dd - 12}" height="{dh * 0.08}" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
    <rect x="{ox + 6}" y="{oy + dh * 0.75}" width="{dd - 12}" height="{dh * 0.08}" fill="#ffffff" stroke="#000000" stroke-width="1.2" />

    <g transform="translate({ox + dd*0.06 + 6}, {oy + dh*0.4})">
      <circle cx="0" cy="0" r="12" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="0" y="4" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">D</text>
    </g>
    <g transform="translate({ox + dd*0.5}, {oy + dh*0.3 + dh*0.04})">
      <circle cx="0" cy="0" r="12" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="0" y="4" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">E</text>
    </g>
  </g>

  <g id="dim-depth">
    <line x1="{ox}" y1="{oy + dh + 4}" x2="{ox}" y2="{dim_y + 8}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{ox + dd}" y1="{oy + dh + 4}" x2="{ox + dd}" y2="{dim_y + 8}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{ox}" y1="{dim_y}" x2="{ox + dd}" y2="{dim_y}" stroke="#000000" stroke-width="1" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
    <rect x="{ox + (dd/2) - 50}" y="{dim_y - 8}" width="100" height="16" fill="#ffffff" stroke="#ffffff" />
    <text x="{ox + (dd/2)}" y="{dim_y + 4}" fill="#000000" text-anchor="middle" font-family="'JetBrains Mono', Courier, monospace" font-size="11" font-weight="bold">&lt;──── {d_in:.1f}\" DEPTH ────&gt;</text>
  </g>

  <g id="dim-height">
    <line x1="{ox - 4}" y1="{oy}" x2="{dim_x - 8}" y2="{oy}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{ox - 4}" y1="{oy + dh}" x2="{dim_x - 8}" y2="{oy + dh}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{dim_x}" y1="{oy}" x2="{dim_x}" y2="{oy + dh}" stroke="#000000" stroke-width="1" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
    <g transform="translate({dim_x - 8}, {oy + (dh/2)}) rotate(-90)">
      <rect x="-45" y="-8" width="90" height="16" fill="#ffffff" stroke="#ffffff" />
      <text x="0" y="4" fill="#000000" text-anchor="middle" font-family="'JetBrains Mono', Courier, monospace" font-size="11" font-weight="bold">&lt;── {h_in:.1f}\" HEIGHT ──&gt;</text>
    </g>
  </g>
"""
        return cls._svg_wrapper(inner, 900, 560, f"SIDE ELEVATION — {product_name}", f"Depth {d_in:.1f}\" × Height {h_in:.1f}\" [End Profile]")

    @classmethod
    def generate_top_view(cls, product_name: str, width_in: float, depth_in: float) -> str:
        w_in = width_in or 60.0
        d_in = depth_in or 36.0

        scale = min(500 / max(w_in, 1), 280 / max(d_in, 1))
        dw = w_in * scale
        dd = d_in * scale

        ox = 450 - (dw / 2)
        oy = 110 + (280 - dd) / 2

        dim_y = oy + dd + 35
        dim_x = ox - 40

        inner = f"""
  <g id="top-plan" stroke="#000000" stroke-width="1.8" fill="#ffffff">
    <rect x="{ox}" y="{oy}" width="{dw}" height="{dd}" stroke="#000000" stroke-width="2" />
    <!-- 4 Corner Posts -->
    <rect x="{ox + 6}" y="{oy + 6}" width="{dw * 0.08}" height="{dd * 0.12}" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
    <rect x="{ox + dw - (dw * 0.08) - 6}" y="{oy + 6}" width="{dw * 0.08}" height="{dd * 0.12}" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
    <rect x="{ox + 6}" y="{oy + dd - (dd * 0.12) - 6}" width="{dw * 0.08}" height="{dd * 0.12}" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
    <rect x="{ox + dw - (dw * 0.08) - 6}" y="{oy + dd - (dd * 0.12) - 6}" width="{dw * 0.08}" height="{dd * 0.12}" fill="#ffffff" stroke="#000000" stroke-width="1.5" />

    <!-- Slat array -->
    <line x1="{ox + dw*0.25}" y1="{oy + 6}" x2="{ox + dw*0.25}" y2="{oy + dd - 6}" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,3" />
    <line x1="{ox + dw*0.5}" y1="{oy + 6}" x2="{ox + dw*0.5}" y2="{oy + dd - 6}" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,3" />
    <line x1="{ox + dw*0.75}" y1="{oy + 6}" x2="{ox + dw*0.75}" y2="{oy + dd - 6}" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,3" />
  </g>

  <g id="dim-width">
    <line x1="{ox}" y1="{oy + dd + 4}" x2="{ox}" y2="{dim_y + 8}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{ox + dw}" y1="{oy + dd + 4}" x2="{ox + dw}" y2="{dim_y + 8}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{ox}" y1="{dim_y}" x2="{ox + dw}" y2="{dim_y}" stroke="#000000" stroke-width="1" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
    <rect x="{ox + (dw/2) - 50}" y="{dim_y - 8}" width="100" height="16" fill="#ffffff" stroke="#ffffff" />
    <text x="{ox + (dw/2)}" y="{dim_y + 4}" fill="#000000" text-anchor="middle" font-family="'JetBrains Mono', Courier, monospace" font-size="11" font-weight="bold">&lt;──── {w_in:.1f}\" WIDTH ────&gt;</text>
  </g>

  <g id="dim-depth">
    <line x1="{ox - 4}" y1="{oy}" x2="{dim_x - 8}" y2="{oy}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{ox - 4}" y1="{oy + dd}" x2="{dim_x - 8}" y2="{oy + dd}" stroke="#000000" stroke-width="0.75" stroke-dasharray="2,2" />
    <line x1="{dim_x}" y1="{oy}" x2="{dim_x}" y2="{oy + dd}" stroke="#000000" stroke-width="1" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
    <g transform="translate({dim_x - 8}, {oy + (dd/2)}) rotate(-90)">
      <rect x="-45" y="-8" width="90" height="16" fill="#ffffff" stroke="#ffffff" />
      <text x="0" y="4" fill="#000000" text-anchor="middle" font-family="'JetBrains Mono', Courier, monospace" font-size="11" font-weight="bold">&lt;── {d_in:.1f}\" DEPTH ──&gt;</text>
    </g>
  </g>
"""
        return cls._svg_wrapper(inner, 900, 560, f"TOP / PLAN VIEW — {product_name}", f"Width {w_in:.1f}\" × Depth {d_in:.1f}\" [Horizontal Overhead Section]")

    @classmethod
    def generate_exploded_view(cls, product_name: str, components: List[Dict[str, Any]]) -> str:
        inner = """
  <g id="exploded-isometric" transform="translate(160, 90)">
    <!-- Insertion trajectories in dashed black lines -->
    <path d="M 280 300 L 280 190" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#arrow-vector)" />
    <path d="M 110 210 L 210 210" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#arrow-vector)" />
    <path d="M 450 210 L 350 210" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#arrow-vector)" />
    <path d="M 280 60 L 280 140" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#arrow-vector)" />

    <!-- Top Ridge Stretcher (Part E) -->
    <g transform="translate(180, 15)">
      <polygon points="100,0 200,20 100,40 0,20" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <polygon points="0,20 100,40 100,55 0,35" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
      <polygon points="100,40 200,20 200,35 100,55" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
      <circle cx="100" cy="20" r="12" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="100" y="24" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">E</text>
    </g>

    <!-- Left Side Sub-assembly (Part A) -->
    <g transform="translate(20, 130)">
      <polygon points="40,0 80,10 80,140 40,130" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <polygon points="0,15 40,0 40,130 0,145" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <circle cx="40" cy="65" r="12" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="40" y="69" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">A</text>
    </g>

    <!-- Center Support Rails / Platform (Part B & C) -->
    <g transform="translate(180, 150)">
      <polygon points="100,0 200,25 100,50 0,25" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <polygon points="0,25 100,50 100,70 0,45" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
      <polygon points="100,50 200,25 200,45 100,70" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
      <circle cx="100" cy="35" r="12" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="100" y="39" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">B</text>
    </g>

    <!-- Right Side Sub-assembly (Part D) -->
    <g transform="translate(440, 130)">
      <polygon points="40,0 80,10 80,140 40,130" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <polygon points="0,15 40,0 40,130 0,145" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <circle cx="40" cy="65" r="12" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="40" y="69" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">D</text>
    </g>

    <!-- Base Foot Frame (Part F) -->
    <g transform="translate(180, 275)">
      <polygon points="100,0 200,20 100,40 0,20" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <polygon points="0,20 100,40 100,55 0,35" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
      <polygon points="100,40 200,20 200,35 100,55" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
      <circle cx="100" cy="25" r="12" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="100" y="29" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">F</text>
    </g>
  </g>

  <!-- Assembly Legend -->
  <g transform="translate(36, 470)">
    <rect width="828" height="36" fill="#ffffff" stroke="#000000" stroke-width="1" />
    <text x="14" y="22" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="9.5" font-weight="bold">EXPLODED VECTOR KEY: Dashed black arrows indicate spatial separation and insertion order.</text>
  </g>
"""
        return cls._svg_wrapper(inner, 900, 560, f"EXPLODED ASSEMBLY VIEW — {product_name}", "Axonometric Component Separation & Joinery Alignment")

    @classmethod
    def generate_joinery_view(cls, product_name: str) -> str:
        inner = """
  <g transform="translate(50, 95)">
    <!-- Detail 1: Pocket Hole Joint -->
    <g transform="translate(0, 0)">
      <rect width="380" height="230" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
      <text x="18" y="26" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="11" font-weight="bold">DETAIL 1: POCKET-HOLE CONNECTION</text>
      <text x="18" y="42" fill="#444444" font-family="'JetBrains Mono', Courier, monospace" font-size="9">1-1/4" Pocket Screws + Titebond II PVA Glue</text>
      <line x1="18" y1="48" x2="362" y2="48" stroke="#000000" stroke-width="0.5" />

      <!-- Horizontal Rail Member -->
      <rect x="40" y="90" width="150" height="50" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="115" y="120" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="9" font-weight="bold">PART B (RAIL)</text>

      <!-- Vertical Post Member -->
      <rect x="190" y="70" width="60" height="130" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <text x="220" y="140" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="9" font-weight="bold">PART A</text>

      <!-- Pocket hole bore and trajectory -->
      <path d="M 80 115 L 145 100 L 205 115" stroke="#000000" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#arrow-vector)" />
      <polygon points="120,90 145,100 135,115 105,100" fill="#ffffff" stroke="#000000" stroke-width="1" />

      <path d="M 90 115 A 25 25 0 0 1 110 105" fill="none" stroke="#000000" stroke-width="1" />
      <text x="75" y="140" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="9" font-weight="bold">15° DRILL ANGLE</text>

      <text x="260" y="140" fill="#444444" font-family="'JetBrains Mono', Courier, monospace" font-size="9">FACE CLAMP</text>
      <path d="M 255 135 L 215 135" stroke="#000000" stroke-width="1" marker-end="url(#arrow-end)" />
    </g>

    <!-- Detail 2: Housing Dado Joint -->
    <g transform="translate(420, 0)">
      <rect width="380" height="230" fill="#ffffff" stroke="#000000" stroke-width="1.2" />
      <text x="18" y="26" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="11" font-weight="bold">DETAIL 2: HOUSING DADO JOINT</text>
      <text x="18" y="42" fill="#444444" font-family="'JetBrains Mono', Courier, monospace" font-size="9">Dado Depth: 1/4" to 3/8" of Panel Thickness</text>
      <line x1="18" y1="48" x2="362" y2="48" stroke="#000000" stroke-width="0.5" />

      <!-- Vertical Upright with Dado Trench -->
      <path d="M 60 70 L 120 70 L 120 110 L 105 110 L 105 150 L 120 150 L 120 190 L 60 190 Z" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
      <!-- Inserted Shelf / Divider -->
      <rect x="105" y="110" width="150" height="40" fill="#ffffff" stroke="#000000" stroke-width="1.5" stroke-dasharray="4,2" />
      <text x="180" y="135" text-anchor="middle" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="9" font-weight="bold">INSERTED SHELF</text>

      <!-- Glue Layer Indicator -->
      <line x1="105" y1="110" x2="105" y2="150" stroke="#000000" stroke-width="3" />
      <text x="175" y="180" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="9">GLUE SPREAD</text>
      <line x1="170" y1="175" x2="110" y2="135" stroke="#000000" stroke-width="1" marker-end="url(#arrow-vector)" />

      <!-- Depth Measurement -->
      <line x1="120" y1="100" x2="105" y2="100" stroke="#000000" stroke-width="1" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
      <text x="95" y="93" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="8.5" font-weight="bold">DADO DEPTH</text>
    </g>

    <!-- Standards Box -->
    <g transform="translate(0, 250)">
      <rect width="800" height="90" fill="#ffffff" stroke="#000000" stroke-width="1" />
      <text x="18" y="24" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="10" font-weight="bold">FASTENER &amp; DRILLING STANDARDS (TIMBER SHOP BY FAISAL):</text>
      <text x="18" y="44" fill="#333333" font-family="'JetBrains Mono', Courier, monospace" font-size="9">• 3/4" Stock: Pre-drill 1/8" pilot hole, use 1-1/4" coarse pocket screws.</text>
      <text x="18" y="62" fill="#333333" font-family="'JetBrains Mono', Courier, monospace" font-size="9">• 1-1/2" Stock (2x4 / 2x6): Pre-drill with stop collar, use 2-1/2" heavy duty screws.</text>
      <text x="18" y="80" fill="#000000" font-family="'JetBrains Mono', Courier, monospace" font-size="9" font-weight="bold">• CRITICAL: Always test pocket hole depth on scrap offcut before boring structural pieces.</text>
    </g>
  </g>
"""
        return cls._svg_wrapper(inner, 900, 560, f"JOINERY & FASTENER DETAILS — {product_name}", "Pocket Holes, Dados, Pilot Holes & Structural Fastening")

    @classmethod
    def generate_all_diagrams(cls, product_name: str, width_in: float, height_in: float, depth_in: float, components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                "view_type": "front",
                "title": "Front Elevation View",
                "description": f"Front technical blueprint with overall width ({width_in or 60.0}\") and height ({height_in or 48.0}\") dimensions, component locations, and vertical spacing.",
                "svg_content": cls.generate_front_view(product_name, width_in, height_in, depth_in, components),
                "sort_order": 1
            },
            {
                "view_type": "side",
                "title": "Side Elevation View",
                "description": f"Side profile blueprint showing overall depth ({depth_in or 36.0}\"), frame stretchers, and leg alignments.",
                "svg_content": cls.generate_side_view(product_name, depth_in, height_in, width_in),
                "sort_order": 2
            },
            {
                "view_type": "top",
                "title": "Top / Plan View",
                "description": f"Top-down orthographic plan view ({width_in or 60.0}\" × {depth_in or 36.0}\") displaying internal slats, corner posts, and perimeter rails.",
                "svg_content": cls.generate_top_view(product_name, width_in, depth_in),
                "sort_order": 3
            },
            {
                "view_type": "exploded",
                "title": "Exploded Assembly Diagram",
                "description": "Axonometric exploded view showing individual components detached along assembly trajectories with part ID balloons.",
                "svg_content": cls.generate_exploded_view(product_name, components),
                "sort_order": 4
            },
            {
                "view_type": "joinery",
                "title": "Joinery Detail Blueprint",
                "description": "Cross-sectional joint engineering specs including pocket hole boring angles, dado recesses, and fastener depths.",
                "svg_content": cls.generate_joinery_view(product_name),
                "sort_order": 5
            }
        ]

blueprint_generator = BlueprintGenerator()
