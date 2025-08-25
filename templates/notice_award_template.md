# Notice of Award

**Solicitation:** {{ title }}
**Awardee:** {{ awardee.vendor_name }}
**Source Selection Method:** {{ selection_method }}

**Scores**
- Technical: {{ '%.2f' % awardee.scores.technical }}
- Price: {{ '%.2f' % awardee.scores.price }}
- Baseline Total (weights): {{ '%.2f' % awardee.total_score if awardee.get('total_score') else 'N/A' }}
- NLP Semantic Alignment: {{ '%.2f' % semantic_match if semantic_match is defined else 'N/A' }}%
- Model Score (Final): {{ '%.2f' % model_score if model_score is defined else 'N/A' }}

**Pre-Award Compliance Snapshot**
- SAM Exclusions: {{ 'Clear' if awardee.sam_clear else 'Excluded/Unknown' }}
- Section 889 Rep: {{ 'Provided' if awardee.rep_889 else 'Missing' }}
- VPAT (508): {{ 'Provided' if awardee.vpat else 'Missing/Not applicable' }}
- BAA/TAA: {{ 'Compliant' if awardee.baa_taa_ok else 'Unknown/Not applicable' }}

The agency thanks all vendors for their participation.
