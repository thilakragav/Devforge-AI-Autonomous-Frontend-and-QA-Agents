# Technical Interview Demonstration Guide (5–10 Minutes)

## Multi-Agent AI System for Automated Frontend Development & QA Testing

---

### Demonstration Overview & Timing
- **Duration**: 5–10 minutes
- **Target Persona**: Technical Interviewers, Lead Architects, Head of Engineering
- **Core Message**: A production-grade multi-agent system where Agent 1 develops modular Astro components from design specifications, Agent 2 validates visual, responsive, and functional health, and the Central Orchestrator drives an autonomous self-correction loop.

---

### Step-by-Step Demonstration Script

#### 1. System Overview & Architecture (1 Minute)
- **Action**: Open the React Dashboard at `http://localhost:3000` (or `Dashboard.tsx`).
- **Talking Points**:
  - "Welcome. We have developed a complete Proof of Concept featuring two autonomous collaborative agents coordinated by a central Python orchestrator."
  - "The target reference is RDGCC.com, a prestigious GCC industrial and regional development portal."
  - "The stack combines React, TypeScript, and Tailwind on the dashboard; FastAPI, Pydantic, OpenCV, and Playwright on the backend; and Astro 4.x with Sanity CMS readiness for the generated code."

#### 2. Design Ingestion & Agent 1 Decomposition (2 Minutes)
- **Action**: Navigate to **Design Input** tab. Show the uploaded RDGCC reference design. Click **Start Analysis & Generation** (or show Agent 1 Workspace).
- **Talking Points**:
  - "Agent 1 ingests PNG, JPG, PDF documents (with PyMuPDF page rasterization), or Figma URLs."
  - "In the **Agent 1 Workspace**, notice the semantic decomposition: brand identity, extracted color palette (`#0A192F` corporate navy, `#C29B38` accent gold), typography scales, and 8 discrete sections."
  - "Crucially, Agent 1 does NOT generate a monolithic single HTML file. In the Code Viewer, you can see modular Astro components: `Header.astro`, `Hero.astro`, `About.astro`, `Sectors.astro`, `Stats.astro`, `Projects.astro`, `Contact.astro`, and `Footer.astro`."
  - "Content is separated into `src/data/homepage.js`, and Sanity CMS schemas (`homepage.js`, `sector.js`) are ready for editorial decoupling."

#### 3. Agent 2: UI & QA Testing Execution (2.5 Minutes)
- **Action**: Navigate to **Agent 2 Workspace**.
- **Talking Points**:
  - "Once the website is rendered, Agent 2 takes over like an automated QA engineer across three distinct testing tiers."
  - **Visual Testing**: Show the **Side-by-Side** and **Split Slider** comparison, as well as the **OpenCV Heatmap**.
    - "We compute measurable Structural Similarity (SSIM index) and pixel delta percentage using OpenCV, highlighting discrepancy regions with bounding contours."
  - **Responsive Testing**: Switch between Desktop (1440×900), Tablet (768×1024), and Mobile (375×812) viewports.
    - "Notice the live responsive iframe. Agent 2 checks for horizontal scroll overflow, text truncation, and navigation collapse."
  - **Functional Testing**: Show the Playwright DOM ledger.
    - "Every test is executed against real elements: anchor links, interactive buttons with accessibility labels, corporate form inputs, and image alt tags. Never marking an unexecuted test as passed."

#### 4. Orchestration & Self-Correction Feedback Loop (2 Minutes)
- **Action**: Navigate to **Agent Activity** tab.
- **Talking Points**:
  - "Here is the heart of the system: the autonomous feedback loop."
  - "When Agent 2 identifies an issue (such as mobile container overflow or headline typography scaling), the Orchestrator translates the failed test into a typed `CorrectionDirective`."
  - "Agent 1's Refactorer receives the directive and applies surgical modifications *only* to the affected components without regenerating the entire website, producing versioned manifests (`v1` $\to$ `v2` $\to$ `v3`)."
  - "Review the live event log console with severity badges and timestamps."

#### 5. Executive Compliance Reports (1.5 Minutes)
- **Action**: Navigate to **QA Reports** tab. Click **Download Official PDF**.
- **Talking Points**:
  - "The system produces both an interactive HTML compliance report and an executive-grade PDF generated via ReportLab."
  - "Open the PDF to show the clean corporate branding, executive metrics grid, visual SSIM scores, full test ledger, and actionable recommendations."

---

### Key Questions & Defensive Talking Points

1. **Why Astro instead of standard React or plain HTML?**
   - "Astro provides zero-JS by default, ultra-fast static loading, and modular component isolation ideal for content-rich corporate holding portals like RDGCC."
2. **How does the system handle missing API keys?**
   - "The system adheres strictly to the rule: *Never fabricate results*. If no API key is provided, the backend operates in an explicitly labelled deterministic demonstration mode that exercises the real OpenCV engine, real Playwright browser driver, real modular Astro compiler, and real ReportLab PDF generator."
3. **Is the system IDE-independent?**
   - "Yes. The codebase contains standard Python and TypeScript code. It can be opened and executed in Cursor, VS Code, or purely via terminal PowerShell scripts."
