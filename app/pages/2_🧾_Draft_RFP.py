import sys, json
from pathlib import Path
from io import BytesIO
import streamlit as st
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_bot.policy_engine import load_policy
from ai_bot.drafting import render_solicitation

BASE = ROOT
DATA = BASE/"data"
TPL = BASE/"templates"
CLAUSES = BASE/"clauses"/"far.json"
POLICY_DIR = BASE/"policy"/"packs"

st.title("Phase 2 — Draft Document")

if not (DATA/"current_solicitation.json").exists():
    st.warning("Please complete Phase 1 first.")
    st.stop()

params = json.loads((DATA/"current_solicitation.json").read_text())
policy = load_policy(str(POLICY_DIR), params.get("jurisdiction","FED"))
clauses = json.loads(CLAUSES.read_text())

UP = DATA/"uploaded_templates"/f"{params.get('instrument','').replace('/','_').replace(' ','_')}.md"
tmpl_path = UP if UP.exists() else (TPL/"solicitation_template.md")
draft_md = render_solicitation(params, str(tmpl_path), policy, clauses)

def md_to_pdf_bytes(title, md_text):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=LETTER)
    width, height = LETTER
    margin = 50
    y = height - margin
    for line in (title + "\n\n" + md_text).splitlines():
        if y < margin + 20:
            c.showPage(); y = height - margin
        c.setFont("Times-Roman", 10)
        c.drawString(margin, y, line[:110])
        y -= 14
    c.save()
    return buf.getvalue()

pdf_bytes = md_to_pdf_bytes(params["title"], draft_md)
st.download_button("Download Draft (PDF)", data=pdf_bytes, file_name="draft.pdf", mime="application/pdf")
with st.expander("Preview Draft (Markdown)"):
    st.markdown(draft_md)

st.info("Proceed to Phase 3 — Publication.")
