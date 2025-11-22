from src.agent import CloserAgent
from src.models import Lead

def main():
    agent = CloserAgent()
    
    print("--- Closer Agent Started ---")
    
    # Case 1: Standard Lead
    lead1 = Lead(email="client@company.com", name="Alice", company="TechCorp", acv=5000)
    print(f"\nProcessing Lead 1: {lead1.email}")
    result1 = agent.process_lead(lead1)
    print(f"Status: {result1['status']}")
    if 'email_body' in result1:
        print(f"Email Body Preview:\n{result1['email_body'][:200]}...")
    if 'pdf_path' in result1:
        print(f"PDF Generated: {result1['pdf_path']}")

    # Case 2: High Value Lead (Escalation)
    lead2 = Lead(email="vip@enterprise.com", name="Bob", company="BigBiz", acv=50000)
    print(f"\nProcessing Lead 2: {lead2.email}")
    result2 = agent.process_lead(lead2)
    print(f"Status: {result2['status']}")
    if 'reason' in result2:
        print(f"Reason: {result2['reason']}")

if __name__ == "__main__":
    main()
