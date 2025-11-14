# frontend/app.py
import streamlit as st
import requests
import os
import io
from pathlib import Path

st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif !important;
    color: #E4E7EB !important;
}

/* Global text */
* {
    color: #E4E7EB !important;
}

/* Page background */
.stApp {
    background-color: #0D1117 !important;
}

/* Input text area */
textarea, .stTextInput input {
    color: #E4E7EB !important;
    background-color: #1A1F24 !important;
    border: 1px solid #2A2F35 !important;
}

/* File uploader text color */
.uploadedFileText, .stFileUploader label, .stFileUploader div {
    color: #E4E7EB !important;
}

/* Buttons */
.stButton>button {
    background-color: #21262D !important;
    color: #E4E7EB !important;
    border: 1px solid #30363D !important;
    padding: 0.6rem 1.2rem;
    border-radius: 6px !important;
    font-weight: 500 !important;
}

.stButton>button:hover {
    background-color: #30363D !important;
    border: 1px solid #3E4450 !important;
}

/* Headings readable */
h1, h2, h3, h4, h5 {
    color: #F0F3F6 !important;
}

/* Status boxes */
.stAlert, .stInfo, .stError, .stSuccess  {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


# --- Config ---
st.set_page_config(page_title="AI Resume Optimizer", layout="wide", initial_sidebar_state="collapsed")
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
PARSE_URL = f"{API_URL}/parse"
SCORE_URL = f"{API_URL}/score"
ENHANCE_URL = f"{API_URL}/enhance"
GEN_DOCX_URL = f"{API_URL}/generate/docx"
GEN_PDF_URL = f"{API_URL}/generate/pdf"

# --- Styling: professional, neutral palette ---
st.markdown(
    """
    <style>
    /* Import system fonts fallback for reliability */
    :root{
      --bg:#f6f7f9; --card:#ffffff; --muted:#6b7280; --accent:#0f1724; --primary:#0b5cff;
      --btn-bg: #0b5cff; --btn-contrast: #fff;
    }
    .main > div { background: var(--bg); }
    .app-header { padding: 28px 48px 10px 48px; }
    .brand { font-size:28px; font-weight:700; color:var(--accent); letter-spacing:-0.2px; }
    .tagline { color:var(--muted); margin-top:4px; }
    .card {
      background: var(--card);
      border-radius:12px;
      padding:22px;
      box-shadow: 0 6px 20px rgba(19,24,31,0.06);
      margin-bottom:18px;
    }
    .muted { color:var(--muted); }
    .controls .stButton>button {
      background: var(--btn-bg);
      color: var(--btn-contrast);
      border-radius:8px;
      padding:10px 14px;
      font-weight:600;
      border: none;
    }
    .secondaryButton .stButton>button {
      background: transparent;
      color: var(--accent);
      border: 1px solid #e6e9ef;
    }
    .small-muted { color:#94a3b8; font-size:13px; }
    pre, code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", monospace; font-size:13px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header ---
st.markdown('<div class="app-header"><div class="brand">AI Resume Optimizer</div>'
            '<div class="tagline">Parse · Score · Enhance · Export — enterprise-grade resume tooling</div></div>',
            unsafe_allow_html=True)

# --- Page grid: left form, right status/output ---
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Upload & Job Description")
    uploaded_file = st.file_uploader("Resume (PDF/DOCX)", type=["pdf", "docx"], help="Recommended: PDF. Max 200MB.")
    st.write("", "")  # small spacer
    job_description = st.text_area("Job description (paste here)", height=160, placeholder="e.g. Machine learning internship — Python, scikit-learn, data pipelines")
    st.markdown('<div class="small-muted">Tip: supply a clear JD to improve ATS scoring and enhancement relevance.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card controls">', unsafe_allow_html=True)
    st.subheader("Actions")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("Parse Resume"):
            if uploaded_file is None:
                st.error("Please upload a resume file first.")
            else:
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    res = requests.post(PARSE_URL, files=files, timeout=60)
                    if res.ok:
                        st.session_state["parsed"] = res.json()
                        st.session_state["enhanced"] = None
                        st.success("Resume parsed successfully.")
                    else:
                        st.error(f"API error {res.status_code}: {res.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

    with col2:
        if st.button("Get ATS Score"):
            if not st.session_state.get("parsed"):
                st.error("Parse resume first.")
            else:
                payload = {"parsed": st.session_state["parsed"], "job_description": job_description or ""}
                try:
                    res = requests.post(SCORE_URL, json=payload, timeout=60)
                    if res.ok:
                        st.session_state["score"] = res.json()
                        st.success("ATS score retrieved.")
                    else:
                        st.error(f"API error {res.status_code}: {res.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

    with col3:
        if st.button("Enhance Resume"):
            if not st.session_state.get("parsed"):
                st.error("Parse resume first.")
            else:
                payload = {"parsed": st.session_state["parsed"], "job_description": job_description or ""}
                try:
                    res = requests.post(ENHANCE_URL, json=payload, timeout=120)
                    if res.ok:
                        st.session_state["enhanced"] = res.json()
                        st.success("Resume enhanced.")
                    else:
                        st.error(f"API error {res.status_code}: {res.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Export buttons area
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Export")
    colA, colB = st.columns([1,1])
    with colA:
        if st.button("Download DOCX"):
            if not st.session_state.get("enhanced"):
                st.error("Enhance resume first.")
            else:
                try:
                    payload = {"data": st.session_state["enhanced"]}
                    # Server should return file bytes or path; try to stream bytes
                    r = requests.post(GEN_DOCX_URL, json=payload, stream=True, timeout=120)
                    if r.ok:
                        # If server returns streamed file content:
                        content_type = r.headers.get("content-type", "")
                        if "application" in content_type:
                            data = r.content
                            st.download_button("Download enhanced.docx", data, file_name="enhanced_resume.docx", mime=content_type)
                        else:
                            # fallback: attempt to parse JSON response with path
                            info = r.json()
                            p = info.get("path")
                            if p and Path(p).exists():
                                with open(p, "rb") as f:
                                    st.download_button("Download enhanced.docx", f.read(), file_name=info.get("filename", "enhanced.docx"))
                            else:
                                st.error("DOCX generation succeeded on server but file not accessible.")
                    else:
                        st.error(f"API error {r.status_code}: {r.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

    with colB:
        if st.button("Download PDF"):
            if not st.session_state.get("enhanced"):
                st.error("Enhance resume first.")
            else:
                try:
                    payload = {"data": st.session_state["enhanced"]}
                    r = requests.post(GEN_PDF_URL, json=payload, stream=True, timeout=120)
                    if r.ok:
                        content_type = r.headers.get("content-type", "")
                        if "application/pdf" in content_type or r.headers.get("content-disposition"):
                            data = r.content
                            st.download_button("Download enhanced.pdf", data, file_name="enhanced_resume.pdf", mime="application/pdf")
                        else:
                            info = r.json()
                            p = info.get("path")
                            if p and Path(p).exists():
                                with open(p, "rb") as f:
                                    st.download_button("Download enhanced.pdf", f.read(), file_name=info.get("filename", "enhanced.pdf"))
                            else:
                                st.error("PDF generation succeeded on server but file not accessible.")
                    else:
                        st.error(f"API error {r.status_code}: {r.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Status & Output")
    # Parsed raw text
    if st.session_state.get("parsed"):
        st.markdown("**Parsed resume (preview)**")
        parsed_text = st.session_state["parsed"].get("text", "")
        st.code(parsed_text[:20000])
    else:
        st.info("No parsed resume yet.")

    # ATS score result
    if st.session_state.get("score"):
        st.markdown("**ATS Score**")
        st.json(st.session_state["score"])

    # Enhanced resume json
    if st.session_state.get("enhanced"):
        st.markdown("**Enhanced resume (JSON preview)**")
        st.json(st.session_state["enhanced"])
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer / debug info (small muted) ---
st.markdown(
    f'<div style="margin-top:18px;color:#94a3b8;font-size:13px">Backend: {API_URL} &nbsp; • &nbsp; Streamlit UI</div>',
    unsafe_allow_html=True,
)
