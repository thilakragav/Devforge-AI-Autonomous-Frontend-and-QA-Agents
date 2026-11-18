"""
Agent 1 - Refactorer & Patch Generator
Applies surgical fixes to Astro components and CSS based on Agent 2 QA test feedback.
"""
from typing import List
from backend.schemas.agent1_schema import AstroProjectManifest, AstroComponentCode
from backend.schemas.orchestrator_schema import CorrectionDirective
from backend.utils.logger import global_log_buffer


class AstroRefactorer:
    def __init__(self):
        pass

    def apply_corrections(
        self,
        manifest: AstroProjectManifest,
        directive: CorrectionDirective,
        new_version: int
    ) -> AstroProjectManifest:
        """
        Applies targeted improvements to components identified by Agent 2 QA feedback.
        Produces a new versioned manifest (e.g. v2 or v3) while maintaining unimpacted code.
        """
        global_log_buffer.log(
            "REFACTOR",
            "AGENT_1",
            f"Applying QA corrections for iteration {directive.iteration} -> new version v{new_version}. Targets: {directive.target_components}"
        )

        updated_components: List[AstroComponentCode] = []
        updated_css = manifest.global_css

        for comp in manifest.components:
            new_comp = comp.model_copy()

            # Target 1: Responsive typography or padding adjustments in Hero
            if any(t in comp.filename for t in directive.target_components) and "Hero" in comp.filename:
                global_log_buffer.log("REFACTOR", "AGENT_1", f"Refactoring {comp.filename}: tuning responsive container padding and headline clamp.")
                # Inject enhanced responsive clamp and padding
                new_comp.content = comp.content.replace(
                    'class="hero-headline text-4xl sm:text-5xl md:text-6xl',
                    'class="hero-headline text-3xl sm:text-4xl md:text-5xl lg:text-6xl tracking-tight'
                )

            # Target 2: Contact form accessibility and button validation
            elif any(t in comp.filename for t in directive.target_components) and "Contact" in comp.filename:
                global_log_buffer.log("REFACTOR", "AGENT_1", f"Refactoring {comp.filename}: adding aria-labels and touch target padding.")
                new_comp.content = comp.content.replace(
                    '<button \n              type="submit"',
                    '<button \n              type="submit" \n              aria-label="Submit Corporate Inquiry Form"'
                )

            # Target 3: Header mobile responsiveness
            elif any(t in comp.filename for t in directive.target_components) and "Header" in comp.filename:
                global_log_buffer.log("REFACTOR", "AGENT_1", f"Refactoring {comp.filename}: improving mobile viewport constraints.")
                new_comp.content = comp.content.replace(
                    '<header class="sticky top-0',
                    '<header class="sticky top-0 w-full overflow-hidden'
                )

            updated_components.append(new_comp)

        # Update global CSS if requested
        if "global.css" in directive.target_components or "layout" in directive.target_components:
            global_log_buffer.log("REFACTOR", "AGENT_1", "Optimizing global CSS: adding overflow safety rule.")
            if "/* Overflow containment safety */" not in updated_css:
                updated_css += "\n/* Overflow containment safety */\nmain, section { max-width: 100vw; overflow-x: clip; }\n"

        updated_manifest = manifest.model_copy(
            update={
                "version": new_version,
                "components": updated_components,
                "global_css": updated_css,
                "output_directory": f"generated_projects/{manifest.project_id}_v{new_version}"
            }
        )

        global_log_buffer.log("REFACTOR", "AGENT_1", f"Completed refactor cycle v{new_version}.")
        return updated_manifest
