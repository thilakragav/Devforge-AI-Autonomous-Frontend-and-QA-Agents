# DevForge AI — Multi-Agent System for Automated Frontend Development and QA Testing

An autonomous, collaborative two-agent engineering architecture designed to convert website reference designs into production-ready modular Astro applications and validate them using automated visual, responsive, and functional quality assurance.

Built for the **48-Hour Technical Assessment Challenge**, using **RDGCC.com** as the target reference design.

---

## 1. System Overview

```
                                      +-----------------------------+
                                      |   Reference Design Input    |
                                      | (PNG, JPG, PDF, Figma URL)  |
                                      +--------------+--------------+
                                                     |
                                                     v
                                      +-----------------------------+
                                      |     Central Orchestrator    |
                                      |       (State Machine)       |
                                      +-------+--------------+------+
                                              |              ^
                                     Step 1-4 |              | Step 13-16
                                    [Generate]|              | [Feedback Loop]
                                              v              |
+------------------------------------+   +----+--------------+------+
|     Agent 1: Design-to-Astro       |   |      Agent 2: UI & QA    |
| - Layout & Token Decomposition     |   | - OpenCV SSIM & Pixel    |
| - Modular Astro Components         |   | - Playwright 3 Viewports |
| - Decoupled Content (homepage.js)  |   | - Functional DOM Testing |
| - Sanity CMS Schema Architecture   |   | - Executive HTML & PDF   |
+-----------------+------------------+   +--------------+-----------+
                  |                                     ^
                  v                                     |
+-------------------------------------------------------+-----------+
|                   Astro Application Runtime                       |
|   (Header, Navigation, Hero, About, Sectors, Stats, Projects, etc)|
+-------------------------------------------------------------------+
```

### The Two Collaborative AI Agents:
1. **Agent 1 (Design-to-Astro Code Generator)**:
   - Ingests visual assets (PNG, JPG, PDF with PyMuPDF page rasterization, Figma URLs).
   - Decomposes visual hierarchy into brand color tokens (`#0A192F` dark navy, `#C29B38` accent gold), typography scales, and 8 discrete sections.
   - Generates maintainable, modular Astro components (`Header.astro`, `Navigation.astro`, `Hero.astro`, `About.astro`, `Sectors.astro`, `Stats.astro`, `Projects.astro`, `Contact.astro`, `Footer.astro`, `MainLayout.astro`, `index.astro`).
   - Decouples structured content into `src/data/homepage.js` and creates Sanity-compatible schemas.
   - Applies surgical refactoring based on QA feedback without regenerating unaffected code.

2. **Agent 2 (UI and QA Testing Agent)**:
   - **Measurable Visual Testing**: OpenCV Structural Similarity Index (SSIM), pixel discrepancy percentage, contour bounding box overlays, and Vision LLM qualitative critique.
   - **Responsive Testing**: Headless browser viewport validation at Desktop (1440Ã—900), Tablet (768Ã—1024), and Mobile (375Ã—812). Checks horizontal overflow, text clipping, and navigation collapse.
   - **Functional Testing**: Verifies real DOM anchor destinations, interactive button accessibility, corporate contact form input validation, and image alt tags.
   - **Executive Reporting**: Produces structured JSON, interactive HTML ledgers, and ReportLab PDF audit reports.

3. **Central Multi-Agent Orchestrator**:
   - Implements a closed-loop state machine with up to **3 automated feedback correction loops**.
   - Translates failed QA assertions into typed Pydantic `CorrectionDirective` instructions for Agent 1.
   - Maintains version history (`v1` $\to$ `v2` $\to$ `v3`), audit snapshots, and real-time telemetry logs.

4. **Developer Cockpit Dashboard**:
   - Modern React + Vite + TypeScript + Tailwind CSS developer interface.
   - 6 Dedicated Pages: **Dashboard Overview**, **Design Input**, **Agent 1 Workspace**, **Agent 2 Workspace**, **QA Reports**, and **Agent Activity Telemetry**.

---

## 2. Technology Stack

- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons.
- **Backend**: Python 3.10+, FastAPI, Pydantic v2, Uvicorn.
- **AI Integration**: Multimodal Vision LLM (Google Gemini / OpenAI / Anthropic compatible adapter) with transparent deterministic test mode when API keys are absent.
- **Agent 1**: Python, Astro 4.x, HTML5, Semantic CSS, JavaScript, Sanity CMS Schema.
- **Agent 2**: Python, Playwright, OpenCV (`cv2`), Pillow (`PIL`), ReportLab (PDF), BeautifulSoup4.
- **Version Control & IDE**: Git, GitHub ready, 100% Cursor and VS Code independent.

---

## 3. Repository Structure

```
AI-Agent-PoC/
â”œâ”€â”€ frontend/
â”‚   â””â”€â”€ dashboard/                  # React + Vite + TypeScript + Tailwind Dashboard
â”‚       â”œâ”€â”€ src/
â”‚       â”‚   â”œâ”€â”€ components/         # MetricCard, CodeViewer, ImageCompareSlider, Sidebar, Header
â”‚       â”‚   â”œâ”€â”€ pages/              # 6 Complete Views (Dashboard, Input, A1, A2, Reports, Activity)
â”‚       â”‚   â”œâ”€â”€ services/           # Typed API Client (fetch)
â”‚       â”‚   â””â”€â”€ types/              # TypeScript Interfaces matching Pydantic schemas
â”‚       â”œâ”€â”€ package.json
â”‚       â”œâ”€â”€ vite.config.ts
â”‚       â””â”€â”€ tailwind.config.js
â”‚
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ main.py                     # FastAPI Application Entrypoint & Static Server
â”‚   â”œâ”€â”€ requirements.txt            # Python Dependencies
â”‚   â”œâ”€â”€ agents/
â”‚   â”‚   â”œâ”€â”€ agent1/                 # Design-to-Astro Generator (analyzer, generator, refactorer)
â”‚   â”‚   â””â”€â”€ agent2/                 # UI & QA Testing Agent (visual_diff, responsive, functional, reports)
â”‚   â”œâ”€â”€ orchestrator/               # Central Pipeline State Machine & Loop Controller
â”‚   â”œâ”€â”€ services/                   # LLMService, AstroService, FileService, PDFService
â”‚   â”œâ”€â”€ schemas/                    # Pydantic Schemas (agent1, agent2, orchestrator)
â”‚   â”œâ”€â”€ api/routes/                 # Modular API Endpoints (upload, agent1, agent2, orchestrator, reports)
â”‚   â””â”€â”€ utils/                      # Logger & Security Path Containment
â”‚
â”œâ”€â”€ generated_projects/
â”‚   â””â”€â”€ project_001/                # Complete Modular Generated RDGCC Astro Application
â”‚       â”œâ”€â”€ src/
â”‚       â”‚   â”œâ”€â”€ components/         # 8 Discrete Astro Components
â”‚       â”‚   â”œâ”€â”€ layouts/            # MainLayout.astro
â”‚       â”‚   â”œâ”€â”€ pages/              # index.astro
â”‚       â”‚   â”œâ”€â”€ data/               # homepage.js (Structured Content)
â”‚       â”‚   â”œâ”€â”€ schemas/            # Sanity CMS Schemas
â”‚       â”‚   â””â”€â”€ styles/             # global.css
â”‚       â”œâ”€â”€ public/preview.html     # Pre-rendered HTML for Browser QA & iframe inspection
â”‚       â”œâ”€â”€ package.json
â”‚       â””â”€â”€ astro.config.mjs
â”‚
â”œâ”€â”€ uploads/                        # Reference Mockups (rdgcc_reference.png, PDFs)
â”œâ”€â”€ reports/                        # QA Audit Outputs (HTML, PDF, Diffs, Screenshots)
â”‚   â”œâ”€â”€ diffs/                      # OpenCV Bounding Contour Heatmaps
â”‚   â””â”€â”€ screenshots/                # Desktop, Tablet, and Mobile Viewports
â”‚
â”œâ”€â”€ tests/                          # Automated Pytest Verification Suite
â”‚   â”œâ”€â”€ test_agent1.py              # Agent 1 Unit & Integration Tests
â”‚   â”œâ”€â”€ test_agent2.py              # Agent 2 OpenCV, Responsive, & Functional Tests
â”‚   â”œâ”€â”€ test_api.py                 # FastAPI Route Integration Tests
â”‚   â””â”€â”€ test_orchestrator.py        # Central Orchestrator Closed-Loop Test
â”‚
â”œâ”€â”€ docs/                           # Documentation
â”‚   â”œâ”€â”€ architecture.md             # In-depth System Architecture & Mermaid Diagrams
â”‚   â”œâ”€â”€ api_spec.md                 # REST API Specification
â”‚   â””â”€â”€ presentation_guide.md       # 5â€“10 Minute Technical Demonstration Script
â”‚
â”œâ”€â”€ requirements.txt                # Root Dependencies
â”œâ”€â”€ .env.example                    # Environment Variables Template
â””â”€â”€ README.md                       # Master Documentation
```

---

## 4. Quickstart Installation & Execution

### Prerequisites
- Python 3.10+ (Verified on Python 3.12.6)
- Node.js 18+ (for running the React Dashboard dev server)
- Git

### Step 1: Clone and Configure Environment
```bash
git clone https://github.com/your-username/AI-Agent-PoC.git
cd AI-Agent-PoC

# Create and activate virtual environment (optional but recommended)
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optional: Insert your `GEMINI_API_KEY`. If left empty, the system automatically runs in transparent deterministic test mode, executing real OpenCV, Playwright, and ReportLab engines without requiring external cloud credits).*

### Step 3: Run the Test Suite
Validate the complete system in seconds:
```bash
pytest tests/ -v
```
**Result**: 15/15 tests passing across Agent 1, Agent 2, FastAPI endpoints, and Orchestrator.

### Step 4: Launch the FastAPI Backend
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend API is now running at `http://127.0.0.1:8000`.
- Health Check: `http://127.0.0.1:8000/api/health`
- Live Astro Preview: `http://127.0.0.1:8000/api/preview/project_001`
- OpenAPI Swagger Docs: `http://127.0.0.1:8000/docs`

### Step 5: Launch the React Dashboard
In a new terminal window:
```bash
cd frontend/dashboard
npm install
npm run dev
```
Open your browser to `http://localhost:3000`.

---

## 5. End-to-End Technical Demonstration

Follow the step-by-step workflow detailed in [`docs/presentation_guide.md`](file:///C:/Users/sunda/OneDrive/Documents/AI-Agent-PoC/docs/presentation_guide.md):

1. **Dashboard Overview**: Review real-time metrics, target design verification (RDGCC.com), and the latest QA pass rate.
2. **Design Input**: Submit a screenshot or PDF. Click **Start Analysis & Generation**.
3. **Agent 1 Workspace**: Inspect extracted brand colors, typography scales, detected sections, and review modular Astro components (`Hero.astro`, `Sectors.astro`, `Contact.astro`) alongside decoupled Sanity schemas.
4. **Agent 2 Workspace**:
   - Compare the original RDGCC screenshot with the rendered Astro site using the **Split Slider** and **OpenCV Contour Heatmap**.
   - Toggle viewports across Desktop (1440Ã—900), Tablet (768Ã—1024), and Mobile (375Ã—812).
   - Inspect the Playwright functional assertion ledger.
5. **QA Reports**: Download the executive ReportLab PDF report and standalone HTML audit ledger.
6. **Agent Activity**: Review real-time event logs and the multi-iteration self-correction feedback loop.

---

## 6. Interview Assessment Deliverables Matrix

| Requirement | Implementation Module | Verification Status |
| :--- | :--- | :--- |
| **Agent 1: Modular Astro** | `backend/agents/agent1/generator.py` | Verified (11 Modular Files) |
| **Agent 1: Sanity Ready** | `backend/agents/agent1/sanity_schemas.py` | Verified (4 Schemas + `homepage.js`) |
| **Agent 2: Visual Testing** | `backend/agents/agent2/visual_diff.py` | Verified (OpenCV SSIM & Contours) |
| **Agent 2: Responsive Testing** | `backend/agents/agent2/responsive_tester.py` | Verified (Desktop, Tablet, Mobile) |
| **Agent 2: Functional Testing** | `backend/agents/agent2/functional_tester.py` | Verified (Playwright / DOM Assertions) |
| **Downloadable PDF Report** | `backend/services/pdf_service.py` | Verified (ReportLab PDF Generation) |
| **Multi-Agent Orchestrator** | `backend/orchestrator/pipeline.py` | Verified (Up to 3 Correction Loops) |
| **React Dashboard (6 Pages)** | `frontend/dashboard/src/pages/` | Verified (React + Vite + Tailwind) |
| **FastAPI REST API** | `backend/api/routes/` | Verified (Pydantic Typed Contracts) |
| **RDGCC Reference Design** | `uploads/rdgcc_reference.png` | Verified (Saudi / GCC Investment Holding) |
| **Automated Test Suite** | `tests/` | Verified (15/15 Pytest Passing) |

---

## 7. License
MIT License. Developed for technical assessment demonstration.

## By Thilak Ragav M

