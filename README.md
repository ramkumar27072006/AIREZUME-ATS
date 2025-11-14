
---

# **AIREZUME-ATS**

Advanced AI-driven Resume Parsing, ATS Scoring, Enhancement, and Document Generation System

---

## **Overview**

AIREZUME-ATS is a full-stack, production-ready platform for automated resume intelligence.
It provides a complete workflow for:

* Parsing resumes (PDF/DOCX)
* Computing ATS scores and keyword relevance
* Enhancing content using AI-powered rewriting
* Exporting refined resumes to DOCX and PDF
* Providing an intuitive UI through a modern Streamlit application

Built with a modular architecture, AIREZUME-ATS is suitable for academic, enterprise, and SaaS-grade deployment.

---

## **Key Features**

### **Resume Parsing**

* Extracts structured text from PDF/DOCX
* Robust fallback extraction
* Handles multi-column and multi-page layouts

### **ATS Scoring Engine**

* Semantic similarity matching using embedding models
* Keyword extraction and coverage analysis
* Composite scoring system with detailed breakdown

### **Resume Enhancement Engine**

* AI-based rewriting for clarity, impact, and ATS alignment
* Bullet-point optimization
* Job-specific content adaptation

### **Document Export**

* DOCX export through python-docx
* PDF export through ReportLab
* Modern and consistent layout formatting

### **Frontend Application**

* Clean Streamlit interface
* Session-based workflow
* Local and deployed API support
* Dark-theme optimized

---

## **Technology Stack**

| Layer      | Technology                          |
| ---------- | ----------------------------------- |
| Frontend   | Streamlit                           |
| Backend    | FastAPI                             |
| AI/NLP     | Transformers, Sentence-Transformers |
| Parsing    | PyPDF2, python-docx                 |
| Export     | python-docx, ReportLab              |
| Deployment | Render / Railway / Docker           |
| Language   | Python 3.10+                        |

---

## **Project Structure**

```
AIREZUME-ATS/
│── backend/
│   ├── main.py
│   ├── parser.py
│   ├── ats_score.py
│   ├── enhancer.py
│   ├── template_engine.py
│   ├── utils.py
│   └── requirements.txt
│
│── frontend/
│   ├── app.py
│   ├── styles.css
│   └── requirements.txt
│
│── README.md
│── LICENSE
│── .env (optional)
```

---

## **Local Setup Guide**

### 1. Clone

```
git clone <repository-url>
cd AIREZUME-ATS
```

### 2. Virtual Environment

```
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate # macOS/Linux
```

### 3. Install Dependencies

```
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 4. Start Backend

```
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Start Frontend

```
streamlit run frontend/app.py
```

Backend runs at:
`http://127.0.0.1:8000`

Frontend runs at:
`http://localhost:8501`

---

## **Environment Variables**

Create a `.env` file for local development:

```
API_URL=http://127.0.0.1:8000
```

On Render, add this as an environment variable in the frontend service.

---

## **Deployment (Render)**

### **Backend Deployment**

Create a **Render Web Service** with:

**Build Command**

```
pip install -r backend/requirements.txt
```

**Start Command**

```
uvicorn backend.main:app --host 0.0.0.0 --port 10000
```

### **Frontend Deployment**

Create a separate **Streamlit Render Web Service**:

**Build Command**

```
pip install -r frontend/requirements.txt
```

**Start Command**

```
streamlit run frontend/app.py --server.address=0.0.0.0 --server.port=10000
```

Set environment variable for frontend:

```
API_URL = https://<your-backend-service>.onrender.com
```

---

## **Future Scope**

### Authentication & User Accounts

* JWT login
* OAuth (Google, LinkedIn)

### Landing Page & SaaS Interface

* Marketing site with conversion-focused UI
* Pricing, FAQ, documentation pages

### Database Integration

* PostgreSQL for resume history and user profiles
* Admin analytics dashboard

### Payments Integration

* Stripe subscriptions
* Tiered pricing models

### Template Marketplace

* Multiple DOCX/PDF resume templates
* Customizable typography themes

### Job Intelligence Add-ons

* Automatic job description parsing
* Skill-gap estimation
* Role-specific optimization heuristics

---

# **License: MIT License**

