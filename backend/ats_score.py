# backend/ats_score.py
from typing import Dict, Any, List
import re
from difflib import SequenceMatcher

def _tokenize(text: str) -> List[str]:
    if not text:
        return []
    text = text.lower()
    # split on non word
    toks = re.findall(r"[a-z0-9\+\#\.\-]+", text)
    return toks

def _unique_keywords(jd: str) -> List[str]:
    toks = _tokenize(jd)
    # remove common short words
    toks = [t for t in toks if len(t) > 2]
    uniq = []
    for t in toks:
        if t not in uniq:
            uniq.append(t)
    return uniq

def _semantic_similarity(a: str, b: str) -> float:
    # simple string similarity via SequenceMatcher
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def score_resume(parsed: Dict[str, Any], job_description: str) -> Dict[str, Any]:
    """
    Very lightweight ATS scoring:
      - Find JD keywords in parsed['text']
      - coverage = matched / total
      - semantic = average similarity between JD and parsed text (coarse)
      - ats_score is weighted combination
    """
    text = ""
    if isinstance(parsed, dict):
        text = parsed.get("text", "") or ""
    else:
        text = str(parsed or "")

    jd = job_description or ""
    keywords = _unique_keywords(jd)
    total_keywords = len(keywords)
    found = []
    for kw in keywords:
        if re.search(r"\b" + re.escape(kw) + r"\b", text, flags=re.I):
            found.append(kw)

    coverage = (len(found) / total_keywords) if total_keywords > 0 else 0.0

    # semantic: compare JD to the longest block of text in resume (coarse)
    # simplified: compare full strings
    semantic = _semantic_similarity(jd, text)

    # ats score: 0..100
    ats_score = (coverage * 0.6 + semantic * 0.4) * 100

    return {
        "ats_score": round(float(ats_score), 2),
        "semantic": round(float(semantic), 3),
        "coverage": round(float(coverage), 3),
        "matched_keywords": found,
        "missing_keywords": [k for k in keywords if k not in found],
        "total_keywords": total_keywords,
    }
