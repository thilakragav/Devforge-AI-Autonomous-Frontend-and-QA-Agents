"""
Direct Integration Tests for FastAPI Route Handlers
"""
import pytest
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import health_check
from backend.api.routes.preview import get_rendered_preview
from backend.api.routes.agent1 import get_project_details
from backend.api.routes.upload import upload_file, Base64UploadRequest
from backend.api.routes.reports import get_report_json


def test_health_check_handler():
    """Verify health check handler returns correct service metadata."""
    res = health_check()
    assert res["status"] == "online"
    assert "ai_engine" in res
    assert "active_agents" in res


def test_preview_handler():
    """Verify preview route serves compiled HTML with RDGCC branding."""
    res = get_rendered_preview("project_001")
    assert res.status_code == 200
    assert "RDGCC" in res.body.decode("utf-8")


def test_get_project_details_handler():
    """Verify project structure route returns modular components."""
    res = get_project_details("project_001")
    assert res["project_id"] == "project_001"
    assert len(res["components"]) >= 5
    assert res["validation_errors"] == []


def test_base64_upload_handler():
    """Verify upload handler saves files and extracts previews."""
    import base64
    dummy_b64 = base64.b64encode(b"dummy image data").decode("utf-8")
    req = Base64UploadRequest(filename="test_upload.png", content_b64=dummy_b64)
    res = upload_file(req)
    assert res["status"] == "success"
    assert "test_upload" in res["saved_path"]


def test_get_report_handler():
    """Verify report retrieval handler loads valid JSON report."""
    res = get_report_json("project_001", iteration=1)
    assert res["project_id"] == "project_001"
    assert "total_tests" in res
