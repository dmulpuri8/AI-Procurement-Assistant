from typing import List, Tuple
import re
from .ai_models import summarize as _summarize, semantic_similarity as _semantic, nlp_status as _nlp_status

_MONEY_RE = re.compile(r"\$\s*([0-9][0-9,]*(?:\.[0-9]{2})?)")
_DATE_RE  = re.compile(r"\b(20[0-9]{2}|19[0-9]{2})\b")
_ORG_RE   = re.compile(r"\b([A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)*\s(?:LLC|Inc|Corp|Partners|Systems))\b")

def summarize_text(text: str) -> str:
    return _summarize(text)

def semantic_score(requirement: str, text: str) -> float:
    return _semantic(requirement, text)

def extract_entities(text: str) -> List[Tuple[str, str]]:
    s = text or ""
    ents = []
    ents += [(m.group(0), "MONEY") for m in _MONEY_RE.finditer(s)]
    ents += [(m.group(0), "DATE")  for m in _DATE_RE.finditer(s)]
    ents += [(m.group(1), "ORG")   for m in _ORG_RE.finditer(s)]
    seen, out = set(), []
    for t,l in ents:
        if (t,l) not in seen:
            seen.add((t,l)); out.append((t,l))
    return out

def nlp_status():
    return _nlp_status()
