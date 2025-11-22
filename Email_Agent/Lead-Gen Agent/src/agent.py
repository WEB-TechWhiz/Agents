from typing import List
from .models import ICPProfile, ScoredLead
from .ingestor import Ingestor
from .enricher import MockEnricher
from .scorer import ICPScorer
import json
import os

class LeadGenAgent:
    def __init__(self, icp_profile: ICPProfile):
        self.ingestor = Ingestor()
        self.enricher = MockEnricher()
        self.scorer = ICPScorer(icp_profile)

    def process_batch(self, csv_path: str = None, manual_data: List[dict] = None) -> List[ScoredLead]:
        raw_leads = []
        if csv_path:
            raw_leads.extend(self.ingestor.ingest_csv(csv_path))
        if manual_data:
            raw_leads.extend(self.ingestor.ingest_manual(manual_data))
            
        processed_leads = []
        for raw in raw_leads:
            enriched = self.enricher.enrich(raw)
            scored = self.scorer.score(enriched)
            processed_leads.append(scored)
            
        return processed_leads

    def handoff_to_outreach(self, leads: List[ScoredLead], output_file: str = "data/ready_leads.json"):
        # Filter only qualified leads (Warm/Hot)
        qualified = [l for l in leads if l.score >= 50]
        
        data = [l.dict() for l in qualified]
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Handed off {len(qualified)} qualified leads to {output_file}")
