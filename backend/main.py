# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
import os
import shutil

from backend.parser import parse_pdf_bytes
from backend.ats_score import score_resume as local_ats_score
from backend.enhancer import ensemble_enhance
from backend.template_engine import generate_docx, generate_pdf_from_text

app = FastAPI(title="Resume Optimizer API", version="0.1.0")

# Allow CORS from Streamlit (usually localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScoreRequest(BaseModel):
    parsed: Dict[str, Any]
    job_description: str


class EnhanceRequest(BaseModel):
    parsed: Dict[str, Any]
    job_description: str
    # optional prompt override
    prompt: str = None


class GenerateRequest(BaseModel):
    data: Dict[str, Any]


@app.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    """
    Accepts a PDF or DOCX upload. Returns extracted text in JSON {"source":"local","text": "..."}
    """
    try:
        contents = await file.read()
        text = parse_pdf_bytes(contents, filename=file.filename)
        return {"source": "local", "text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/score")
async def score_resume(req: ScoreRequest):
    """
    Accepts JSON: {"parsed": {...}, "job_description": "..."}
    Returns ATS scoring JSON.
    """
    try:
        parsed = req.parsed
        jd = req.job_description or ""
        result = local_ats_score(parsed, jd)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/enhance")
async def enhance_resume(req: EnhanceRequest):
    """
    Accepts JSON: {"parsed": {...}, "job_description": "...", "prompt": "..."}
    Returns enhanced resume dictionary (text + optionally structured)
    """
    try:
        parsed = req.parsed
        jd = req.job_description or ""
        prompt = req.prompt
        text = parsed.get("text", "") if isinstance(parsed, dict) else str(parsed)
        enhanced = ensemble_enhance(text, jd, prompt=prompt)
        return enhanced
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/docx")
def gen_docx(req: GenerateRequest):
    """
    Accepts JSON: {"data": { enhanced resume data } }
    Returns a file response (docx)
    """
    try:
        path = generate_docx(req.data)
        return {"filename": os.path.basename(path), "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/pdf")
def gen_pdf(req: GenerateRequest):
    """
    Accepts JSON: {"data": { enhanced resume data } }
    Returns JSON with file path. (Streamlit will download by requesting this file path)
    """
    try:
        data = req.data
        name = data.get("name") or data.get("full_name") or "candidate"
        summary = data.get("summary", "")
        body = data.get("text", summary)
        pdf_path = generate_pdf_from_text(f"{name}\n\n{summary}\n\n{body}", name=name)
        return {"filename": os.path.basename(pdf_path), "path": pdf_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
