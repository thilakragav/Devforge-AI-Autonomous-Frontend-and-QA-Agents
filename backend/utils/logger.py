"""
Centralized Logger for Multi-Agent System
"""
import logging
import sys
from datetime import datetime
from typing import List
from backend.schemas.orchestrator_schema import RunStepLog

# Configure console logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("MultiAgentPoC")


class AgentLogBuffer:
    """Thread-safe in-memory log buffer for streaming to dashboard and orchestrator state."""
    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self._entries: List[RunStepLog] = []

    def log(self, stage: str, agent: str, message: str, level: str = "INFO") -> RunStepLog:
        entry = RunStepLog(
            timestamp=datetime.utcnow().isoformat(),
            stage=stage,
            agent=agent,
            message=message,
            level=level
        )
        self._entries.append(entry)
        if len(self._entries) > self.max_entries:
            self._entries.pop(0)

        # Also emit to Python logging
        log_level = getattr(logging, level.upper(), logging.INFO)
        logger.log(log_level, f"[{agent}][{stage}] {message}")
        return entry

    def get_logs(self) -> List[RunStepLog]:
        return list(self._entries)

    def clear(self):
        self._entries.clear()


global_log_buffer = AgentLogBuffer()
