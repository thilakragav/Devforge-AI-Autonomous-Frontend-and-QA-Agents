"""
Agent 2 - QA Report Generator
Assembles structured QAReport, interactive HTML reports, and executive PDF reports.
"""
import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from backend.schemas.agent2_schema import (
    QAReport,
    TestCaseResult,
    VisualDiffMetrics,
    ViewportAudit,
    TestSeverity,
)
from backend.services.pdf_service import PDFService
from backend.utils.logger import global_log_buffer


class QAReportGenerator:
    def __init__(self, reports_dir: str = "reports", pdf_service: Optional[PDFService] = None):
        self.reports_dir = Path(reports_dir).resolve()
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_service = pdf_service or PDFService(output_dir=str(self.reports_dir))

    def build_report(
        self,
        project_id: str,
        iteration: int,
        test_cases: List[TestCaseResult],
        visual_metrics: Optional[VisualDiffMetrics] = None,
        responsive_audits: List[ViewportAudit] = None
    ) -> QAReport:
        """
        Compiles all test case results into a structured QAReport.
        Generates downloadable HTML and PDF representations.
        """
        responsive_audits = responsive_audits or []
        total = len(test_cases)
        passed = sum(1 for tc in test_cases if tc.passed)
        failed = total - passed
        critical = sum(1 for tc in test_cases if not tc.passed and tc.severity == TestSeverity.CRITICAL)
        high = sum(1 for tc in test_cases if not tc.passed and tc.severity == TestSeverity.HIGH)

        if critical > 0 or high > 0:
            status = "FAILED_NEEDS_CORRECTION"
        elif failed > 0:
            status = "ACCEPTED_WITH_WARNINGS"
        else:
            status = "PASSED"

        # Formulate actionable recommendations
        recs: List[str] = []
        for tc in test_cases:
            if not tc.passed and tc.recommendation and tc.recommendation not in recs:
                recs.append(f"[{tc.test_id}] {tc.recommendation}")

        if not recs:
            recs.append("All structural, responsive, and functional test criteria satisfied with zero critical regressions.")

        report = QAReport(
            project_id=project_id,
            iteration=iteration,
            timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            total_tests=total,
            passed_tests=passed,
            failed_tests=failed,
            critical_issues_count=critical,
            high_issues_count=high,
            overall_status=status,
            test_cases=test_cases,
            visual_metrics=visual_metrics,
            responsive_audits=responsive_audits,
            recommendations_summary=recs
        )

        # 1. Generate HTML Report
        html_path = self._generate_html_report(report)
        report.html_report_path = str(html_path)

        # 2. Generate PDF Report via ReportLab
        try:
            pdf_path = self.pdf_service.generate_qa_pdf(report)
            report.pdf_report_path = str(pdf_path)
        except Exception as e:
            global_log_buffer.log("REPORT_GEN", "AGENT_2", f"PDF generation warning: {e}", "WARNING")

        # 3. Save JSON Report
        json_path = self.reports_dir / f"QA_Report_{project_id}_v{iteration}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))

        global_log_buffer.log(
            "REPORT_GEN",
            "AGENT_2",
            f"Generated QA Report: {total} tests ({passed} passed, {failed} failed, {critical} critical). HTML: {Path(html_path).name}"
        )

        return report

    def _generate_html_report(self, report: QAReport) -> str:
        out_path = self.reports_dir / f"QA_Report_{report.project_id}_v{report.iteration}.html"

        rows_html = ""
        for tc in report.test_cases:
            badge_class = "bg-green-100 text-green-800" if tc.passed else "bg-red-100 text-red-800"
            sev_class = "text-red-600 font-bold" if tc.severity in (TestSeverity.CRITICAL, TestSeverity.HIGH) else "text-slate-600"
            rows_html += f"""
            <tr class="border-b border-slate-100 hover:bg-slate-50 transition">
              <td class="py-3 px-4 font-mono text-xs font-semibold">{tc.test_id}</td>
              <td class="py-3 px-4 text-xs font-medium text-slate-500 uppercase">{tc.category.value}</td>
              <td class="py-3 px-4 text-xs font-medium text-slate-800">{tc.description}</td>
              <td class="py-3 px-4 text-xs"><span class="px-2 py-0.5 rounded text-[11px] font-bold {badge_class}">{"PASS" if tc.passed else "FAIL"}</span></td>
              <td class="py-3 px-4 text-xs {sev_class}">{tc.severity.value}</td>
              <td class="py-3 px-4 text-xs text-slate-600">{tc.actual_result}</td>
              <td class="py-3 px-4 text-xs text-slate-500 italic">{tc.recommendation or tc.issue_description or "-"}</td>
            </tr>
            """

        recs_html = "".join([f"<li class='text-xs text-slate-700 mb-1.5'>• {r}</li>" for r in report.recommendations_summary])

        ssim_display = f"{report.visual_metrics.ssim_score:.4f}" if report.visual_metrics else "N/A"
        pixel_diff_display = f"{report.visual_metrics.pixel_diff_percentage:.2f}%" if report.visual_metrics else "N/A"

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>QA Report - {report.project_id} (Iteration {report.iteration})</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3, h4 {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 p-6 md:p-12">
  <div class="max-w-6xl mx-auto space-y-8">
    
    <!-- Header Banner -->
    <div class="bg-[#0A192F] text-white p-8 rounded-2xl shadow-lg border border-slate-800 flex flex-col md:flex-row md:items-center justify-between">
      <div>
        <div class="inline-block px-3 py-1 rounded bg-[#C29B38] text-white text-xs font-bold tracking-wider uppercase mb-3">
          Agent 2 QA Audit
        </div>
        <h1 class="text-3xl font-extrabold tracking-tight text-white mb-2">
          Quality Assurance & UI Verification Report
        </h1>
        <p class="text-slate-300 text-xs">
          Project: <b>{report.project_id}</b> | Iteration: <b>v{report.iteration}</b> | Timestamp: {report.timestamp}
        </p>
      </div>
      <div class="mt-6 md:mt-0 text-right">
        <span class="inline-block px-4 py-2 rounded-xl text-sm font-bold { 'bg-green-500/20 text-green-300 border border-green-500/40' if report.overall_status == 'PASSED' else 'bg-red-500/20 text-red-300 border border-red-500/40'}">
          {report.overall_status}
        </span>
      </div>
    </div>

    <!-- Executive Metrics Grid -->
    <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-center">
        <span class="text-xs uppercase font-bold text-slate-400 block mb-1">Total Tests</span>
        <span class="text-3xl font-extrabold text-[#0A192F]">{report.total_tests}</span>
      </div>
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-center">
        <span class="text-xs uppercase font-bold text-slate-400 block mb-1">Passed</span>
        <span class="text-3xl font-extrabold text-green-600">{report.passed_tests}</span>
      </div>
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-center">
        <span class="text-xs uppercase font-bold text-slate-400 block mb-1">Failed</span>
        <span class="text-3xl font-extrabold text-red-600">{report.failed_tests}</span>
      </div>
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-center">
        <span class="text-xs uppercase font-bold text-slate-400 block mb-1">Critical Issues</span>
        <span class="text-3xl font-extrabold text-red-600">{report.critical_issues_count}</span>
      </div>
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-center">
        <span class="text-xs uppercase font-bold text-slate-400 block mb-1">Visual SSIM</span>
        <span class="text-3xl font-extrabold text-[#C29B38]">{ssim_display}</span>
      </div>
    </div>

    <!-- Recommendations -->
    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <h2 class="text-lg font-bold text-[#0A192F] mb-3">Key Recommendations & Agent Feedback</h2>
      <ul class="space-y-1 list-none pl-0">
        {recs_html}
      </ul>
    </div>

    <!-- Test Cases Table -->
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="p-6 border-b border-slate-200">
        <h2 class="text-lg font-bold text-[#0A192F]">Detailed Test Execution Ledger</h2>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-slate-500 uppercase text-[11px] font-bold">
              <th class="py-3 px-4">Test ID</th>
              <th class="py-3 px-4">Category</th>
              <th class="py-3 px-4">Description</th>
              <th class="py-3 px-4">Status</th>
              <th class="py-3 px-4">Severity</th>
              <th class="py-3 px-4">Observed Result</th>
              <th class="py-3 px-4">Recommendation</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </div>
    </div>

  </div>
</body>
</html>"""
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(out_path)
