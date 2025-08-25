from typing import List, Dict
from pathlib import Path
import random

VENDOR_NAMES = [
  "RedOak Analytics","Cobalt Ridge","Sunset Systems","VertexIQ","NimbusWorks",
  "IronPeak Consulting","CedarByte","BlueOrbit","Orchid Labs","Granite Harbor",
  "HarborPoint Solutions","GreenPeak Systems","QuantumEdge LLC","CloudZen LLC","NorthStar Digital"
]

TECH_SNIPPETS = [
  "Zero-downtime cutovers with blue/green deployments.",
  "Automation-first using Infrastructure as Code (IaC).",
  "CIS Hardened images and continuous compliance scans.",
  "Hybrid cloud design with migration factory model.",
  "Runbook-driven operations and on-call rotations.",
  "Zero Trust network segmentation and identity hardening.",
  "EVM tracking with milestone-based invoicing."
]

def synthesize_proposals(out_dir: Path, params: Dict, n: int = 10, price_center: float = None):
    out_dir.mkdir(parents=True, exist_ok=True)
    budget = float(params.get("internal_budget", 200000))
    if price_center is None:
        price_center = budget * 0.9
    for i in range(n):
        name = random.choice(VENDOR_NAMES) + f" {random.randint(1,999)}"
        price = max(50000, random.gauss(price_center, price_center*0.15))
        sb = random.random() < 0.5
        vpat = random.random() < 0.85
        sec889 = True
        sam = True
        taa = random.random() < 0.9
        tech = " ".join(random.sample(TECH_SNIPPETS, k=3))
        txt = f"""Vendor: {name}
SAM: {'Active' if sam else 'Excluded'}
VPAT: {'Provided' if vpat else 'Missing'}
Section889: {'Yes' if sec889 else 'No'}
BAA/TAA: {'Compliant' if taa else 'Unknown'}
Interest: Yes
Size: {'Small Business' if sb else 'Large'}
Executive Summary: {params.get('title','Project')} execution with {tech}
Technical: {random.randint(4,10)} engineers, {random.randint(3,12)} years, {random.randint(6,24)} similar projects.
Management: PMO-led delivery with risk and issue logs.
Past Performance: Various public sector engagements.
Price: ${price:,.0f}
"""
        (out_dir/f"synth_vendor_{i+1}.txt").write_text(txt)
