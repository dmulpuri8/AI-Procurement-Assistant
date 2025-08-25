import re, json, math, yaml
from typing import List, Dict, Any

def extract_price(text: str) -> float:
    m = re.search(r'\$\s*([0-9][0-9,]*(?:\.[0-9]{2})?)', text or "")
    if not m:
        return math.inf
    return float(m.group(1).replace(',', ''))

def contains_all(text: str, keywords: List[str]) -> int:
    text_low = (text or "").lower()
    return sum(1 for kw in keywords if kw.lower() in text_low)

def read_json(path: str) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)

def read_yaml(path: str) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def parse_metadata(text: str) -> Dict[str, str]:
    md = {}
    for line in (text or "").splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            md[k.strip().lower()] = v.strip()
    return md
