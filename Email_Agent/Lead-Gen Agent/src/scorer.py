from .models import EnrichedLead, ScoredLead, ICPProfile, LeadSegment

class ICPScorer:
    def __init__(self, profile: ICPProfile):
        self.profile = profile

    def score(self, lead: EnrichedLead) -> ScoredLead:
        score = 0
        reasons = []

        # Industry Match
        if lead.industry in self.profile.target_industries:
            score += 30
            reasons.append(f"Industry match: {lead.industry}")

        # Role Match
        if lead.role in self.profile.target_roles:
            score += 30
            reasons.append(f"Role match: {lead.role}")
            
        # Tech Stack Match
        for tech in self.profile.required_tech:
            if tech in lead.tech_stack:
                score += 20
                reasons.append(f"Tech match: {tech}")

        # Segment
        if score >= 80:
            segment = LeadSegment.HOT
        elif score >= 50:
            segment = LeadSegment.WARM
        else:
            segment = LeadSegment.COLD

        return ScoredLead(
            **lead.dict(),
            score=score,
            segment=segment,
            match_reasons=reasons
        )
