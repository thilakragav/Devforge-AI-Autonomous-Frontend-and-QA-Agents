"""
Agent 2 Pydantic Schemas - UI and QA Testing Agent
"""
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class TestSeverity(str, Enum):
    __test__ = False
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class TestCategory(str, Enum):
    __test__ = False
    VISUAL = "VISUAL"
    RESPONSIVE = "RESPONSIVE"
    FUNCTIONAL = "FUNCTIONAL"


class TestCaseResult(BaseModel):
    __test__ = False
    test_id: str = Field(..., description="Unique identifier (e.g. VIS-001, RESP-002, FUNC-003)")
    category: TestCategory
    description: str = Field(..., description="What was tested")
    expected_result: str
    actual_result: str
    passed: bool
    severity: TestSeverity
    issue_description: Optional[str] = None
    recommendation: Optional[str] = None
    affected_component: Optional[str] = None
    screenshot_path: Optional[str] = None


class VisualDiffMetrics(BaseModel):
    ssim_score: float = Field(..., description="Structural Similarity Index (-1.0 to 1.0)")
    pixel_diff_percentage: float = Field(..., description="Percentage of non-matching pixels")
    mismatched_pixel_count: int = Field(default=0)
    diff_image_path: str = Field(..., description="Path to visual diff heatmap or contour overlay")
    reference_image_path: str
    generated_image_path: str
    llm_visual_critique: str = Field(default="", description="Multimodal LLM qualitative analysis")


class ViewportAudit(BaseModel):
    device: str = Field(..., description="e.g. Desktop, Tablet, Mobile")
    viewport: str = Field(..., description="e.g. 1440x900, 768x1024, 375x812")
    screenshot_path: str
    horizontal_overflow: bool = False
    text_overflow_detected: bool = False
    navigation_broken: bool = False
    issues: List[str] = Field(default_factory=list)


class QAReport(BaseModel):
    project_id: str
    iteration: int = Field(default=1)
    timestamp: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    critical_issues_count: int
    high_issues_count: int
    overall_status: str = Field(default="PASSED", description="PASSED, FAILED_NEEDS_CORRECTION, ACCEPTED_WITH_WARNINGS")
    test_cases: List[TestCaseResult] = Field(default_factory=list)
    visual_metrics: Optional[VisualDiffMetrics] = None
    responsive_audits: List[ViewportAudit] = Field(default_factory=list)
    html_report_path: Optional[str] = None
    pdf_report_path: Optional[str] = None
    recommendations_summary: List[str] = Field(default_factory=list)


class QATestRequest(BaseModel):
    project_id: str
    iteration: int = 1
    preview_url: str
    reference_image_path: str
    demo_mode: bool = False
