import pytest
from src.models import RawLead, EnrichedLead, ICPProfile, LeadSegment
from src.scorer import ICPScorer
from src.enricher import MockEnricher

def test_enricher():
    enricher = MockEnricher()
    raw = RawLead(email="test@test.com", company="TechCorp")
    enriched = enricher.enrich(raw)
    
    assert enriched.industry is not None
    assert enriched.role == "Head of Growth" # Based on mock logic

def test_scorer_hot_lead():
    icp = ICPProfile(
        target_industries=["SaaS"],
        target_roles=["Head of Growth"],
        required_tech=["Python"]
    )
    scorer = ICPScorer(icp)
    
    lead = EnrichedLead(
        email="hot@test.com",
        industry="SaaS",
        role="Head of Growth",
        tech_stack=["Python"],
        source="manual"
    )
    
    scored = scorer.score(lead)
    assert scored.score >= 80
    assert scored.segment == LeadSegment.HOT

def test_scorer_cold_lead():
    icp = ICPProfile(
        target_industries=["SaaS"],
        target_roles=["Head of Growth"]
    )
    scorer = ICPScorer(icp)
    
    lead = EnrichedLead(
        email="cold@test.com",
        industry="Retail",
        role="Intern",
        source="manual"
    )
    
    scored = scorer.score(lead)
    assert scored.score < 50
    assert scored.segment == LeadSegment.COLD
