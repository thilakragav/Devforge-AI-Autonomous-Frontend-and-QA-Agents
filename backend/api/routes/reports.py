"""
Reports API Routes - QA Audit Retrieval & PDF/HTML Downloads
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
import json

from backend.schemas.agent2_schema import QAReport

router = APIRouter(prefix="/api/reports", tags=["Reports"])
REPORTS_DIR = (Path(__file__).resolve().parent.parent.parent.parent / "reports").resolve()


@router.get("/{project_id}")
def get_report_json(project_id: str, iteration: int = 1):
    file_path = REPORTS_DIR / f"QA_Report_{project_id}_v{iteration}.json"
    if not file_path.exists():
        # Search for any iteration
        matches = list(REPORTS_DIR.glob(f"QA_Report_{project_id}_v*.json"))
        if matches:
            file_path = matches[-1]
        else:
            raise HTTPException(status_code=404, detail=f"No QA report found for project: {project_id}")

    data = json.loads(file_path.read_text(encoding="utf-8"))
    return data


@router.get("/{project_id}/download")
def download_report(project_id: str, format: str = Query(default="pdf", pattern="^(pdf|html|json)$"), iteration: int = 1):
    if format == "pdf":
        matches = list(REPORTS_DIR.glob(f"QA_Report_{project_id}_*.pdf"))
        if not matches:
            raise HTTPException(status_code=404, detail="PDF report not found")
        return FileResponse(str(matches[-1]), media_type="application/pdf", filename=matches[-1].name)
    elif format == "html":
        file_path = REPORTS_DIR / f"QA_Report_{project_id}_v{iteration}.html"
        if not file_path.exists():
            matches = list(REPORTS_DIR.glob(f"QA_Report_{project_id}_v*.html"))
            if matches:
                file_path = matches[-1]
            else:
                raise HTTPException(status_code=404, detail="HTML report not found")
        return FileResponse(str(file_path), media_type="text/html", filename=file_path.name)
    else:
        file_path = REPORTS_DIR / f"QA_Report_{project_id}_v{iteration}.json"
        return FileResponse(str(file_path), media_type="application/json", filename=file_path.name)
