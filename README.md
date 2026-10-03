# WOODPLAN AI 🪵📐
> **"From Reference to Ready-to-Build."**  
> AI Woodworking Product Analyzer & DIY Plan Generator

WOODPLAN AI is an end-to-end, production-grade web application that turns any reference photo, screenshot, or existing PDF woodworking plan into a complete, shop-ready DIY build plan.

It decomposes product anatomy, identifies nominal lumber stock (1x4, 2x4, 2x6, plywood), estimates envelope dimensions via scale anchoring, calculates master cut lists with a 15% waste allowance, generates technical CAD-style orthographic blueprints, and produces printable, multi-page PDF woodworking manuals.

---

## 🌟 Key Features

- **Multi-Modal Reference Input:**
  - Drag-and-drop or upload images (`JPG`, `PNG`, `WEBP`)
  - Paste screenshots directly from the clipboard (`Ctrl+V`)
  - Multi-image reference support
  - Native Woodworking PDF ingestion (text parsing & visual layout extraction)
- **Dimension Inference & Scale Anchor Engine:**
  - Classifies measurements as `CONFIRMED`, `ESTIMATED`, `INFERRED`, or `USER_PROVIDED`
  - Scale anchoring to standard references (e.g., *Twin Mattress 38" × 75"*, *2x4 Lumber*, *Custom dimensions*)
  - Explicit warning badges: *"AI ESTIMATE — VERIFY BEFORE CUTTING"*
- **Structural Anatomical Decomposition:**
  - Component identification (Part ID, Name, Lumber Size, Finished Cut, Angles, Joinery, Hardware, Purpose)
  - Master Cut List with angles, kerf margin, and confidence levels
  - Material list grouped by nominal lumber with configurable cut waste percentage (default 15%)
  - Hardware specifications categorized by `REFERENCE_VISIBLE`, `REFERENCE_INFERRED`, and `OPTIONAL`
- **Joinery & Step-by-Step Instructions:**
  - Pocket holes, dados, lap joints, mortise & tenon, dowels, face screws, and PVA glue
  - Sequential shop stages with objectives, tooling, machining cuts, assembly, checkpoints, and safety alerts
- **CAD Technical Blueprint Drafting:**
  - Precision orthographic SVG views: **Front Elevation**, **Side Profile**, **Top / Plan View**, **Axonometric Exploded View**, and **Joinery Details**
  - Standard drafting arrows, extension lines, dimension callouts, and part ID balloons
  - Dual comparison view: *Source Reference* vs. *CAD Blueprint*
- **Shop-Ready Printable PDF:**
  - Cover page, project overview, tooling list, materials list, cut list, step-by-step instructions, finishing guide, and final quality checklist
  - Built with ReportLab using a clean woodworking blueprint aesthetic
- **Provider-Agnostic AI Architecture:**
  - Modular abstraction layer (`AIProvider`, `VisionProvider`, `TextProvider`, `DiagramProvider`, `PDFGenerator`)
  - Pluggable Google Gemini 1.5/2.5 Flash & OpenAI vision adapters
  - Embedded zero-friction rule-based geometric knowledge engine ensuring 100% offline uptime and resilience

---

## 🏗️ Architecture & Tech Stack

```
woodplan-ai/
├── backend/                  # FastAPI Python Backend
│   ├── app/
│   │   ├── main.py           # Application entrypoint & CORS
│   │   ├── config.py         # Settings & environment variables
│   │   ├── database.py       # SQLAlchemy engine & session factory
│   │   ├── models/           # Database tables (projects, components, cut lists, etc.)
│   │   ├── schemas/          # Pydantic validation schemas
│   │   ├── api/              # REST API routes (/api/projects)
│   │   └── services/
│   │       ├── ai/           # Gemini & fallback geometric engines
│   │       ├── pdf/          # ReportLab PDF generator & pypdf extractor
│   │       ├── diagrams/     # Precision SVG CAD blueprint generator
│   │       └── storage/      # File validation & disk storage
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Container build for Render
│   └── test_api.py           # Unit & integration test suite
│
├── frontend/                 # React + TypeScript + Vite Frontend
│   ├── src/
│   │   ├── api/client.ts     # Typed REST API client
│   │   ├── types/            # TypeScript definitions
│   │   ├── components/       # Reusable UI components
│   │   │   ├── Navbar.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── UploadZone.tsx
│   │   │   ├── BlueprintViewer.tsx
│   │   │   ├── AnalysisProgress.tsx
│   │   │   └── tabs/         # 10 plan specification tabs
│   │   └── views/            # Main application views
│   ├── tailwind.config.js    # Tailwind styling & blueprint themes
│   └── package.json
│
├── render.yaml               # Render Blueprint for Backend + Postgres
├── vercel.json               # Vercel SPA routing configuration
├── .env.example              # Environment variables template
└── DEPLOYMENT.md             # Production deployment guide
```

---

## 🚀 Quickstart (Local Development)

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)

### 1. Backend Setup
```bash
cd backend
python -m venv venv

# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend will start at: `http://localhost:8000` (API docs at `http://localhost:8000/docs`).

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend will start at: `http://localhost:5173`.

---

## 🧪 Running Automated Tests

Run the backend test suite:
```bash
cd backend
python test_api.py
```
Tests verify health check, project creation, seeded projects, SVG blueprint generation, and ReportLab PDF compilation.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/projects` | List all saved woodworking projects |
| `POST` | `/api/projects` | Initialize a new plan project |
| `GET` | `/api/projects/{id}` | Retrieve complete project specification |
| `PUT` | `/api/projects/{id}` | Update parameters, parts, or dimensions |
| `DELETE` | `/api/projects/{id}` | Delete a project and associated files |
| `POST` | `/api/projects/{id}/upload` | Upload reference image or PDF |
| `POST` | `/api/projects/{id}/analyze` | Trigger vision analysis & plan generation |
| `GET` | `/api/projects/{id}/progress` | Poll real-time progress state |
| `POST` | `/api/projects/{id}/reanalyze` | Recalculate cut lists from updated dimensions |
| `POST` | `/api/projects/{id}/generate-pdf`| Recompile printable PDF woodworking plan |
| `GET` | `/api/projects/{id}/pdf` | Download official blueprint PDF |

---

## 📄 License
MIT License. Crafted for makers, carpenters, and DIY enthusiasts.
