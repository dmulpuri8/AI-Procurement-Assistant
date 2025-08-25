import sys, json, zipfile
from pathlib import Path
from io import BytesIO
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE = ROOT
DATA = BASE/"data"

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

st.title("Phase 3 — Publication (Refined)")

if not (DATA/"current_solicitation.json").exists():
    st.warning("Please complete Phase 1 first.")
    st.stop()

params = json.loads((DATA/"current_solicitation.json").read_text())

st.subheader("Public Synopsis")
st.write(f"**Instrument:** {params.get('instrument','')}")
st.write(f"**Title:** {params.get('title','')}")
st.write(f"**Publish Date:** {params.get('dates',{}).get('publish','')} — **Proposal Due:** {params.get('dates',{}).get('proposal_due','')}")

with st.expander("Optional: Notice Details"):
    synopsis = st.text_area("Short Synopsis", value=f"{params.get('title','Solicitation')} — competitive opportunity issued by the Agency. See the draft document for full details.")
    contact_name = st.text_input("POC Name", value="Procurement Officer")
    contact_email = st.text_input("POC Email", value="procurement@example.gov")
    submission_channel = st.selectbox("Submission Channel", ["Portal","Email","Hardcopy"], index=0)
    questions_due = st.text_input("Questions Due (ISO date or 'TBD')", value=params.get('dates',{}).get('questions_due','TBD'))
    answers_posted = st.text_input("Answers Posted (ISO date or 'TBD')", value=params.get('dates',{}).get('answers_posted','TBD'))

def make_pdf(title, lines):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=LETTER)
    w, h = LETTER; m=50; y=h-m
    c.setTitle(title)
    c.setAuthor("AI Procurement Demo")
    c.setFont("Times-Roman", 11)
    for ln in lines.splitlines():
        if y < m + 24:
            c.showPage(); c.setFont("Times-Roman", 11); y=h-m
        c.drawString(m, y, ln[:110]); y -= 14
    c.save()
    return buf.getvalue()

notice_text = f"""PUBLIC NOTICE
Title: {params.get('title','')}
Instrument: {params.get('instrument','')}
Publish: {params.get('dates',{}).get('publish','')}
Proposal Due: {params.get('dates',{}).get('proposal_due','')}
Anticipated Award: {params.get('dates',{}).get('anticipated_award','')}
Submission: {submission_channel}
Synopsis: {synopsis}
"""

schedule_text = f"""SCHEDULE OF EVENTS
Publish: {params.get('dates',{}).get('publish','')}
Questions Due: {questions_due}
Answers Posted: {answers_posted}
Proposal Due: {params.get('dates',{}).get('proposal_due','')}
Anticipated Award: {params.get('dates',{}).get('anticipated_award','')}
"""

contact_text = f"""CONTRACTING POINT OF CONTACT
Name: {contact_name}
Email: {contact_email}
"""

st.download_button("Download Public Notice (PDF)", data=make_pdf("Public Notice", notice_text), file_name="public_notice.pdf", mime="application/pdf")
st.download_button("Download Schedule of Events (PDF)", data=make_pdf("Schedule of Events", schedule_text), file_name="schedule_of_events.pdf", mime="application/pdf")

if st.button("Create Posting Package (ZIP)"):
    zbuf = BytesIO()
    with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("public_notice.pdf", make_pdf("Public Notice", notice_text))
        z.writestr("schedule_of_events.pdf", make_pdf("Schedule of Events", schedule_text))
        z.writestr("contact.txt", contact_text)
        z.writestr("submission_instructions.txt", f"Submit via: {submission_channel}. Reference the solicitation title and number.")
        meta = json.dumps({
            "title": params["title"],
            "instrument": params.get("instrument"),
            "publish_date": params["dates"]["publish"],
            "proposal_due": params["dates"]["proposal_due"],
            "anticipated_award": params["dates"]["anticipated_award"],
            "submission_channel": submission_channel
        }, indent=2)
        z.writestr("metadata.json", meta)
    st.download_button("Download Posting Package", data=zbuf.getvalue(), file_name="posting_package.zip", mime="application/zip")
