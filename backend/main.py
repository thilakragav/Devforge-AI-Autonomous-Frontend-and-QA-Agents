"""
FastAPI Server - Multi-Agent AI System Backend
Autonomous Frontend Development & QA Testing Architecture
"""
import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import (
    upload_router,
    agent1_router,
    agent2_router,
    orchestrator_router,
    reports_router,
    preview_router,
)
from backend.services.llm_service import LLMService
from backend.services.astro_service import AstroService
from backend.agents.agent1.analyzer import DesignAnalyzer
from backend.agents.agent1.generator import AstroCodeGenerator
from backend.utils.logger import global_log_buffer

# Ensure directories exist
for folder in ["uploads", "reports/screenshots", "reports/diffs", "reports/state", "generated_projects"]:
    Path(folder).mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure baseline project_001 exists so developer can explore immediately
    global_log_buffer.log("SERVER", "SYSTEM", "FastAPI Multi-Agent Server initializing.")
    llm = LLMService()
    mode_info = llm.get_active_mode_info()
    global_log_buffer.log("SERVER", "SYSTEM", f"LLM Integration Mode: {mode_info['mode']} ({mode_info['provider']})")

    # Generate baseline project_001 on initial boot if not present
    astro_service = AstroService()
    baseline_dir = Path("generated_projects/project_001")
    if not baseline_dir.exists():
        global_log_buffer.log("STARTUP", "SYSTEM", "Pre-compiling baseline project_001 for immediate demonstration.")
        generator = AstroCodeGenerator()
        analysis = llm._get_rdgcc_reference_analysis(is_demo=not llm.is_live_available())
        manifest = generator.generate_project(
            analysis=analysis,
            project_id="project_001",
            version=1,
            output_directory="generated_projects/project_001"
        )
        astro_service.write_project_files(manifest)

    yield
    global_log_buffer.log("SERVER", "SYSTEM", "FastAPI server shutting down.")


app = FastAPI(
    title="Multi-Agent AI Frontend & QA Automation System",
    description="Autonomous collaborative AI agents: Design-to-Astro Code Generator and UI/QA Testing Agent.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration for React / Vite Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Directories for Dashboards & Visual Diff Inspection
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/reports/screenshots", StaticFiles(directory="reports/screenshots"), name="screenshots")
app.mount("/reports/diffs", StaticFiles(directory="reports/diffs"), name="diffs")

# Register API Routers
app.include_router(upload_router)
app.include_router(agent1_router)
app.include_router(agent2_router)
app.include_router(orchestrator_router)
app.include_router(reports_router)
app.include_router(preview_router)


@app.get("/api/health")
def health_check():
    llm = LLMService()
    mode_info = llm.get_active_mode_info()
    return {
        "status": "online",
        "service": "Multi-Agent PoC Backend",
        "ai_engine": mode_info,
        "active_agents": ["Agent 1 (Design-to-Astro)", "Agent 2 (UI & QA Testing)"],
        "orchestrator_state": "ready"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("backend.main:app", host="127.0.0.1", port=port, reload=True)
