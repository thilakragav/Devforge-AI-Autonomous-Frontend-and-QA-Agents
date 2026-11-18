"""
Orchestrator State Manager
Maintains in-memory run states and persists execution history.
"""
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path
import json

from backend.schemas.orchestrator_schema import OrchestratorRunState, RunStepLog
from backend.utils.logger import global_log_buffer


class OrchestratorStateManager:
    def __init__(self, storage_dir: str = "reports/state"):
        self.storage_dir = Path(storage_dir).resolve()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._runs: Dict[str, OrchestratorRunState] = {}

    def create_run(self, run_id: str, design_input_path: str = "", figma_url: Optional[str] = None, max_iterations: int = 3) -> OrchestratorRunState:
        state = OrchestratorRunState(
            run_id=run_id,
            status="INITIALIZED",
            current_iteration=1,
            max_iterations=max_iterations,
            design_input_path=design_input_path,
            figma_url=figma_url,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat(),
            logs=global_log_buffer.get_logs()
        )
        self._runs[run_id] = state
        self.save_to_disk(run_id)
        return state

    def get_run(self, run_id: str) -> Optional[OrchestratorRunState]:
        if run_id in self._runs:
            # Refresh logs from global buffer
            self._runs[run_id].logs = global_log_buffer.get_logs()
            return self._runs[run_id]

        # Try loading from disk
        file_path = self.storage_dir / f"{run_id}.json"
        if file_path.exists():
            data = json.loads(file_path.read_text(encoding="utf-8"))
            state = OrchestratorRunState(**data)
            self._runs[run_id] = state
            return state

        return None

    def update_run(self, state: OrchestratorRunState):
        state.updated_at = datetime.utcnow().isoformat()
        state.logs = global_log_buffer.get_logs()
        self._runs[state.run_id] = state
        self.save_to_disk(state.run_id)

    def save_to_disk(self, run_id: str):
        if run_id in self._runs:
            file_path = self.storage_dir / f"{run_id}.json"
            file_path.write_text(self._runs[run_id].model_dump_json(indent=2), encoding="utf-8")

    def list_runs(self) -> List[OrchestratorRunState]:
        return list(self._runs.values())


orchestrator_state_manager = OrchestratorStateManager()
