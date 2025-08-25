INSTRUMENTS = [
    "RFI — Request for Information",
    "Sources Sought / Market Research Notice",
    "RFQ — Request for Quotation (SAP/GSA okay)",
    "IFB — Invitation for Bid (Sealed Bidding)",
    "RFP — Request for Proposal",
    "RFTOP / Task Order RFP (IDIQ/GWAC/BPA)",
    "BPA Call / Purchase under Existing BPA",
    "OTA — Other Transaction Authority",
    "BAA — Broad Agency Announcement",
    "CSO — Commercial Solutions Opening",
    "Sole Source (J&A / Limited Sources)",
    "RLP — Request for Lease Proposals (Facilities)",
    "Micro-Purchase (Gov Purchase Card)"
]
DETAILS = {
  "RFI — Request for Information": {"summary":"Market research only; no award.","award_basis":"N/A","reg_notes":"FAR Part 10","extra_fields":[]},
  "Sources Sought / Market Research Notice": {"summary":"Check vendor interest/size before a solicitation.","award_basis":"N/A","reg_notes":"FAR Part 10","extra_fields":[]},
  "RFQ — Request for Quotation (SAP/GSA okay)": {"summary":"Price quotes for well-defined requirements.","award_basis":"Best value (price-driven).","reg_notes":"FAR Part 13","extra_fields":["GSA Schedule (optional)"]},
  "IFB — Invitation for Bid (Sealed Bidding)": {"summary":"Clear specs; award to lowest responsive/responsible.","award_basis":"Lowest price.","reg_notes":"FAR Part 14","extra_fields":[]},
  "RFP — Request for Proposal": {"summary":"Complex requirements; evaluates tech, past perf, price.","award_basis":"Best Value Tradeoff or LPTA.","reg_notes":"FAR Part 15","extra_fields":[]},
  "RFTOP / Task Order RFP (IDIQ/GWAC/BPA)": {"summary":"Competed among vehicle holders.","award_basis":"Best Value or LPTA among holders.","reg_notes":"Order under vehicle.","extra_fields":["Vehicle Type (IDIQ/GWAC/BPA)","Vehicle Name/Number"]},
  "BPA Call / Purchase under Existing BPA": {"summary":"Streamlined ordering under BPA.","award_basis":"Best value among BPA holders.","reg_notes":"Order under BPA.","extra_fields":["BPA Number"]},
  "OTA — Other Transaction Authority": {"summary":"Non-FAR for R&D/prototypes.","award_basis":"Merit/innovation.","reg_notes":"Agency OTA policy.","extra_fields":["Consortium Name (optional)"]},
  "BAA — Broad Agency Announcement": {"summary":"Basic/applied research.","award_basis":"Scientific/technical merit.","reg_notes":"FAR 35.016.","extra_fields":[]},
  "CSO — Commercial Solutions Opening": {"summary":"Innovative commercial solutions.","award_basis":"Innovation/feasibility/value.","reg_notes":"Agency CSO.","extra_fields":[]},
  "Sole Source (J&A / Limited Sources)": {"summary":"Only one source or urgent/unique circumstances.","award_basis":"J&A; price reasonableness.","reg_notes":"FAR 6.302.","extra_fields":["Justification Summary"]},
  "RLP — Request for Lease Proposals (Facilities)": {"summary":"Facilities leasing.","award_basis":"Best value (rate/location/buildout).","reg_notes":"GSAR/agency policy.","extra_fields":["Location","Square Footage","Term (months)"]},
  "Micro-Purchase (Gov Purchase Card)": {"summary":"Below threshold; card-based.","award_basis":"Price & availability.","reg_notes":"FAR 13.201.","extra_fields":[]}
}
def instrument_info(name: str):
    return DETAILS.get(name, {"summary":"", "award_basis":"", "reg_notes":"", "extra_fields":[]})
