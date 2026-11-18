"""
Agent 1 - Design Analyzer
Decomposes uploaded design assets (PNG, JPG, PDF, Figma URL) into structured design specifications.
"""
from typing import Optional
from pathlib import Path

from backend.schemas.agent1_schema import DesignAnalysisResult
from backend.services.file_service import FileService
from backend.services.llm_service import LLMService
from backend.utils.logger import global_log_buffer


class DesignAnalyzer:
    def __init__(self, file_service: Optional[FileService] = None, llm_service: Optional[LLMService] = None):
        self.file_service = file_service or FileService()
        self.llm_service = llm_service or LLMService()

    def analyze(self, file_path: Optional[str] = None, figma_url: Optional[str] = None) -> DesignAnalysisResult:
        """
        Coordinates input validation, format normalization (PDF to image if necessary),
        and vision-based semantic extraction.
        """
        global_log_buffer.log("ANALYZER", "AGENT_1", f"Initiating design analysis. File: {file_path}, Figma: {figma_url}")

        reference_image_for_analysis: str = ""

        if file_path:
            p = Path(file_path).resolve()
            if not p.exists():
                raise FileNotFoundError(f"Input design file not found: {file_path}")

            # Normalize PDF or Image
            reference_image_for_analysis = self.file_service.process_input_for_analysis(str(p))
            global_log_buffer.log("ANALYZER", "AGENT_1", f"Prepared reference image for visual analysis: {Path(reference_image_for_analysis).name}")
        elif figma_url:
            global_log_buffer.log("ANALYZER", "AGENT_1", f"Processing Figma URL: {figma_url}")
            # In Figma URL mode, use the default reference visual template
            reference_image_for_analysis = "uploads/rdgcc_reference.png"
        else:
            raise ValueError("Either file_path or figma_url must be provided.")

        # Run Multimodal LLM Analysis
        analysis_result = self.llm_service.analyze_design(
            image_path=reference_image_for_analysis,
            figma_url=figma_url
        )

        global_log_buffer.log(
            "ANALYZER",
            "AGENT_1",
            f"Analysis complete: Identified {len(analysis_result.sections)} sections, {len(analysis_result.colors)} color tokens, and {len(analysis_result.typography)} font scales."
        )

        return analysis_result
