# backend/template_engine.py
import os
import tempfile
import uuid
from typing import Dict, Any
from docx import Document
from fpdf import FPDF


def generate_docx(enhanced: Dict[str, Any]) -> str:
    """
    Generate a .docx file from enhanced resume data.
    """
    doc = Document()

    name = enhanced.get("name", "")
    summary = enhanced.get("summary", "")
    bullets = enhanced.get("bullets", []) or []
    text = enhanced.get("text", "")

    if name:
        doc.add_heading(name, level=1)

    if summary:
        doc.add_paragraph(summary)

    if bullets:
        doc.add_paragraph("")
        for b in bullets:
            doc.add_paragraph(b, style="List Bullet")

    if text:
        doc.add_paragraph("")
        doc.add_paragraph(text)

    tmpdir = tempfile.gettempdir()
    fname = f"enhanced_{uuid.uuid4().hex[:8]}.docx"
    path = os.path.join(tmpdir, fname)
    doc.save(path)

    return path


def generate_pdf_from_text(text: str, name: str = "candidate") -> str:
    """
    Generate a PDF using fpdf2 (Render compatible).
    """
    tmpdir = tempfile.gettempdir()
    fname = f"resume_{uuid.uuid4().hex[:8]}.pdf"
    path = os.path.join(tmpdir, fname)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, name, ln=True)

    # Body
    pdf.set_font("Arial", "", 11)

    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf.output(path)

    return path
