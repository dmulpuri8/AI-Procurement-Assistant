from typing import Tuple, List, Dict
from pathlib import Path
import re

def _read_pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        parts = []
        for page in reader.pages:
            try:
                parts.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join(parts)
    except Exception as e:
        return ""

def _read_docx_text(path: Path) -> str:
    try:
        import docx
        doc = docx.Document(str(path))
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""

def extract_sections(raw: str) -> List[Tuple[str,str]]:
    if not raw:
        return []
    text = raw.replace("\r","")
    pattern = re.compile(r"^(\s*\d+\.?\s+[A-Z][^\n]{2,})$", re.M)
    idxs = [(m.start(), m.group(0).strip()) for m in pattern.finditer(text)]
    known = ["Introduction","Vendor Instructions","Evaluation Criteria","Compliance Matrix","Pricing Details","Scope of Work","Table of Contents"]
    for k in known:
        for m in re.finditer(rf"^\s*{re.escape(k)}\s*$", text, re.M|re.I):
            idxs.append((m.start(), m.group(0).strip()))
    idxs = sorted(set(idxs), key=lambda t: t[0])
    sections = []
    for i,(pos,title) in enumerate(idxs):
        end = idxs[i+1][0] if i+1<len(idxs) else len(text)
        body = text[pos:end].split("\n",1)[-1]
        sections.append((title.strip(), body.strip()))
    return sections

def to_markdown_template(sections: List[Tuple[str,str]], params_keys: Dict[str,str]) -> str:
    out = []
    out.append("# {{ doc_label }}: {{ title }}\n")
    out.append("## 1. Document Type & Notes")
    out.append("- Instrument: **{{ instrument }}**")
    out.append("- Summary: {{ instrinfo.summary }}")
    out.append("- Award Basis: {{ instrinfo.award_basis }}")
    out.append("- Regulatory Notes: {{ instrinfo.reg_notes }}")
    out.append("{% if instrument_extras %}- Instrument Extras: {{ instrument_extras }}{% endif %}\n")
    out.append("## 2. Background & Scope of Work\n{{ scope_of_work }}\n")
    out.append("## 3. Key Dates")
    out.append("- Publication Date: {{ dates.publish }}")
    out.append("- Proposal Due: {{ dates.proposal_due }}")
    out.append("- Anticipated Award: {{ dates.anticipated_award }}")
    out.append("- Period of Performance: {{ project_duration_days }} days\n")
    out.append("## 4. Response Instructions")
    out.append("- Required Sections: {{ response_instructions.sections | join(', ') }}")
    out.append("- Page Limit: {{ response_instructions.page_limit }}")
    out.append("- Accepted Formats: {{ response_instructions.format | join(', ') }}")
    out.append("- Submission Method: {{ response_instructions.submission_method }}\n")
    out.append("## 5. Evaluation")
    out.append("- Method: {{ selection_method }}")
    out.append("- Weights: Technical {{ evaluation_weights.technical*100 }}% / Price {{ evaluation_weights.price*100 }}%\n")
    for title, body in sections:
        t = title.lower()
        if any(k in t for k in ["vendor instructions","evaluation criteria","compliance matrix","pricing details"]):
            out.append(f"## {title.strip()}")
            out.append(body.strip()[:4000])
            out.append("")
    out.append("## 6. Policy & Clauses")
    out.append("- Type by Budget: **{{ solicitation_type }}**")
    out.append("{% for cid, title in clauses.items() -%}")
    out.append("- FAR {{ cid }} — {{ title }}")
    out.append("{% endfor -%}")
    return "\n".join(out)

def ingest_to_md_template(path: Path) -> str:
    ext = path.suffix.lower()
    raw = ""
    if ext==".pdf":
        raw = _read_pdf_text(path)
    elif ext==".docx":
        raw = _read_docx_text(path)
    else:
        raw = path.read_text(errors="ignore")
    secs = extract_sections(raw)
    md = to_markdown_template(secs, {})
    return md
