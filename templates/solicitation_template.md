# {{ doc_label }}: {{ title }}

> **Confidentiality Notice.** This document contains proprietary information of the issuing agency and is provided solely for preparing a response. Unauthorized disclosure is prohibited.

## Table of Contents
1. Document Type & Notes  
2. Introduction & Purpose  
3. Background & Scope of Work  
4. Key Dates & Schedule of Events  
5. Vendor Minimum Requirements & Eligibility  
6. Response Instructions (Structure & Submission)  
7. Evaluation & Basis of Award  
8. Procurement Method & Thresholds (Policy)  
9. Compliance Requirements (Pre‑Award Gates)  
10. Compliance Matrix (Offeror Response)  
11. Pricing Details & Assumptions  
12. Clauses & Terms (Reference)  

---

## 1. Document Type & Notes
- **Instrument:** {{ instrument }}
- **Summary:** {{ instrinfo.summary }}
- **Award Basis:** {{ instrinfo.award_basis }}
- **Regulatory Notes:** {{ instrinfo.reg_notes }}
{% if instrument_extras %}- **Instrument Extras:** {{ instrument_extras }}{% endif %}

## 2. Introduction & Purpose
This Request is issued to obtain proposals for **{{ title }}**. The Agency intends to award to the Offeror providing the best value in accordance with Section 7.

## 3. Background & Scope of Work
{{ scope_of_work }}

## 4. Key Dates & Schedule of Events
- **Publication Date:** {{ dates.publish }}
- **Questions Due:** {{ dates.questions_due | default("TBD") }}
- **Answers Posted:** {{ dates.answers_posted | default("TBD") }}
- **Proposal Due:** {{ dates.proposal_due }}
- **Anticipated Award:** {{ dates.anticipated_award }}
- **Period of Performance:** {{ project_duration_days }} days

## 5. Vendor Minimum Requirements & Eligibility
- **Minimum Years of Experience:** {{ vendor_requirements.min_years_exp }}
- **Minimum Number of Past Projects:** {{ vendor_requirements.min_projects }}
{% if vendor_requirements.certs %}- **Required Certifications:** {{ vendor_requirements.certs | join(', ') }}{% endif %}

## 6. Response Instructions (Structure & Submission)
Offerors shall follow the structure below and observe page limits and formats.
- **Required Sections:** {{ response_instructions.sections | join(', ') }}
- **Page Limit:** {{ response_instructions.page_limit }}
- **Accepted Formats:** {{ response_instructions.format | join(', ') }}
- **Submission Method:** {{ response_instructions.submission_method }}

## 7. Evaluation & Basis of Award
- **Source Selection Method:** {{ selection_method }}
- **Weights:** Technical {{ (evaluation_weights.technical*100) | round(0) }}% / Price {{ (evaluation_weights.price*100) | round(0) }}%
- **Instrument-Specific Notes:** RFI/Sources Sought (no award), IFB (lowest responsive/responsible), Micro‑Purchase (under threshold), RFTOP/BPA (eligible holders).

## 8. Procurement Method & Thresholds (Policy: {{ policy.name }})
- **Type by Budget:** {{ solicitation_type }}
- **Micro‑Purchase Threshold:** ${{ policy.thresholds.micro_purchase }}
- **Simplified Acquisition Threshold:** ${{ policy.thresholds.simplified_acquisition }}

## 9. Compliance Requirements (Pre‑Award Gates)
- **Section 508 VPAT:** {{ policy.compliance.require_vpat_508 }}
- **Section 889 Representation:** {{ policy.compliance.require_section_889_rep }}
- **SAM Exclusions Check:** {{ policy.compliance.check_sam_exclusions }}
- **BAA/TAA Applicable:** {{ policy.compliance.baa_taa_applicable }}

## 10. Compliance Matrix (Offeror Response)
Complete S/C/T/N with remarks for:
- Technical/Functional
- Security/Hosting
- Performance & Scalability
- Integration & APIs
- Reporting & Analytics
- Other/Support

## 11. Pricing Details & Assumptions
Provide firm‑fixed pricing, fully itemized. State assumptions and dependencies.

## 12. Clauses & Terms (Reference)
{% for cid, title in clauses.items() -%}
- FAR {{ cid }} — {{ title }}
{% endfor -%}

---
### Auto‑extracted Sections (from uploaded template)
{# Ingested sections such as Vendor Instructions, Evaluation Criteria, Compliance Matrix and Pricing Details will be appended here when a PDF/DOCX template is uploaded in Phase 1. #}
