"""
Unit and Integration Tests for Central Multi-Agent Orchestrator
"""
import pytest
import os
import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from backend.orchestrator.pipeline import CentralOrchestrator
from backend.orchestrator.state import orchestrator_state_manager
from backend.schemas.orchestrator_schema import OrchestratorRunState


def test_orchestrator_state_manager(tmp_path):
    """Verify OrchestratorStateManager creates, persists, and retrieves multi-agent run states."""
    run = orchestrator_state_manager.create_run(
        run_id="test_run_state_001",
        design_input_path="uploads/rdgcc_reference.png",
        max_iterations=3
    )

    assert run.run_id == "test_run_state_001"
    assert run.status == "INITIALIZED"
    assert run.current_iteration == 1

    # Update state
    run.status = "COMPLETED"
    orchestrator_state_manager.update_run(run)

    retrieved = orchestrator_state_manager.get_run("test_run_state_001")
    assert retrieved is not None
    assert retrieved.status == "COMPLETED"


def test_orchestrator_full_closed_loop():
    """
    Executes the complete multi-agent cycle:
    Agent 1 (Decomposition & Astro Gen) -> Agent 2 (Visual, Responsive, Functional QA) -> QA Report
    """
    ref_image = PROJECT_ROOT / "uploads" / "rdgcc_reference.png"
    orch = CentralOrchestrator()

    run_state = orch.execute_run(
        run_id="test_pipeline_e2e",
        file_path=str(ref_image),
        max_iterations=2
    )

    assert isinstance(run_state, OrchestratorRunState)
    assert run_state.status == "COMPLETED"
    assert run_state.design_analysis is not None
    assert len(run_state.manifest_history) >= 1
    assert len(run_state.qa_history) >= 1

    final_qa = run_state.qa_history[-1]
    assert final_qa.total_tests >= 10
    assert final_qa.passed_tests > 0
    assert final_qa.html_report_path is not None
    assert Path(final_qa.html_report_path).exists()
