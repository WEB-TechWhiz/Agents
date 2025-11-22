from src.manager import ComplianceManager
from src.models import SuppressionReason, ConsentType

def main():
    manager = ComplianceManager()
    
    print("--- Compliance Agent Started ---")
    
    email1 = "user1@example.com"
    email2 = "user2@example.com"
    
    # 1. Log Consent
    print(f"\n--- Step 1: Logging Consent for {email1} ---")
    manager.log_consent(email1, "Signup Form", ConsentType.MARKETING)
    
    # 2. Check Eligibility
    is_eligible = manager.check_eligibility(email1)
    print(f"Is {email1} eligible? {is_eligible}")
    
    # 3. Unsubscribe
    print(f"\n--- Step 2: Unsubscribing {email1} ---")
    manager.add_to_suppression_list(email1, SuppressionReason.UNSUBSCRIBED)
    
    is_eligible = manager.check_eligibility(email1)
    print(f"Is {email1} eligible? {is_eligible}")
    
    # 4. DSAR Request
    print(f"\n--- Step 3: DSAR Request for {email1} ---")
    manager.process_dsar_delete(email1)
    
    # Verify Redaction (Manual check of logs would show REDACTED)
    print("DSAR processing complete.")

if __name__ == "__main__":
    main()
