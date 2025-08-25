import sys, json
from pathlib import Path
import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_bot.evm import build_schedule, build_invoice_plan

BASE = ROOT
DATA = BASE/"data"

st.title("Phase 6 — Monitoring & Finance (EVM + Invoices)")

if not (DATA/"current_solicitation.json").exists():
    st.warning("Please complete Phase 1 first.")
    st.stop()

params = json.loads((DATA/"current_solicitation.json").read_text())
if not params.get("dates",{}).get("anticipated_award"):
    st.info("Set Anticipated Award Date in Phase 1.")
    st.stop()

schedule = build_schedule(params["dates"]["anticipated_award"], int(params.get("project_duration_days",180)))
invoice = build_invoice_plan(schedule, float(params.get("internal_budget",0)))

st.subheader("Deliverables & EVM Milestones")
df_sched = pd.DataFrame(schedule)
st.dataframe(df_sched, use_container_width=True)

st.subheader("Invoice Schedule (Financial Report)")
df_inv = pd.DataFrame(invoice)
st.dataframe(df_inv, use_container_width=True)

st.bar_chart(df_inv.set_index("milestone")["amount"])

def report_pdf(title, schedule_df, invoice_df):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=LETTER)
    width, height = LETTER
    m = 40; y = height - m
    c.setFont("Times-Bold", 12); c.drawString(m, y, title); y -= 20
    c.setFont("Times-Roman", 10); c.drawString(m, y, "Deliverables & EVM Milestones:"); y -= 16
    for _, row in schedule_df.iterrows():
        line = f"- {row['name']}: due {row['due']} (EVM {int(row['evm_pct']*100)}%)"
        if y < m + 20: c.showPage(); y = height - m
        c.drawString(m, y, line[:110]); y -= 14
    y -= 10
    c.setFont("Times-Roman", 10); c.drawString(m, y, "Invoice Schedule:"); y -= 16
    for _, row in invoice_df.iterrows():
        line = f"- {row['milestone']}: ${row['amount']} on/after {row['invoice_on_or_after']} ({row['net_terms']})"
        if y < m + 20: c.showPage(); y = height - m
        c.drawString(m, y, line[:110]); y -= 14
    c.save()
    return buf.getvalue()

pdf = report_pdf("Financial Report", df_sched, df_inv)
st.download_button("Download Financial Report (PDF)", data=pdf, file_name="financial_report.pdf", mime="application/pdf")
st.download_button("Download Invoice Schedule (CSV)", data=df_inv.to_csv(index=False), file_name="invoice_schedule.csv", mime="text/csv")
