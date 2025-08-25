# AI Procurement — Multipage Demo v4 (Dynamic, Industry-Refined)

**What’s new in v4**  
- Industry-style default template: TOC, schedule of events, eligibility, compliance matrix, pricing.  
- Phase 3 Publication: public notice PDF, schedule-of-events PDF, contact block + posting package ZIP.  
- Sample data: ≥10 vendors, ≥12 proposals, expanded past-performance/SAM/vehicle-holder sets.  
- Sample documents: `sample_docs/` per-instrument drafts, plus RFP public notice and award.  

## Run (Python 3.13 quick path)
```bash
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements-3.13.txt
python -m streamlit run app/app.py
```

> To enable embeddings/summarization, use Python **3.12** and install `requirements-ml.txt` instead.
