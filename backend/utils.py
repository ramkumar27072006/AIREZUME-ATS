# backend/utils.py
import re

def clean_whitespace(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip() if s else s
