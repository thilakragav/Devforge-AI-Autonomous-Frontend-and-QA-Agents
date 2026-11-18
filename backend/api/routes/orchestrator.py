"""
Orchestrator API Routes - Multi-Agent Coordination & Pipeline Execution
"""
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from backend.schemas.orchestrator_schema import (
    OrchestratorTriggerRequest,
    OrchestratorRunState,
)
from backend.orchestrator.pipeline import CentralOrchestrator
from backend.orchestrator.state import orchestrator_state_manager
from backend.utils.logger import global_log_buffer

router = APIRouter(prefix="/api/orchestrator", tags=["Orchestrator"])
orchestrator = CentralOrchestrator()


@router.post("/run", response_model=OrchestratorRunState)
async def trigger_orchestrator_run(req: OrchestratorTriggerRequest, background_tasks: BackgroundTasks):
    try:
        import uuid
        run_id = f"run_{uuid.uuid4().hex[:8]}"

        # Initialize run state synchronously so client has immediate handle
        state = orchestrator_state_manager.create_run(
            run_id=run_id,
            design_input_path=req.file_path or "",
            figma_url=req.figma_url,
            max_iterations=req.max_iterations
        )

        # Run background execution
        background_tasks.add_task(
            orchestrator.execute_run,
            run_id=run_id,
            file_path=req.file_path,
            figma_url=req.figma_url,
            max_iterations=req.max_iterations
        )

        return state
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to launch orchestrator: {str(e)}")


@router.get("/status/{run_id}", response_model=OrchestratorRunState)
async def get_orchestrator_status(run_id: str):
    state = orchestrator_state_manager.get_run(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return state


@router.get("/runs")
async def list_orchestrator_runs():
    return orchestrator_state_manager.list_runs()


@router.get("/logs")
async def get_system_logs():
    return global_log_buffer.get_logs()
