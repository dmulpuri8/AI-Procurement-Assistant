from jinja2 import Template
from .thresholds import determine_solicitation_type
from .instrument import instrument_info

def render_solicitation(params: dict, template_path: str, policy: dict, clauses: dict) -> str:
    with open(template_path,'r') as f:
        tmpl = Template(f.read())
    p = dict(params)
    p["solicitation_type"] = determine_solicitation_type(p["internal_budget"], policy)
    instr = p.get("instrument","RFP — Request for Proposal")
    p["instrument"] = instr
    p["instrinfo"] = instrument_info(instr)
    # Label
    if instr.startswith("RFI"):
        doc_label = "Request for Information (RFI)"
    elif instr.startswith("Sources Sought"):
        doc_label = "Sources Sought / Market Research Notice"
    elif instr.startswith("RFQ"):
        doc_label = "Request for Quotation (RFQ)"
    elif instr.startswith("IFB"):
        doc_label = "Invitation for Bid (IFB)"
    elif instr.startswith("RFTOP"):
        doc_label = "Task Order Request (RFTOP)"
    elif instr.startswith("BPA Call"):
        doc_label = "BPA Call"
    elif instr.startswith("OTA"):
        doc_label = "Other Transaction (OTA)"
    elif instr.startswith("BAA"):
        doc_label = "Broad Agency Announcement (BAA)"
    elif instr.startswith("CSO"):
        doc_label = "Commercial Solutions Opening (CSO)"
    elif instr.startswith("Sole Source"):
        doc_label = "Sole Source (J&A)"
    elif instr.startswith("RLP"):
        doc_label = "Request for Lease Proposals (RLP)"
    elif instr.startswith("Micro-Purchase"):
        doc_label = "Micro-Purchase Notice"
    else:
        doc_label = "Request for Proposal (RFP)"
    p["doc_label"] = doc_label
    p["instrument_extras"] = p.get("instrument_extras")
    return tmpl.render(**p, policy=policy, clauses=clauses)
