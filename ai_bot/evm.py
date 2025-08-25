from datetime import date, timedelta

def build_schedule(award_iso: str, duration_days: int):
    y,m,d = [int(x) for x in award_iso.split("-")]
    start = date(y,m,d)
    milestones = [
      ("Project Kickoff", 0, 0.05),
      ("Discovery Complete", int(duration_days*0.15), 0.15),
      ("Architecture & Pilot", int(duration_days*0.35), 0.40),
      ("Rollout 50%", int(duration_days*0.65), 0.70),
      ("Go-Live", int(duration_days*0.90), 0.90),
      ("Closeout & KT", duration_days, 1.00)
    ]
    out = []
    for name, offset, evm in milestones:
        out.append({"name": name, "due": str(start + timedelta(days=offset)), "evm_pct": evm})
    return out

def build_invoice_plan(schedule, budget):
    out = []
    for i, ms in enumerate(schedule, start=1):
        amount = round(budget * (ms["evm_pct"] - (schedule[i-2]["evm_pct"] if i>1 else 0)), 2)
        out.append({"milestone": ms["name"], "invoice_on_or_after": ms["due"], "amount": amount, "net_terms": "Net 30"})
    return out
