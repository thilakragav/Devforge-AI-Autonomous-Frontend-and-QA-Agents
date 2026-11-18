"""
Agent 2 API Routes - QA & UI Testing Automation
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.schemas.agent2_schema import QAReport, QATestRequest
from backend.agents.agent2.visual_diff import VisualDiffTester
from backend.agents.agent2.responsive_tester import ResponsiveTester
from backend.agents.agent2.functional_tester import FunctionalTester
from backend.agents.agent2.playwright_driver import BrowserDriver
from backend.agents.agent2.report_generator import QAReportGenerator
from backend.services.astro_service import AstroService

router = APIRouter(prefix="/api/agent2", tags=["Agent 2"])

visual_tester = VisualDiffTester()
responsive_tester = ResponsiveTester()
functional_tester = FunctionalTester()
browser_driver = BrowserDriver()
report_generator = QAReportGenerator()
astro_service = AstroService()


@router.post("/test", response_model=QAReport)
def run_agent2_tests(req: QATestRequest):
    try:
        # 1. Capture viewports
        screenshots = browser_driver.capture_all_viewports(
            url=req.preview_url,
            project_id=req.project_id,
            iteration=req.iteration
        )

        # 2. Visual comparison
        desktop_shot = screenshots.get("Desktop", "")
        visual_metrics, visual_tcs = visual_tester.compare(
            reference_image_path=req.reference_image_path,
            generated_image_path=desktop_shot,
            project_id=req.project_id,
            iteration=req.iteration
        )

        # 3. Read rendered HTML
        proj_dir = astro_service.get_project_dir(req.project_id)
        preview_file = proj_dir / "public" / "preview.html"
        html_content = preview_file.read_text(encoding="utf-8") if preview_file.exists() else ""

        # 4. Responsive & functional
        resp_audits, resp_tcs = responsive_tester.audit_viewports(screenshots, html_content)
        func_tcs = functional_tester.run_tests(html_content, req.preview_url)

        # 5. Compile QA Report
        report = report_generator.build_report(
            project_id=req.project_id,
            iteration=req.iteration,
            test_cases=visual_tcs + resp_tcs + func_tcs,
            visual_metrics=visual_metrics,
            responsive_audits=resp_audits
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent 2 testing execution error: {str(e)}")
