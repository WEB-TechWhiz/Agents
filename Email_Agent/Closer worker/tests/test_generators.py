import pytest
from src.models import Lead, Proposal, ProposalOption
from src.generators import ProposalGenerator

def test_proposal_generator_email():
    # Setup
    lead = Lead(email="test@test.com", name="Test User", company="Test Co")
    proposal = Proposal(
        lead=lead,
        product_name="Test Product",
        price_range="$100",
        roi_estimate="10x",
        timeline="1 week",
        options=[ProposalOption(name="Opt1", description="Desc1")]
    )
    generator = ProposalGenerator("src/templates")
    
    # Execute
    email_body = generator.generate_email_body(proposal, "http://link")
    
    # Verify
    assert "Test User" in email_body
    assert "Test Product" in email_body
    assert "http://link" in email_body
    assert "Opt1" in email_body

def test_proposal_generator_quote():
    lead = Lead(email="test@test.com", name="Test User", company="Test Co")
    proposal = Proposal(
        lead=lead,
        product_name="Test Product",
        price_range="$100",
        roi_estimate="10x",
        timeline="1 week",
        options=[]
    )
    generator = ProposalGenerator("src/templates")
    
    quote_text = generator.generate_quote_text(proposal)
    
    assert "QUOTE FOR SERVICES" in quote_text
    assert "Test Product" in quote_text
    assert "$100" in quote_text
