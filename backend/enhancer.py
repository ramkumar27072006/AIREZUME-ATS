# backend/enhancer.py
from typing import Dict, Any, Optional
import re

def _split_sentences(text: str):
    # naive sentence splitter
    if not text:
        return []
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def _make_bullets_from_text(text: str, max_bullets=8):
    sents = _split_sentences(text)
    bullets = []
    for s in sents:
        # short normalization
        s2 = re.sub(r'\s+', ' ', s).strip()
        if len(s2) > 10:
            bullets.append(s2)
        if len(bullets) >= max_bullets:
            break
    return bullets

def ensemble_enhance(text: str, job_description: str, prompt: Optional[str] = None) -> Dict[str, Any]:
    """
    Simple rule-based 'enhancer' placeholder. Return dictionary with
    - name (if found)
    - summary (first paragraph)
    - bullets: generated bullet points
    - text: merged enhanced text
    This function is where you'd call an LLM later.
    """
    src = text or ""
    lines = src.splitlines()
    # first non-empty line as name (if appears like a name)
    name = ""
    for l in lines[:6]:
        t = l.strip()
        if t and len(t) < 60 and len(t.split()) <= 4:
            name = t
            break

    # find a short summary: first paragraph-like block
    paragraphs = [p.strip() for p in src.split("\n\n") if p.strip()]
    summary = paragraphs[0] if paragraphs else (src[:200] if src else "")

    # make bullets from the resume text
    bullets = _make_bullets_from_text(src, max_bullets=10)

    # add job_description as a skill-oriented bullet
    if job_description:
        bullets.insert(0, f"Target role: {job_description.strip()}")

    enhanced_text = f"{name}\n\n{summary}\n\n" + "\n".join(f"- {b}" for b in bullets)

    # return dict with fields expected by template_engine and frontend
    return {
        "name": name,
        "summary": summary,
        "bullets": bullets,
        "text": enhanced_text,
        "metadata": {"source_enhancer": "rule-based-v1"},
    }
