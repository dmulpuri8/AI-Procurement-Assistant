import sys, json
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_bot.evaluation import evaluate_bids
from ai_bot.policy_engine import load_policy
from ai_bot.nlp_utils import summarize_text, extract_entities, semantic_score, nlp_status
from ai_bot.sole_source import recommend_sole_source
from ai_bot.vendor_synth import synthesize_proposals

BASE = ROOT
DATA = BASE/"data"
POLICY_DIR = BASE/"policy"/"packs"
SAM_DB = DATA/"sam_exclusions.json"

st.title("Phase 4 — Proposal Intake & AI Evaluation")

if not (DATA/"current_solicitation.json").exists():
    st.warning("Please complete Phase 1 first.")
    st.stop()

params = json.loads((DATA/"current_solicitation.json").read_text())
policy = load_policy(str(POLICY_DIR), params.get("jurisdiction","FED"))

with st.expander("Generate Synthetic Vendor Proposals"):
    n = st.slider("How many vendors to generate?", 1, 30, 10)
    price_center = st.number_input("Target price center (USD)", 10000, 1000000, int(float(params.get("internal_budget",200000))*0.9), step=5000)
    if st.button("Generate Now"):
        synthesize_proposals(DATA/"proposals", params, n=n, price_center=price_center)
        st.success(f"Generated {n} synthetic proposals into data/proposals.")

nlp_on = st.sidebar.checkbox("Enable AI/NLP", value=True, key="nlp4")
sem_weight = st.sidebar.slider("Semantic weight (0–0.5)", 0.0, 0.5, 0.2, 0.05, key="sem4")
ok, err = nlp_status()
if nlp_on and err:
    st.sidebar.info(err)

ss = recommend_sole_source(params["title"], params.get("scope_of_work",""), str(DATA/"past_projects.csv"), str(DATA/"historical_bidders.json"))
with st.expander("Sole Source Analysis (Heuristic)"):
    st.write("Strong candidates:", ", ".join(ss["strong_candidates"]) or "None")
    st.write("Prior bidders:", ", ".join(ss["prior_bidders"]) or "None")
    st.write("**Sole-source suggestion:**", ss["sole_source_suggestion"] or "No")

results = evaluate_bids(str(DATA/"proposals"), params, policy, str(SAM_DB))

rows = []
for r in results:
    raw_text = Path(r.path).read_text()
    if nlp_on and ok:
        summary = summarize_text(raw_text)
        ents = extract_entities(raw_text)
        sem = semantic_score(params.get("scope_of_work",""), raw_text)
    else:
        summary = summarize_text(raw_text)
        ents = extract_entities(raw_text)
        sem = 0.0
    model_score = round((1.0 - sem_weight)*r.scores.total + sem_weight*sem, 2)
    rows.append({
        "Vendor": r.vendor_name,
        "Gate: All Clear": r.gates.get("all_clear", False),
        "Eligible (rules)": r.compliance.eligible,
        "Tech": r.scores.technical,
        "Price": r.scores.price,
        "Total": r.scores.total,
        "Semantic%": sem,
        "Model Score": model_score,
        "Missing": "; ".join(r.compliance.missing_items),
        "Summary": summary,
        "Entities": ", ".join([f"{t}<{l}>" for t,l in ents]),
    })

df = pd.DataFrame(rows).sort_values(by=["Gate: All Clear","Eligible (rules)","Model Score"], ascending=[False,False,False])
st.dataframe(df, use_container_width=True)

instr = params.get("instrument","RFP — Request for Proposal")
if instr.startswith("RFI") or instr.startswith("Sources Sought"):
    st.subheader("Market Research Rollup")
    st.caption("RFI/Sources Sought: No award scoring performed.")
elif instr.startswith("IFB"):
    st.subheader("Sealed Bid Mode — Lowest Price among responsive/responsible")
    st.caption("Award basis: Lowest responsive, responsible bid (FAR Part 14).")
elif instr.startswith("Micro-Purchase"):
    st.subheader("Micro-Purchase Mode")
    mpt = policy.get("thresholds",{}).get("micro_purchase",0)
    st.write(f"Micro-Purchase Threshold: ${mpt}")

st.info("Proceed to Phase 5 — Award.")
