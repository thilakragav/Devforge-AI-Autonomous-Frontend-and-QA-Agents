"""
Orchestrator Pydantic Schemas - Central Pipeline & Multi-Agent State
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from backend.schemas.agent1_schema import AstroProjectManifest, DesignAnalysisResult
from backend.schemas.agent2_schema import QAReport


class CorrectionDirective(BaseModel):
    iteration: int
    target_components: List[str] = Field(default_factory=list)
    specific_issues: List[str] = Field(default_factory=list)
    actionable_instructions: List[str] = Field(default_factory=list)


class RunStepLog(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    stage: str
    agent: str  # "ORCHESTRATOR", "AGENT_1", "AGENT_2", "SYSTEM"
    message: str
    level: str = "INFO"  # "INFO", "WARNING", "ERROR", "SUCCESS"


class OrchestratorRunState(BaseModel):
    run_id: str
    project_name: str = "RDGCC Corporate Website"
    status: str = "IDLE"  # IDLE, ANALYZING, GENERATING, BUILDING, SERVING, TESTING, REFACTORING, COMPLETED, FAILED
    current_iteration: int = 1
    max_iterations: int = 3
    design_input_path: str = ""
    figma_url: Optional[str] = None
    design_analysis: Optional[DesignAnalysisResult] = None
    manifest_history: List[AstroProjectManifest] = Field(default_factory=list)
    qa_history: List[QAReport] = Field(default_factory=list)
    correction_history: List[CorrectionDirective] = Field(default_factory=list)
    logs: List[RunStepLog] = Field(default_factory=list)
    preview_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class OrchestratorTriggerRequest(BaseModel):
    file_path: Optional[str] = None
    figma_url: Optional[str] = None
    project_name: Optional[str] = "RDGCC Corporate Website"
    max_iterations: int = 3
    demo_mode: bool = False
