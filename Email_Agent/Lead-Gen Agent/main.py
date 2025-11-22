from src.agent import LeadGenAgent
from src.models import ICPProfile

def main():
    # 1. Define ICP
    icp = ICPProfile(
        target_industries=["SaaS", "Fintech"],
        target_roles=["Head of Growth", "CTO"],
        required_tech=["Python"]
    )
    
    agent = LeadGenAgent(icp)
    
    print("--- Lead-Gen Agent Started ---")
    
    # 2. Mock Data Input
    manual_leads = [
        {"email": "lead1@techco.com", "company": "TechCo", "first_name": "John"},
        {"email": "lead2@retail.com", "company": "RetailInc", "first_name": "Jane"}
    ]
    
    # 3. Process Batch
    print("\nProcessing Batch...")
    results = agent.process_batch(manual_data=manual_leads)
    
    for lead in results:
        print(f"Lead: {lead.email} | Score: {lead.score} ({lead.segment})")
        print(f"   Reasons: {lead.match_reasons}")
        
    # 4. Hand-off
    print("\nHanding off qualified leads...")
    agent.handoff_to_outreach(results)

if __name__ == "__main__":
    main()
