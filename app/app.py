import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

st.set_page_config(page_title="AI Procurement — v4", layout="wide")
st.title("AI for Procurement & Solicitation — Multipage Demo v4")

st.markdown(
'''
**New in v4**: industry-refined template, beefed-up Publication artifacts, + larger sample data.

Use the **Pages** (left sidebar) to walk each phase:

1. **Initiation** — parameters + instrument + optional **PDF/DOCX template upload**
2. **Draft Document** — generates from uploaded or default template; download **PDF**
3. **Publication** — **Public Notice PDF**, **Schedule-of-Events PDF**, multi-file **Posting Package**
4. **Intake & Evaluation** — AI/NLP summaries, entities, semantic match + **Generate Vendors**
5. **Award** — instrument-aware logic; **Notice of Award (PDF)**
6. **Monitoring & Finance** — **EVM Milestones**, **Invoice Schedule (CSV/PDF)**
'''
)
