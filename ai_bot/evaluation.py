import os, glob
from dataclasses import dataclass
from typing import List, Dict, Any
from .utils import extract_price, contains_all
from .compliance import parse_vendor_compliance, preaward_gate

@dataclass
class Compliance:
    eligible: bool
    missing_items: List[str]

@dataclass
class Scores:
    technical: float
    price: float
    total: float

@dataclass
class BidResult:
    vendor_name: str
    compliance: Compliance
    scores: Scores
    raw_price: float
    gates: Dict[str,bool]
    vpat: bool
    rep_889: bool
    sam_clear: bool
    baa_taa_ok: bool
    path: str

REQUIRED_TECH_KEYWORDS = ["modernization","security","migration","runbook","architecture","pilot","rollout","knowledge transfer"]

def parse_vendor_name(text: str) -> str:
    for line in (text or "").splitlines():
        if line.lower().startswith("vendor:"):
            return line.split(":",1)[1].strip()
    return "Unknown Vendor"

def evaluate_bids(proposals_dir: str, params: Dict[str, Any], policy: dict, sam_db_path: str) -> List[BidResult]:
    paths = sorted(glob.glob(os.path.join(proposals_dir,"*.txt")))
    contents = [(p, open(p,'r').read()) for p in paths]

    prices = [extract_price(c) for _,c in contents] or [1.0]
    min_price = min(prices)

    results: List[BidResult] = []
    for p, text in contents:
        vendor = parse_vendor_name(text)
        vc = parse_vendor_compliance(text)
        gates = preaward_gate(vc, policy)

        missing = []
        instr = params["response_instructions"]
        for s in instr["sections"]:
            if s.lower() not in (text or "").lower():
                missing.append(f"Missing section: {s}")
        eligible = len(missing)==0

        tech_hits = contains_all(text, REQUIRED_TECH_KEYWORDS)
        coverage_ratio = (len(instr['sections'])-len(missing))/max(1,len(instr['sections']))
        tech_score = min(100.0, (tech_hits/len(REQUIRED_TECH_KEYWORDS))*80 + coverage_ratio*20)

        price = extract_price(text)
        price_score = 100.0 * (min_price / price) if price and price!=float('inf') else 0.0
        price_score = min(100.0, max(0.0, price_score))

        w = params["evaluation_weights"]
        total = round(tech_score*w["technical"] + price_score*w["price"], 2)

        results.append(BidResult(
            vendor_name=vendor,
            compliance=Compliance(eligible=eligible, missing_items=missing),
            scores=Scores(technical=round(tech_score,2), price=round(price_score,2), total=total),
            raw_price=price,
            gates=gates, vpat=vc["vpat"], rep_889=vc["sec889"], sam_clear=vc["sam"], baa_taa_ok=vc["baa_taa"],
            path=p
        ))
    return results
