from .utils import read_json, parse_metadata

def sam_clear(vendor_name: str, sam_db_path: str) -> bool:
    data = read_json(sam_db_path)
    for row in data:
        if row["vendor_name"].lower() == vendor_name.lower():
            return row["status"].lower()=="active"
    return False

def parse_vendor_compliance(text: str):
    md = parse_metadata(text)
    return {
        "sam": md.get("sam","unknown").lower()=="active",
        "vpat": md.get("vpat","missing").lower()=="provided",
        "sec889": md.get("section889","no").lower() in ("yes","true"),
        "baa_taa": md.get("baa/taa","unknown").lower() in ("compliant","yes","true") or md.get("baa_taa","unknown").lower() in ("compliant","yes","true")
    }

def preaward_gate(vendor_compliance: dict, policy: dict):
    comp = policy.get("compliance",{})
    result = {
      "sam": (not comp.get("check_sam_exclusions", True)) or vendor_compliance["sam"],
      "vpat": (not comp.get("require_vpat_508", False)) or vendor_compliance["vpat"],
      "sec889": (not comp.get("require_section_889_rep", False)) or vendor_compliance["sec889"],
      "baa_taa": (not comp.get("baa_taa_applicable", False)) or vendor_compliance["baa_taa"]
    }
    result["all_clear"] = all(result.values())
    return result
