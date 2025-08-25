import sys, json
from pathlib import Path
import streamlit as st
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_bot.policy_engine import load_policy
from ai_bot.instrument import INSTRUMENTS, instrument_info
from ai_bot.template_ingest import ingest_to_md_template

BASE = ROOT
DATA = BASE/"data"
POLICY_DIR = BASE/"policy"/"packs"

st.title("Phase 1 — Solicitation Initiation")
policy_code = st.sidebar.selectbox("Policy Pack", ["FED","STATE_X"], index=0, key="policy1")
policy = load_policy(str(POLICY_DIR), policy_code)

params = {}
if (DATA/"sample_solicitation.json").exists():
    params = json.loads((DATA/"sample_solicitation.json").read_text())

with st.form("init"):
    params["instrument"] = st.selectbox("Solicitation Instrument", INSTRUMENTS, index=INSTRUMENTS.index(params.get("instrument","RFP — Request for Proposal")) if params.get("instrument") in INSTRUMENTS else INSTRUMENTS.index("RFP — Request for Proposal"))
    info = instrument_info(params["instrument"])
    with st.expander("Instrument Details"):
        st.markdown(f"**Summary:** {info['summary']}\n\n**Award Basis:** {info['award_basis']}\n\n**Regulatory Notes:** {info['reg_notes']}")
    # instrument extras
    extras = params.get("instrument_extras", {})
    if info["extra_fields"]:
        st.subheader("Instrument Extras")
        for fld in info["extra_fields"]:
            key = fld.lower().replace(' ','_').replace('/','_').replace('(','').replace(')','')
            if fld.startswith("Vehicle Type"):
                extras["vehicle_type_idiq_gwac_bpa"] = st.selectbox("Vehicle Type", ["","IDIQ","GWAC","BPA"], index=0)
            elif fld.startswith("Vehicle Name/Number"):
                extras["vehicle_name_number"] = st.text_input("Vehicle Name/Number", value=extras.get("vehicle_name_number",""))
            else:
                extras[key] = st.text_input(fld, value=extras.get(key, ""))
    params["instrument_extras"] = extras

    # Upload custom template (PDF/DOCX) for this instrument
    upload = st.file_uploader("Upload custom template (PDF or DOCX) for this instrument", type=["pdf","docx"], accept_multiple_files=False)
    if upload is not None:
        TPL_DIR = DATA / "uploaded_templates"
        TPL_DIR.mkdir(parents=True, exist_ok=True)
        suffix = ".pdf" if upload.type=="application/pdf" or upload.name.lower().endswith(".pdf") else ".docx"
        raw_path = TPL_DIR / f"{params['instrument'].replace('/','_').replace(' ','_')}{suffix}"
        raw_path.write_bytes(upload.read())
        md = ingest_to_md_template(raw_path)
        (TPL_DIR / f"{params['instrument'].replace('/','_').replace(' ','_')}.md").write_text(md)
        st.success("Template uploaded and ingested. It will be used in Phase 2 for drafting.")

    params["title"] = st.text_input("Title", value=params.get("title","Data Center Modernization Services"))
    params["scope_of_work"] = st.text_area("Scope of Work", height=180, value=params.get("scope_of_work",""))
    c1,c2,c3 = st.columns(3)
    with c1:
        params.setdefault("dates",{})
        params["dates"]["publish"] = st.date_input("Publish Date").isoformat()
    with c2:
        params["dates"]["proposal_due"] = st.date_input("Proposal Due Date").isoformat()
    with c3:
        params["dates"]["anticipated_award"] = st.date_input("Anticipated Award Date").isoformat()
    params["project_duration_days"] = st.number_input("Project Duration (days)", 1, value=params.get("project_duration_days",240))
    params["internal_budget"] = st.number_input("Internal Budget (USD — hidden from vendors)", 0, value=params.get("internal_budget",250000))

    vr = params.get("vendor_requirements", {"min_years_exp":5,"min_projects":3,"certs":["PMP"]})
    col4,col5 = st.columns(2)
    with col4:
        vr["min_years_exp"] = st.number_input("Min Years Experience", 0, value=vr.get("min_years_exp",5))
    with col5:
        vr["min_projects"] = st.number_input("Min Past Projects", 0, value=vr.get("min_projects",3))
    vr["certs"] = [c.strip() for c in st.text_input("Required Certifications (comma-separated)", value=",".join(vr.get("certs",[]))).split(",") if c.strip()]
    params["vendor_requirements"] = vr

    ri = params.get("response_instructions", {"sections":["Executive Summary","Technical","Management","Past Performance","Price"],"page_limit":30,"format":["PDF"],"submission_method":"Portal"})
    ri["sections"] = [s.strip() for s in st.text_input("Required Sections", value=",".join(ri.get("sections",[]))).split(",") if s.strip()]
    ri["page_limit"] = st.number_input("Page Limit", 1, value=ri.get("page_limit",30))
    ri["format"] = [f.strip() for f in st.text_input("Accepted Formats", value=",".join(ri.get("format",["PDF"]))).split(",") if f.strip()]
    ri["submission_method"] = st.selectbox("Submission Method", ["Portal","Email","Hardcopy"], index=0)
    params["response_instructions"] = ri

    ew = params.get("evaluation_weights", {"technical":0.7,"price":0.3})
    if params["instrument"].startswith("IFB"):
        base_tech = 0.0
    elif params["instrument"].startswith("RFQ") or params["instrument"].startswith("Micro-Purchase"):
        base_tech = 0.4
    else:
        base_tech = ew.get("technical",0.7)
    ew["technical"] = st.slider("Technical Weight", 0.0, 1.0, base_tech, 0.05)
    ew["price"] = round(1.0 - ew["technical"], 2)
    params["evaluation_weights"] = ew

    # Optional Q&A dates for Phase 2/3
    params["dates"]["questions_due"] = st.text_input("Questions Due (optional, ISO date)", value=params["dates"].get("questions_due",""))
    params["dates"]["answers_posted"] = st.text_input("Answers Posted (optional, ISO date)", value=params["dates"].get("answers_posted",""))

    params["jurisdiction"] = policy_code
    selection_method = st.selectbox("Source Selection Method", policy["source_selection"]["methods"], index=1 if "Best" in params.get("selection_method","Best Value Tradeoff") else 0)
    params["selection_method"] = selection_method
    submitted = st.form_submit_button("Validate & Save")

if submitted:
    if len(params.get("scope_of_work","").strip()) < 50:
        st.error("Scope too short (>= 50 chars).")
    else:
        (DATA/"current_solicitation.json").write_text(json.dumps(params, indent=2))
        st.success("Saved. Go to Phase 2 — Draft Document.")
