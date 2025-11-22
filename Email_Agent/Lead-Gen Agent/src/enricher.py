import random
from .models import RawLead, EnrichedLead

class MockEnricher:
    def enrich(self, lead: RawLead) -> EnrichedLead:
        # Simulate API call latency or logic
        
        # Mock data based on email domain or random
        industry = "SaaS" if "tech" in (lead.company or "").lower() else "Retail"
        tech_stack = ["Python", "AWS"] if random.random() > 0.5 else ["Shopify"]
        
        return EnrichedLead(
            **lead.dict(),
            industry=industry,
            company_size="50-200",
            tech_stack=tech_stack,
            role="Head of Growth", # Mock role
            location="San Francisco, CA"
        )
