"""
Unit and Integration Tests for Agent 2 - UI and QA Testing Agent
"""
import pytest
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from backend.agents.agent2.visual_diff import VisualDiffTester, compute_opencv_ssim
from backend.agents.agent2.responsive_tester import ResponsiveTester
from backend.agents.agent2.functional_tester import FunctionalTester
from backend.agents.agent2.report_generator import QAReportGenerator
from backend.agents.agent2.playwright_driver import BrowserDriver
from backend.schemas.agent2_schema import TestSeverity, TestCategory


def test_visual_diff_opencv_ssim_and_contours(tmp_path):
    """Verify OpenCV measurable difference: SSIM calculation, pixel delta, and diff overlay generation."""
    ref_image = PROJECT_ROOT / "uploads" / "rdgcc_reference.png"
    assert ref_image.exists()

    vt = VisualDiffTester(output_dir=str(tmp_path))
    metrics, test_cases = vt.compare(
        reference_image_path=str(ref_image),
        generated_image_path=str(ref_image),
        project_id="test_vis",
        iteration=1
    )

    # Identical images should have SSIM ~ 1.0 and 0% pixel diff
    assert metrics.ssim_score >= 0.99
    assert metrics.pixel_diff_percentage == 0.0
    assert Path(metrics.diff_image_path).exists()
    assert len(test_cases) == 3
    assert all(tc.passed for tc in test_cases)


def test_responsive_layout_tester():
    """Verify responsive tester evaluates Desktop (1440x900), Tablet (768x1024), and Mobile (375x812)."""
    rt = ResponsiveTester()
    sample_html = """
    <html>
      <body style="overflow-x: hidden;">
        <nav class="hidden md:flex">Desktop Links</nav>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
          <div>Card 1</div>
          <div>Card 2</div>
        </div>
      </body>
    </html>
    """
    mock_shots = {
        "Desktop": "shot_desk.png",
        "Tablet": "shot_tab.png",
        "Mobile": "shot_mob.png",
    }

    audits, test_cases = rt.audit_viewports(mock_shots, sample_html)

    assert len(audits) == 3
    assert any(a.device == "Desktop" for a in audits)
    assert any(a.device == "Tablet" for a in audits)
    assert any(a.device == "Mobile" for a in audits)
    assert len(test_cases) == 3
    assert all(tc.passed for tc in test_cases)


def test_functional_dom_tester():
    """Verify functional tester inspects actual DOM elements for navigation, buttons, forms, and images."""
    ft = FunctionalTester()
    html_sample = """
    <!DOCTYPE html>
    <html>
      <head><title>RDGCC Corporate Website</title></head>
      <body>
        <a href="#about">About</a>
        <a href="#sectors">Sectors</a>
        <button type="button" aria-label="Language Selector">EN</button>
        <form>
          <input type="text" name="name" required />
          <input type="email" name="email" required />
          <button type="submit">Submit</button>
        </form>
        <img src="/logo.svg" alt="RDGCC Brand Logo" />
        <h1>Empowering Regional Excellence</h1>
        <h2>Strategic Business Sectors</h2>
      </body>
    </html>
    """

    test_cases = ft.run_tests(html_sample, "http://localhost:8000/api/preview/test")

    assert len(test_cases) == 6
    # Check individual IDs
    t_ids = [tc.test_id for tc in test_cases]
    assert "FUNC-001" in t_ids  # Title
    assert "FUNC-002" in t_ids  # Nav links
    assert "FUNC-003" in t_ids  # Button
    assert "FUNC-004" in t_ids  # Form
    assert "FUNC-005" in t_ids  # Image alt
    assert "FUNC-006" in t_ids  # Heading hierarchy
    assert all(tc.passed for tc in test_cases)


def test_qa_report_generator_html_and_pdf(tmp_path):
    """Verify Agent 2 compiles structured QAReport, HTML ledger, and ReportLab PDF."""
    rg = QAReportGenerator(reports_dir=str(tmp_path))
    ft = FunctionalTester()
    html_sample = "<!DOCTYPE html><html><head><title>RDGCC</title></head><body><h1>Title</h1><h2>Subtitle</h2></body></html>"
    tcs = ft.run_tests(html_sample, "http://localhost:8000")

    report = rg.build_report(
        project_id="test_report_gen",
        iteration=1,
        test_cases=tcs,
        visual_metrics=None,
        responsive_audits=[]
    )

    assert report.total_tests == len(tcs)
    assert Path(report.html_report_path).exists()
    assert Path(report.pdf_report_path).exists()
    assert report.pdf_report_path.endswith(".pdf")
    assert Path(report.pdf_report_path).stat().st_size > 1000
