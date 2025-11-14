# backend/template_engine.py
import os
import tempfile
from typing import Dict, Any
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import uuid


def generate_docx(enhanced: Dict[str, Any]) -> str:
    """
    Generate DOCX from enhanced resume dict.
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



def generate_pdf_from_text(text: str, name: str = "Candidate") -> str:
    """
    Simple fallback PDF generator using reportlab.
    Works on Windows, Linux, and Render.
    """
    tmpdir = tempfile.gettempdir()
    fname = f"resume_{uuid.uuid4().hex[:8]}.pdf"
    path = os.path.join(tmpdir, fname)

    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    margin = 50
    y = height - margin

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, name)
    y -= 25

    # Body
    c.setFont("Helvetica", 10)
    for line in text.split("\n"):
        if y < 50:
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", 10)

        # wrap text manually
        while len(line) > 100:
            cut = line[:100]
            last_space = cut.rfind(" ")
            if last_space > 0:
                cut = cut[:last_space]
            c.drawString(margin, y, cut)
            y -= 14
            line = line[len(cut):].lstrip()

        c.drawString(margin, y, line)
        y -= 14

    c.save()
    return path
