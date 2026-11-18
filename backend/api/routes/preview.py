"""
Preview API Route - Serves compiled preview HTML for iframe and browser inspection
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter(prefix="/api/preview", tags=["Preview"])
PROJECTS_DIR = (Path(__file__).resolve().parent.parent.parent.parent / "generated_projects").resolve()


@router.get("/{project_id}", response_class=HTMLResponse)
def get_rendered_preview(project_id: str):
    """
    Renders the live website for browser testing, Playwright, or dashboard iframe.
    """
    proj_dir = PROJECTS_DIR / project_id
    if not proj_dir.exists():
        # Check if project_001 baseline exists
        proj_dir = PROJECTS_DIR / "project_001"

    preview_file = proj_dir / "public" / "preview.html"
    if not preview_file.exists():
        raise HTTPException(status_code=404, detail="Preview document not compiled yet.")

    return HTMLResponse(content=preview_file.read_text(encoding="utf-8"))
