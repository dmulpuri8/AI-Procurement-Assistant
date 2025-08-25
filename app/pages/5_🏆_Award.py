import sys, json
from pathlib import Path
from io import BytesIO
import streamlit as st
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from jinja2 import Template

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_bot.evaluation import evaluate_bids
from ai_bot.policy_engine import load_policy
from ai_bot.nlp_utils import nlp_status, summarize_text, extract_entities, semantic_score

BASE = ROOT
DATA = BASE/"data"
TPL = BASE/"templates"
POLICY_DIR = BASE/"policy"/"packs"
SAM_DB = DATA/"sam_exclusions.json"

st.title("Phase 5 — Award")

if not (DATA/"current_solicitation.json").exists():
    st.warning("Please complete Phase 1 first.")
    st.stop()

params = json.loads((DATA/"current_solicitation.json").read_text())
policy = load_policy(str(POLICY_DIR), params.get("jurisdiction","FED"))

results = evaluate_bids(str(DATA/"proposals"), params, policy, str(SAM_DB))
nlp_on = st.sidebar.checkbox("Enable AI/NLP", value=True, key="nlp5")
sem_weight = st.sidebar.slider("Semantic weight (0–0.5)", 0.0, 0.5, 0.2, 0.05, key="sem5")
ok, err = nlp_status()

rows = []
for r in results:
    raw_text = Path(r.path).read_text()
    sem = semantic_score(params.get("scope_of_work",""), raw_text) if (nlp_on and ok) else 0.0
    model_score = round((1.0 - sem_weight)*r.scores.total + sem_weight*sem, 2)
    rows.append((r, model_score, sem))

instr = params.get("instrument","RFP — Request for Proposal")
if instr.startswith("RFI") or instr.startswith("Sources Sought"):
    st.info("RFI/Sources Sought: No award is made. Use insights to craft a future solicitation.")
    st.stop()
elif instr.startswith("IFB"):
    eligible = [(r,ms,sem) for (r,ms,sem) in rows if r.gates.get("all_clear") and r.compliance.eligible]
    if not eligible:
        st.warning("No vendor passes all gates + eligibility.")
        st.stop()
    winner = sorted(eligible, key=lambda t: t[0].raw_price)[0]
elif instr.startswith("Micro-Purchase"):
    mpt = policy.get("thresholds",{}).get("micro_purchase",0)
    eligible = [(r,ms,sem) for (r,ms,sem) in rows if r.gates.get("all_clear") and r.compliance.eligible and r.raw_price <= mpt]
    if not eligible:
        st.warning("No vendor under micro-purchase threshold; cannot award in micro-purchase mode.")
        st.stop()
    winner = sorted(eligible, key=lambda t: t[0].raw_price)[0]
else:
    eligible = [(r,ms,sem) for (r,ms,sem) in rows if r.gates.get("all_clear") and r.compliance.eligible]
    if not eligible:
        st.warning("No vendor passes all gates + eligibility.")
        st.stop()
    winner = sorted(eligible, key=lambda t: t[1], reverse=True)[0]

r, ms, sem = winner
st.success(f"Recommended Awardee: **{r.vendor_name}** (Model Score {ms})")

t = Template((TPL/"notice_award_template.md").read_text())
award_md = t.render(
    title=params["title"],
    awardee={
        "vendor_name": r.vendor_name,
        "scores": {"technical": r.scores.technical, "price": r.scores.price},
        "total_score": r.scores.total,
        "compliance": {"eligible": r.compliance.eligible},
        "sam_clear": True, "rep_889": True, "vpat": True, "baa_taa_ok": True
    },
    evaluation_weights=params["evaluation_weights"],
    selection_method=params["selection_method"],
    sem_weight=sem_weight, semantic_match=sem, model_score=ms
)

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

pdf = md_to_pdf_bytes("Notice of Award", award_md)
st.download_button("Download Notice of Award (PDF)", data=pdf, file_name="notice_of_award.pdf", mime="application/pdf")
with st.expander("Preview Award (Markdown)"):
    st.markdown(award_md)

st.info("Proceed to Phase 6 — Monitoring & Finance.")
