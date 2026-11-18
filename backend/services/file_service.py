"""
File Service - Handles file uploads, PDF page rasterization, and image handling
"""
import os
import shutil
from typing import List, Optional
from pathlib import Path
from PIL import Image

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

from backend.utils.security import sanitize_filename, validate_file_extension, ALLOWED_UPLOAD_EXTENSIONS
from backend.utils.logger import global_log_buffer


class FileService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir).resolve()
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_upload(self, file_bytes: bytes, original_filename: str) -> str:
        """Saves an uploaded file safely to the upload directory and returns its absolute path."""
        clean_name = sanitize_filename(original_filename)
        if not validate_file_extension(clean_name, ALLOWED_UPLOAD_EXTENSIONS):
            raise ValueError(f"File type not permitted: {clean_name}")

        dest_path = self.upload_dir / clean_name
        # If exists, append timestamp or counter
        counter = 1
        base, ext = os.path.splitext(clean_name)
        while dest_path.exists():
            dest_path = self.upload_dir / f"{base}_{counter}{ext}"
            counter += 1

        with open(dest_path, "wb") as f:
            f.write(file_bytes)

        global_log_buffer.log("UPLOAD", "SYSTEM", f"Saved upload: {dest_path.name} ({len(file_bytes)} bytes)")
        return str(dest_path)

    def extract_pdf_pages_to_images(self, pdf_path: str, dpi: int = 150) -> List[str]:
        """
        Extracts each page of a PDF as a high-resolution PNG image.
        Returns list of absolute paths to generated images.
        """
        if not PYMUPDF_AVAILABLE:
            global_log_buffer.log("PDF_EXTRACT", "SYSTEM", "PyMuPDF (fitz) not available, attempting fallback", "WARNING")
            raise RuntimeError("PyMuPDF is required for PDF page extraction.")

        pdf_path = Path(pdf_path).resolve()
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        extracted_images: List[str] = []
        doc = fitz.open(str(pdf_path))
        base_name = pdf_path.stem

        zoom = dpi / 72  # 72 is standard PDF point resolution
        matrix = fitz.Matrix(zoom, zoom)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=matrix)
            out_filename = self.upload_dir / f"{base_name}_page_{page_num + 1}.png"
            pix.save(str(out_filename))
            extracted_images.append(str(out_filename))

        doc.close()
        global_log_buffer.log("PDF_EXTRACT", "SYSTEM", f"Extracted {len(extracted_images)} page(s) from {pdf_path.name}")
        return extracted_images

    def process_input_for_analysis(self, file_path: str) -> str:
        """
        Takes an input path (PNG, JPG, PDF). If PDF, extracts page 1 as reference image.
        Returns single image path for visual analysis.
        """
        path = Path(file_path).resolve()
        ext = path.suffix.lower()

        if ext == ".pdf":
            pages = self.extract_pdf_pages_to_images(str(path))
            if not pages:
                raise ValueError(f"No pages could be extracted from PDF: {path}")
            return pages[0]
        elif ext in {".png", ".jpg", ".jpeg", ".webp"}:
            return str(path)
        else:
            raise ValueError(f"Unsupported input format: {ext}")

    def create_thumbnail(self, image_path: str, max_size: int = 400) -> str:
        """Generates a small web-friendly thumbnail for the dashboard."""
        p = Path(image_path)
        thumb_path = p.parent / f"{p.stem}_thumb.webp"
        with Image.open(p) as img:
            img.thumbnail((max_size, max_size))
            img.save(thumb_path, "WEBP", quality=85)
        return str(thumb_path)
