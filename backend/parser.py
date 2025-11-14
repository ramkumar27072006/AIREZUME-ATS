# backend/parser.py
import pdfplumber
import tempfile
import os
from typing import Optional

def parse_pdf_bytes(pdf_bytes: bytes, filename: Optional[str] = "upload.pdf") -> str:
    """
    Given bytes of a PDF (or other binary), write to temp file and extract text using pdfplumber.
    Returns plain text.
    """
    # detect .pdf
    lower = (filename or "").lower()
    if lower.endswith(".pdf") or True:  # we'll attempt PDF extraction; if it's docx bytes, user can convert separately
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        try:
            tmp.write(pdf_bytes)
            tmp.flush()
            tmp.close()
            text = ""
            try:
                with pdfplumber.open(tmp.name) as pdf:
                    for p in pdf.pages:
                        txt = p.extract_text()
                        if txt:
                            text += txt + "\n"
            except Exception:
                # fallback: return bytes decoded maybe plain text
                try:
                    text = pdf_bytes.decode(errors="ignore")
                except Exception:
                    text = ""
            return text.strip()
        finally:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass
