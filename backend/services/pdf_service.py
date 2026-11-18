"""
PDF Service - Generates Executive QA Reports using ReportLab
"""
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from backend.schemas.agent2_schema import QAReport, TestSeverity
from backend.utils.logger import global_log_buffer


class PDFService:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_qa_pdf(self, report: QAReport) -> str:
        """
        Creates an executive-grade PDF QA audit report.
        Returns the absolute path to the generated PDF.
        """
        filename = f"QA_Report_{report.project_id}_v{report.iteration}_{int(datetime.now(timezone.utc).timestamp())}.pdf"
        file_path = self.output_dir / filename

        doc = SimpleDocTemplate(
            str(file_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom corporate palette
        NAVY = colors.HexColor("#0A192F")
        GOLD = colors.HexColor("#C29B38")
        SLATE = colors.HexColor("#334155")
        LIGHT_BG = colors.HexColor("#F8FAFC")
        BORDER = colors.HexColor("#E2E8F0")
        PASS_GREEN = colors.HexColor("#16A34A")
        FAIL_RED = colors.HexColor("#DC2626")

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=NAVY
        )

        subtitle_style = ParagraphStyle(
            'DocSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=SLATE
        )

        heading2_style = ParagraphStyle(
            'Heading2_Custom',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=17,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=6
        )

        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            textColor=colors.white
        )

        table_body_style = ParagraphStyle(
            'TableBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=7.5,
            leading=10,
            textColor=SLATE
        )

        story = []

        # 1. Header & Title Banner
        story.append(Paragraph(f"AGENT 2: QA & UI VERIFICATION REPORT", title_style))
        story.append(Paragraph(
            f"Project: <b>{report.project_id}</b> | Iteration: <b>v{report.iteration}</b> | Generated: {report.timestamp} | Status: <b>{report.overall_status}</b>",
            subtitle_style
        ))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=14))

        # 2. Executive Metrics Summary Table
        metrics_data = [
            [
                Paragraph("<b>Total Test Cases</b>", subtitle_style),
                Paragraph("<b>Passed</b>", subtitle_style),
                Paragraph("<b>Failed</b>", subtitle_style),
                Paragraph("<b>Critical Issues</b>", subtitle_style),
                Paragraph("<b>Visual SSIM</b>", subtitle_style),
            ],
            [
                Paragraph(f"<font size=14 color='{NAVY.hexval()}'><b>{report.total_tests}</b></font>", subtitle_style),
                Paragraph(f"<font size=14 color='{PASS_GREEN.hexval()}'><b>{report.passed_tests}</b></font>", subtitle_style),
                Paragraph(f"<font size=14 color='{FAIL_RED.hexval()}'><b>{report.failed_tests}</b></font>", subtitle_style),
                Paragraph(f"<font size=14 color='{FAIL_RED.hexval()}'><b>{report.critical_issues_count}</b></font>", subtitle_style),
                Paragraph(f"<font size=14 color='{GOLD.hexval()}'><b>{f'{report.visual_metrics.ssim_score:.3f}' if report.visual_metrics else 'N/A'}</b></font>", subtitle_style),
            ]
        ]
        metrics_table = Table(metrics_data, colWidths=[108, 108, 108, 108, 108])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
            ('BOX', (0, 0), (-1, -1), 1, BORDER),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(metrics_table)
        story.append(Spacer(1, 14))

        # 3. Visual & Responsive Section
        story.append(Paragraph("1. Measurable Visual & Responsive Testing", heading2_style))
        if report.visual_metrics:
            vm = report.visual_metrics
            critique = vm.llm_visual_critique or "Visual comparison executed via OpenCV SSIM and contour difference analysis."
            story.append(Paragraph(
                f"<b>OpenCV Metrics:</b> SSIM Index: <b>{vm.ssim_score:.4f}</b> | "
                f"Pixel Discrepancy: <b>{vm.pixel_diff_percentage:.2f}%</b> | "
                f"Mismatched Pixels: <b>{vm.mismatched_pixel_count:,}</b>",
                table_body_style
            ))
            story.append(Spacer(1, 4))
            story.append(Paragraph(f"<b>Vision LLM Analysis:</b> {critique}", table_body_style))
            story.append(Spacer(1, 8))

        if report.responsive_audits:
            resp_data = [
                [Paragraph("Device", table_header_style), Paragraph("Viewport", table_header_style), Paragraph("Horizontal Overflow", table_header_style), Paragraph("Layout Broken", table_header_style), Paragraph("Observed Status", table_header_style)]
            ]
            for aud in report.responsive_audits:
                resp_data.append([
                    Paragraph(aud.device, table_body_style),
                    Paragraph(aud.viewport, table_body_style),
                    Paragraph("No (Passed)" if not aud.horizontal_overflow else "<font color=red>Yes (Failed)</font>", table_body_style),
                    Paragraph("No (Passed)" if not aud.text_overflow_detected else "<font color=red>Yes (Failed)</font>", table_body_style),
                    Paragraph("Pass" if not aud.issues else "; ".join(aud.issues), table_body_style),
                ])
            resp_table = Table(resp_data, colWidths=[90, 80, 110, 110, 150])
            resp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), NAVY),
                ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(resp_table)
            story.append(Spacer(1, 14))

        # 4. Detailed Test Case Audit Table
        story.append(Paragraph("2. Functional & Visual Test Case Execution Audit", heading2_style))
        test_rows = [
            [
                Paragraph("Test ID", table_header_style),
                Paragraph("Category", table_header_style),
                Paragraph("Description", table_header_style),
                Paragraph("Status", table_header_style),
                Paragraph("Severity", table_header_style),
                Paragraph("Recommendation / Notes", table_header_style)
            ]
        ]

        for tc in report.test_cases:
            status_text = f"<font color='{PASS_GREEN.hexval()}'><b>PASS</b></font>" if tc.passed else f"<font color='{FAIL_RED.hexval()}'><b>FAIL</b></font>"
            sev_color = FAIL_RED.hexval() if tc.severity in (TestSeverity.CRITICAL, TestSeverity.HIGH) else SLATE.hexval()
            test_rows.append([
                Paragraph(tc.test_id, table_body_style),
                Paragraph(tc.category.value, table_body_style),
                Paragraph(tc.description, table_body_style),
                Paragraph(status_text, table_body_style),
                Paragraph(f"<font color='{sev_color}'><b>{tc.severity.value}</b></font>", table_body_style),
                Paragraph(tc.recommendation or tc.issue_description or "Verified against reference expectation.", table_body_style)
            ])

        cases_table = Table(test_rows, colWidths=[55, 65, 150, 45, 55, 170])
        cases_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(cases_table)
        story.append(Spacer(1, 14))

        # 5. Summary Recommendations
        if report.recommendations_summary:
            story.append(Paragraph("3. Actionable Remediation Summary", heading2_style))
            for rec in report.recommendations_summary:
                story.append(Paragraph(f"• {rec}", table_body_style))

        # Build document
        doc.build(story)
        global_log_buffer.log("PDF_EXPORT", "AGENT_2", f"Generated executive QA PDF: {file_path.name}")
        return str(file_path)
