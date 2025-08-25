def determine_solicitation_type(budget: float, policy: dict) -> str:
    th = policy.get("thresholds", {})
    if budget >= th.get("simplified_acquisition", 0):
        return "Competitive (Formal)"
    elif budget >= th.get("micro_purchase", 0):
        return "Three Quotes / Simplified"
    else:
        return "Micro-Purchase"
