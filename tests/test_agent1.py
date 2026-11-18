"""
Unit and Integration Tests for Agent 1 - Design-to-Astro Code Generator
"""
import pytest
import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from backend.schemas.agent1_schema import (
    DesignAnalysisResult,
    AstroProjectManifest,
    ColorToken,
    TypographyToken,
    SectionSpec,
)
from backend.agents.agent1.analyzer import DesignAnalyzer
from backend.agents.agent1.generator import AstroCodeGenerator
from backend.agents.agent1.refactorer import AstroRefactorer
from backend.schemas.orchestrator_schema import CorrectionDirective
from backend.services.astro_service import AstroService


def test_design_analyzer_deterministic():
    """Verify Agent 1 decomposes reference design into structured specifications."""
    analyzer = DesignAnalyzer()
    ref_image = PROJECT_ROOT / "uploads" / "rdgcc_reference.png"
    
    result = analyzer.analyze(file_path=str(ref_image))
    
    assert isinstance(result, DesignAnalysisResult)
    assert result.project_name == "RDGCC Corporate Regional Portal"
    assert len(result.colors) >= 5
    assert len(result.sections) >= 6
    assert any(s.id == "hero" for s in result.sections)
    assert any(s.id == "sectors" for s in result.sections)


def test_astro_code_generator_modular_structure():
    """Verify Agent 1 generates modular Astro components, structured data, and configs."""
    analyzer = DesignAnalyzer()
    generator = AstroCodeGenerator()
    
    sample_analysis = DesignAnalysisResult(
        project_name="RDGCC Test",
        brand_identity="Modern Corporate GCC",
        colors=[ColorToken(name="primary", hex="#0A192F", usage="header")],
        typography=[TypographyToken(element="h1", font_family="Inter", size="3rem")],
        sections=[
            SectionSpec(id="hero", name="Hero Section", component_name="Hero.astro", description="Hero banner", data_keys=["hero"]),
            SectionSpec(id="sectors", name="Sectors", component_name="Sectors.astro", description="Sectors grid", data_keys=["sectors"])
        ],
        assumptions_and_limitations=["Tested locally"]
    )
    
    manifest = generator.generate_project(sample_analysis, project_id="test_proj_001", version=1)
    
    assert isinstance(manifest, AstroProjectManifest)
    assert manifest.project_id == "test_proj_001"
    assert len(manifest.components) >= 8  # Header, Nav, Hero, About, Sectors, Stats, Projects, Contact, Footer, Layout, Index
    
    # Check that individual components exist (no monolithic single file)
    filenames = [c.filename for c in manifest.components]
    assert "Header.astro" in filenames
    assert "Hero.astro" in filenames
    assert "Sectors.astro" in filenames
    assert "Footer.astro" in filenames
    assert "MainLayout.astro" in filenames
    assert "index.astro" in filenames
    
    # Check content separation (homepage.js)
    assert "export const heroContent" in manifest.structured_content_file
    assert "export const sectorsData" in manifest.structured_content_file
    
    # Check Sanity CMS schemas
    assert len(manifest.sanity_schemas) >= 4
    sanity_names = [s.schema_name for s in manifest.sanity_schemas]
    assert "homepage" in sanity_names
    assert "sector" in sanity_names


def test_astro_service_materialization_and_validation(tmp_path):
    """Verify AstroService writes valid files to disk and verifies syntax."""
    generator = AstroCodeGenerator()
    llm_analysis = DesignAnalyzer().llm_service._get_rdgcc_reference_analysis(is_demo=True)
    manifest = generator.generate_project(llm_analysis, project_id="test_astro_val", version=1)
    
    service = AstroService(base_dir=str(tmp_path))
    out_dir = service.write_project_files(manifest)
    
    assert Path(out_dir).exists()
    assert (Path(out_dir) / "src" / "components" / "Hero.astro").exists()
    assert (Path(out_dir) / "src" / "data" / "homepage.js").exists()
    assert (Path(out_dir) / "package.json").exists()
    
    errors = service.validate_project("test_astro_val")
    assert errors == []


def test_astro_refactorer_targeted_patching():
    """Verify Agent 1 refactorer modifies ONLY the targeted components during correction loops."""
    generator = AstroCodeGenerator()
    llm_analysis = DesignAnalyzer().llm_service._get_rdgcc_reference_analysis(is_demo=True)
    manifest = generator.generate_project(llm_analysis, project_id="test_refactor", version=1)
    
    refactorer = AstroRefactorer()
    directive = CorrectionDirective(
        iteration=1,
        target_components=["Hero.astro"],
        specific_issues=["Hero headline typography clamp"],
        actionable_instructions=["Add responsive clamp classes"]
    )
    
    v2_manifest = refactorer.apply_corrections(manifest, directive, new_version=2)
    
    assert v2_manifest.version == 2
    hero_v2 = next(c for c in v2_manifest.components if "Hero" in c.filename)
    about_v2 = next(c for c in v2_manifest.components if "About" in c.filename)
    about_v1 = next(c for c in manifest.components if "About" in c.filename)
    
    # Hero was patched
    assert "lg:text-6xl" in hero_v2.content
    # About was preserved identically
    assert about_v2.content == about_v1.content
