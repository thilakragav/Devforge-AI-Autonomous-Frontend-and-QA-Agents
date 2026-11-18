# API Specification: Multi-Agent AI System Backend

Base URL: `http://localhost:8000/api`

---

## 1. System Health
- **Endpoint**: `GET /api/health`
- **Description**: Returns engine health, active AI provider mode, and agent statuses.
- **Response**:
```json
{
  "status": "online",
  "service": "Multi-Agent PoC Backend",
  "ai_engine": {
    "mode": "DEMO_DETERMINISTIC",
    "provider": "builtin-heuristic-engine",
    "notice": "Operating in clearly labelled deterministic test mode."
  },
  "active_agents": ["Agent 1 (Design-to-Astro)", "Agent 2 (UI & QA Testing)"],
  "orchestrator_state": "ready"
}
```

---

## 2. Design Ingestion
- **Endpoint**: `POST /api/upload`
- **Description**: Uploads a design asset (PNG, JPG, PDF) encoded in base64.
- **Request Body**:
```json
{
  "filename": "rdgcc_mockup.pdf",
  "content_b64": "<base64 string>",
  "project_name": "RDGCC Corporate Website"
}
```
- **Response**:
```json
{
  "status": "success",
  "filename": "rdgcc_mockup.pdf",
  "saved_path": "uploads/rdgcc_mockup.pdf",
  "preview_image": "uploads/rdgcc_mockup_page_1.png"
}
```

---

## 3. Agent 1 Endpoints
- **Endpoint**: `POST /api/agent1/analyze`
  - Decomposes design into structured JSON tokens and sections.
- **Endpoint**: `POST /api/agent1/generate`
  - Synthesizes modular Astro components, structured data, and Sanity schemas.
- **Endpoint**: `GET /api/agent1/projects/{project_id}`
  - Returns inventory of generated Astro components and validation status.

---

## 4. Agent 2 Endpoints
- **Endpoint**: `POST /api/agent2/test`
  - Runs visual difference, responsive viewports, and functional test suite.
- **Request Body**:
```json
{
  "project_id": "project_001",
  "preview_url": "http://127.0.0.1:8000/api/preview/project_001",
  "reference_image_path": "uploads/rdgcc_reference.png",
  "iteration": 1
}
```

---

## 5. Orchestrator Endpoints
- **Endpoint**: `POST /api/orchestrator/run`
  - Starts asynchronous multi-agent orchestration pipeline.
- **Endpoint**: `GET /api/orchestrator/status/{run_id}`
  - Polls run state, current iteration, manifests, and QA history.
- **Endpoint**: `GET /api/orchestrator/runs`
  - Lists all past execution runs.
- **Endpoint**: `GET /api/orchestrator/logs`
  - Retrieves real-time event log buffer.

---

## 6. Reports & Previews
- **Endpoint**: `GET /api/preview/{project_id}`
  - Serves compiled HTML preview for browser testing and dashboard iframe.
- **Endpoint**: `GET /api/reports/{project_id}`
  - Retrieves structured JSON QA report.
- **Endpoint**: `GET /api/reports/{project_id}/download?format=pdf`
  - Downloads ReportLab executive QA PDF audit report.
- **Endpoint**: `GET /api/reports/{project_id}/download?format=html`
  - Downloads standalone HTML report.
