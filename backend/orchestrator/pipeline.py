"""
Central Orchestrator Pipeline
Coordinates the autonomous closed-loop collaboration between Agent 1 and Agent 2.
"""
import asyncio
from typing import Optional, List
from pathlib import Path

from backend.schemas.orchestrator_schema import OrchestratorRunState, CorrectionDirective
from backend.schemas.agent1_schema import AstroProjectManifest
from backend.schemas.agent2_schema import QAReport, TestSeverity
from backend.agents.agent1.analyzer import DesignAnalyzer
from backend.agents.agent1.generator import AstroCodeGenerator
from backend.agents.agent1.refactorer import AstroRefactorer
from backend.agents.agent2.playwright_driver import BrowserDriver
from backend.agents.agent2.visual_diff import VisualDiffTester
from backend.agents.agent2.responsive_tester import ResponsiveTester
from backend.agents.agent2.functional_tester import FunctionalTester
from backend.agents.agent2.report_generator import QAReportGenerator
from backend.services.astro_service import AstroService
from backend.services.file_service import FileService
from backend.orchestrator.state import orchestrator_state_manager
from backend.utils.logger import global_log_buffer


class CentralOrchestrator:
    def __init__(
        self,
        analyzer: Optional[DesignAnalyzer] = None,
        generator: Optional[AstroCodeGenerator] = None,
        refactorer: Optional[AstroRefactorer] = None,
        astro_service: Optional[AstroService] = None,
        browser_driver: Optional[BrowserDriver] = None,
        visual_tester: Optional[VisualDiffTester] = None,
        responsive_tester: Optional[ResponsiveTester] = None,
        functional_tester: Optional[FunctionalTester] = None,
        report_generator: Optional[QAReportGenerator] = None,
        file_service: Optional[FileService] = None
    ):
        self.analyzer = analyzer or DesignAnalyzer()
        self.generator = generator or AstroCodeGenerator()
        self.refactorer = refactorer or AstroRefactorer()
        self.astro_service = astro_service or AstroService()
        self.browser_driver = browser_driver or BrowserDriver()
        self.visual_tester = visual_tester or VisualDiffTester()
        self.responsive_tester = responsive_tester or ResponsiveTester()
        self.functional_tester = functional_tester or FunctionalTester()
        self.report_generator = report_generator or QAReportGenerator()
        self.file_service = file_service or FileService()

    def execute_run(
        self,
        run_id: str,
        file_path: Optional[str] = None,
        figma_url: Optional[str] = None,
        max_iterations: int = 3,
        port: int = 8000
    ) -> OrchestratorRunState:
        """
        Executes the full 17-step multi-agent cycle with up to 3 automated feedback iterations.
        """
        state = orchestrator_state_manager.create_run(
            run_id=run_id,
            design_input_path=file_path or "",
            figma_url=figma_url,
            max_iterations=max_iterations
        )

        global_log_buffer.log("ORCHESTRATOR", "ORCHESTRATOR", f"Starting automated execution pipeline for run: {run_id}")

        try:
            # -------------------------------------------------------------
            # STEP 1 & 2: Accept Design & Start Agent 1 Analysis
            # -------------------------------------------------------------
            state.status = "ANALYZING"
            orchestrator_state_manager.update_run(state)
            global_log_buffer.log("PIPELINE", "ORCHESTRATOR", "Step 1/17: Delegating reference visual asset to Agent 1.")

            # Ensure reference image exists
            clean_ref_image = "uploads/rdgcc_reference.png"
            if file_path:
                clean_ref_image = self.file_service.process_input_for_analysis(file_path)

            design_analysis = self.analyzer.analyze(
                file_path=clean_ref_image,
                figma_url=figma_url
            )
            state.design_analysis = design_analysis
            orchestrator_state_manager.update_run(state)

            # -------------------------------------------------------------
            # STEP 3 & 4: Generate Modular Astro Project (v1)
            # -------------------------------------------------------------
            state.status = "GENERATING"
            orchestrator_state_manager.update_run(state)
            global_log_buffer.log("PIPELINE", "ORCHESTRATOR", "Step 4/17: Agent 1 synthesizing modular Astro components.")

            manifest = self.generator.generate_project(
                analysis=design_analysis,
                project_id=run_id,
                version=1,
                output_directory=f"generated_projects/{run_id}"
            )

            # -------------------------------------------------------------
            # STEP 5: Validate Generated Code & Write Files to Disk
            # -------------------------------------------------------------
            state.status = "BUILDING"
            orchestrator_state_manager.update_run(state)
            global_log_buffer.log("PIPELINE", "ORCHESTRATOR", "Step 5/17: Materializing Astro project to disk.")
            self.astro_service.write_project_files(manifest)
            val_errors = self.astro_service.validate_project(run_id)
            if val_errors:
                manifest.build_valid = False
                manifest.validation_errors = val_errors
                global_log_buffer.log("PIPELINE", "ORCHESTRATOR", f"Validation warnings: {val_errors}", "WARNING")

            state.manifest_history.append(manifest)
            orchestrator_state_manager.update_run(state)

            # -------------------------------------------------------------
            # FEEDBACK LOOP: Iterations 1 to max_iterations (default 3)
            # -------------------------------------------------------------
            current_manifest = manifest
            iteration = 1

            while iteration <= max_iterations:
                state.current_iteration = iteration
                state.status = "TESTING"
                orchestrator_state_manager.update_run(state)

                global_log_buffer.log("PIPELINE", "ORCHESTRATOR", f"Beginning QA Testing Iteration {iteration}/{max_iterations}")

                # STEP 6: Prepare Preview Server & Static HTML
                preview_html = self.astro_service.compile_to_static_html(current_manifest)
                preview_url = f"http://127.0.0.1:{port}/api/preview/{run_id}"
                state.preview_url = preview_url

                # STEP 7: Playwright Multi-Viewport Capture (Desktop, Tablet, Mobile)
                global_log_buffer.log("PIPELINE", "AGENT_2", f"Step 7/17: Capturing viewports (1440x900, 768x1024, 375x812) for v{iteration}")
                screenshots = self.browser_driver.capture_all_viewports(
                    url=preview_url,
                    project_id=run_id,
                    iteration=iteration
                )

                # STEP 8 & 9: Agent 2 Visual Testing (OpenCV SSIM & Bounding Contours)
                desktop_screenshot = screenshots.get("Desktop", "")
                visual_metrics, visual_tcs = self.visual_tester.compare(
                    reference_image_path=clean_ref_image,
                    generated_image_path=desktop_screenshot,
                    project_id=run_id,
                    iteration=iteration
                )

                # STEP 10: Agent 2 Responsive Testing
                resp_audits, resp_tcs = self.responsive_tester.audit_viewports(
                    screenshots=screenshots,
                    html_content=preview_html
                )

                # STEP 11: Agent 2 Functional Testing (Links, Buttons, Form, Images)
                func_tcs = self.functional_tester.run_tests(
                    html_content=preview_html,
                    preview_url=preview_url
                )

                # STEP 12: Assemble Complete QA Report (HTML & PDF)
                all_tcs = visual_tcs + resp_tcs + func_tcs
                qa_report = self.report_generator.build_report(
                    project_id=run_id,
                    iteration=iteration,
                    test_cases=all_tcs,
                    visual_metrics=visual_metrics,
                    responsive_audits=resp_audits
                )
                state.qa_history.append(qa_report)
                orchestrator_state_manager.update_run(state)

                # ---------------------------------------------------------
                # STEP 13 & 14: Evaluate Corrections or Terminate
                # ---------------------------------------------------------
                critical_or_high_fails = [
                    tc for tc in all_tcs 
                    if not tc.passed and tc.severity in (TestSeverity.CRITICAL, TestSeverity.HIGH)
                ]

                if not critical_or_high_fails:
                    global_log_buffer.log(
                        "PIPELINE",
                        "ORCHESTRATOR",
                        f"Iteration {iteration} PASSED all critical and high criteria! Quality threshold satisfied.",
                        "SUCCESS"
                    )
                    break

                if iteration >= max_iterations:
                    global_log_buffer.log(
                        "PIPELINE",
                        "ORCHESTRATOR",
                        f"Reached maximum correction iterations ({max_iterations}). Finalizing report.",
                        "WARNING"
                    )
                    break

                # Prepare CorrectionDirective for Agent 1
                state.status = "REFACTORING"
                orchestrator_state_manager.update_run(state)

                target_components = list(set([tc.affected_component for tc in critical_or_high_fails if tc.affected_component]))
                instructions = [tc.recommendation or tc.issue_description for tc in critical_or_high_fails if tc.recommendation or tc.issue_description]
                directive = CorrectionDirective(
                    iteration=iteration,
                    target_components=target_components,
                    specific_issues=[tc.description for tc in critical_or_high_fails],
                    actionable_instructions=instructions
                )
                state.correction_history.append(directive)

                global_log_buffer.log(
                    "PIPELINE",
                    "ORCHESTRATOR",
                    f"Transmitting {len(instructions)} QA correction directives to Agent 1 for iteration {iteration + 1}."
                )

                # Agent 1 applies surgical refactoring
                next_version = iteration + 1
                current_manifest = self.refactorer.apply_corrections(
                    manifest=current_manifest,
                    directive=directive,
                    new_version=next_version
                )
                self.astro_service.write_project_files(current_manifest)
                state.manifest_history.append(current_manifest)
                orchestrator_state_manager.update_run(state)

                iteration += 1

            # -------------------------------------------------------------
            # STEP 17: Save Final Results & Mark Completed
            # -------------------------------------------------------------
            state.status = "COMPLETED"
            orchestrator_state_manager.update_run(state)
            global_log_buffer.log("PIPELINE", "ORCHESTRATOR", f"Multi-Agent PoC run {run_id} successfully COMPLETED.", "SUCCESS")
            return state

        except Exception as e:
            state.status = "FAILED"
            state.error_message = str(e)
            orchestrator_state_manager.update_run(state)
            global_log_buffer.log("PIPELINE", "ORCHESTRATOR", f"Pipeline failed: {e}", "ERROR")
            raise
