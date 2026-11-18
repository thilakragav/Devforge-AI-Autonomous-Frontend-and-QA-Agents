"""
Agent 1 API Routes - Design Analysis & Astro Project Generation
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from backend.schemas.agent1_schema import (
    DesignInputRequest,
    DesignAnalysisResult,
    AstroProjectManifest,
)
from backend.agents.agent1.analyzer import DesignAnalyzer
from backend.agents.agent1.generator import AstroCodeGenerator
from backend.services.astro_service import AstroService

router = APIRouter(prefix="/api/agent1", tags=["Agent 1"])
analyzer = DesignAnalyzer()
generator = AstroCodeGenerator()
astro_service = AstroService()


class GenerateRequest(BaseModel):
    analysis: DesignAnalysisResult
    project_id: str = "project_001"
    version: int = 1


@router.post("/analyze", response_model=DesignAnalysisResult)
def analyze_design_endpoint(req: DesignInputRequest):
    try:
        result = analyzer.analyze(file_path=req.file_path, figma_url=req.figma_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent 1 analysis error: {str(e)}")


@router.post("/generate", response_model=AstroProjectManifest)
def generate_astro_project(req: GenerateRequest):
    try:
        manifest = generator.generate_project(
            analysis=req.analysis,
            project_id=req.project_id,
            version=req.version
        )
        astro_service.write_project_files(manifest)
        return manifest
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent 1 generation error: {str(e)}")


@router.get("/projects/{project_id}")
def get_project_details(project_id: str):
    try:
        proj_dir = astro_service.get_project_dir(project_id)
        if not proj_dir.exists():
            raise HTTPException(status_code=404, detail="Project not found")

        components = []
        comp_dir = proj_dir / "src" / "components"
        if comp_dir.exists():
            for f in comp_dir.glob("*.astro"):
                components.append({
                    "name": f.name,
                    "path": str(f.relative_to(proj_dir)),
                    "size_bytes": f.stat().st_size
                })

        return {
            "project_id": project_id,
            "path": str(proj_dir),
            "components": components,
            "validation_errors": astro_service.validate_project(project_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
