"""
Security and Path Validation Utilities
Enforces containment within allowed project folders to prevent directory traversal and unsafe executions.
"""
import os
import re
from pathlib import Path
from typing import Set

ALLOWED_EXTENSIONS: Set[str] = {
    ".png", ".jpg", ".jpeg", ".pdf", ".svg", ".webp",
    ".astro", ".js", ".mjs", ".ts", ".tsx", ".css", ".json", ".html", ".md"
}

ALLOWED_UPLOAD_EXTENSIONS: Set[str] = {
    ".png", ".jpg", ".jpeg", ".pdf", ".webp"
}


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal and invalid characters."""
    filename = os.path.basename(filename)
    filename = re.sub(r"[^\w\.-]", "_", filename)
    return filename


def validate_file_extension(filename: str, allowed: Set[str] = ALLOWED_EXTENSIONS) -> bool:
    """Check if file extension is permitted."""
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed


def is_safe_path(target_path: str, base_dir: str) -> bool:
    """
    Ensure target_path resolves strictly within base_dir.
    Guards against path traversal attacks (e.g. '../..').
    """
    try:
        resolved_base = Path(base_dir).resolve()
        resolved_target = Path(target_path).resolve()
        return resolved_base in resolved_target.parents or resolved_base == resolved_target
    except Exception:
        return False


def validate_project_path(project_dir: str, root_dir: str) -> str:
    """Validates and returns normalized safe path within root."""
    if not is_safe_path(project_dir, root_dir):
        raise ValueError(f"Security Alert: Path '{project_dir}' attempts traversal outside safe root '{root_dir}'")
    return str(Path(project_dir).resolve())
