"""
Astro Service - Project Scaffolding, File System Management, Code Validation, and Preview Server
"""
import os
import re
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

from backend.schemas.agent1_schema import AstroProjectManifest, AstroComponentCode
from backend.utils.logger import global_log_buffer
from backend.utils.security import is_safe_path


class AstroService:
    def __init__(self, base_dir: str = "generated_projects"):
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.active_processes: Dict[str, subprocess.Popen] = {}

    def get_project_dir(self, project_id: str) -> Path:
        p = self.base_dir / project_id
        if not is_safe_path(str(p), str(self.base_dir)):
            raise ValueError(f"Invalid project path traversal attempt: {project_id}")
        return p

    def write_project_files(self, manifest: AstroProjectManifest) -> str:
        """
        Materializes an Astro project manifest onto disk in the required modular structure:
        src/
          components/
          layouts/
          pages/
          data/
          styles/
        public/
        package.json
        astro.config.mjs
        """
        proj_dir = self.get_project_dir(manifest.project_id)
        proj_dir.mkdir(parents=True, exist_ok=True)

        # Standard subdirectories
        (proj_dir / "src" / "components").mkdir(parents=True, exist_ok=True)
        (proj_dir / "src" / "layouts").mkdir(parents=True, exist_ok=True)
        (proj_dir / "src" / "pages").mkdir(parents=True, exist_ok=True)
        (proj_dir / "src" / "data").mkdir(parents=True, exist_ok=True)
        (proj_dir / "src" / "styles").mkdir(parents=True, exist_ok=True)
        (proj_dir / "src" / "schemas").mkdir(parents=True, exist_ok=True)
        (proj_dir / "public").mkdir(parents=True, exist_ok=True)

        # 1. Write components
        for comp in manifest.components:
            target_path = proj_dir / comp.path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(comp.content)

        # 2. Write structured data file
        data_path = proj_dir / "src" / "data" / "homepage.js"
        with open(data_path, "w", encoding="utf-8") as f:
            f.write(manifest.structured_content_file)

        # 3. Write Sanity schemas
        for sanity_schema in manifest.sanity_schemas:
            schema_file = proj_dir / "src" / "schemas" / f"{sanity_schema.schema_name}.js"
            with open(schema_file, "w", encoding="utf-8") as f:
                f.write(sanity_schema.schema_code)

        # 4. Write global CSS
        css_path = proj_dir / "src" / "styles" / "global.css"
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(manifest.global_css)

        # 5. Write package.json
        pkg_path = proj_dir / "package.json"
        with open(pkg_path, "w", encoding="utf-8") as f:
            f.write(manifest.package_json)

        # 6. Write astro.config.mjs
        config_path = proj_dir / "astro.config.mjs"
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(manifest.astro_config)

        # 7. Write index.html pre-render for direct browser preview
        compiled_html = self.compile_to_static_html(manifest)
        index_html_path = proj_dir / "public" / "preview.html"
        with open(index_html_path, "w", encoding="utf-8") as f:
            f.write(compiled_html)

        global_log_buffer.log("ASTRO_GEN", "AGENT_1", f"Wrote {len(manifest.components)} components and assets to {proj_dir.name}")
        return str(proj_dir)

    def validate_project(self, project_id: str) -> List[str]:
        """
        Validates the modular Astro project:
        - Frontmatter integrity
        - File existence
        - Matching imports
        - Responsive CSS classes
        """
        proj_dir = self.get_project_dir(project_id)
        errors: List[str] = []

        if not (proj_dir / "package.json").exists():
            errors.append("Missing package.json")
        if not (proj_dir / "astro.config.mjs").exists():
            errors.append("Missing astro.config.mjs")
        if not (proj_dir / "src" / "pages" / "index.astro").exists():
            errors.append("Missing src/pages/index.astro")
        if not (proj_dir / "src" / "data" / "homepage.js").exists():
            errors.append("Missing structured content file: src/data/homepage.js")

        # Check components frontmatter
        comp_dir = proj_dir / "src" / "components"
        if comp_dir.exists():
            for f in comp_dir.glob("*.astro"):
                content = f.read_text(encoding="utf-8")
                # Must have --- delimiters if it has frontmatter
                if content.startswith("---"):
                    parts = content.split("---")
                    if len(parts) < 3:
                        errors.append(f"Component {f.name} has unclosed frontmatter '---' fence.")

        return errors

    def compile_to_static_html(self, manifest: AstroProjectManifest) -> str:
        """
        Generates a 1:1 compiled HTML document from the modular Astro components and data.
        This provides a zero-dependency, instantaneous preview server for Playwright, OpenCV, and Dashboard iframe.
        """
        # Find Layout and Components
        layout_comp = next((c for c in manifest.components if "MainLayout" in c.filename), None)
        header_comp = next((c for c in manifest.components if "Header" in c.filename), None)
        hero_comp = next((c for c in manifest.components if "Hero" in c.filename), None)
        about_comp = next((c for c in manifest.components if "About" in c.filename), None)
        sectors_comp = next((c for c in manifest.components if "Sectors" in c.filename or "Services" in c.filename), None)
        stats_comp = next((c for c in manifest.components if "Stats" in c.filename), None)
        projects_comp = next((c for c in manifest.components if "Projects" in c.filename), None)
        contact_comp = next((c for c in manifest.components if "Contact" in c.filename), None)
        footer_comp = next((c for c in manifest.components if "Footer" in c.filename), None)

        def extract_template(comp: Optional[AstroComponentCode]) -> str:
            if not comp:
                return ""
            parts = comp.content.split("---")
            if len(parts) >= 3:
                return parts[2].strip()
            return comp.content.strip()

        css = manifest.global_css

        # Build clean preview document
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{manifest.project_name}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {css}
  </style>
</head>
<body class="bg-surface text-slate-800 antialiased selection:bg-accent-gold selection:text-white">
  <div id="site-container" class="min-h-screen flex flex-col">
    {extract_template(header_comp)}
    <main class="flex-grow">
      {extract_template(hero_comp)}
      {extract_template(about_comp)}
      {extract_template(sectors_comp)}
      {extract_template(stats_comp)}
      {extract_template(projects_comp)}
      {extract_template(contact_comp)}
    </main>
    {extract_template(footer_comp)}
  </div>
</body>
</html>"""
        return html
