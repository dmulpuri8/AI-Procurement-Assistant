import json
from typing import List, Dict

def load_past_projects(csv_path: str) -> List[Dict]:
    rows = []
    with open(csv_path, newline='') as f:
        for i, line in enumerate(f):
            if i==0: continue
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) < 5: continue
            vendor, agency, ptype, year, rating = parts
            rows.append({"vendor": vendor, "agency": agency, "project_type": ptype, "year": year, "rating": rating})
    return rows

def recommend_sole_source(title: str, sow_text: str, past_csv: str, historical_json: str) -> Dict:
    past = load_past_projects(past_csv)
    hist = json.load(open(historical_json,'r'))
    candidates = {}
    for r in past:
        if "modernization" in r["project_type"].lower() and r["rating"].lower() in ("excellent","good"):
            candidates[r["vendor"]] = candidates.get(r["vendor"], 0) + 1
    prior_bidders = set(hist.get(title, []))
    overlap = [v for v in candidates if v in prior_bidders]
    suggestion = overlap[0] if len(overlap)==1 else None
    return {"strong_candidates": sorted(candidates.keys()), "prior_bidders": sorted(prior_bidders), "sole_source_suggestion": suggestion}
