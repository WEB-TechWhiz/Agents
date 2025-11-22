from datetime import datetime
from typing import Optional
from .models import SuppressionRecord, ConsentRecord, SuppressionReason, ConsentType, AuditLog
from .storage import JsonStorage

class ComplianceManager:
    def __init__(self, storage: JsonStorage = None):
        self.storage = storage or JsonStorage()
        self.suppression_list = self.storage.load_suppression_list()
        self.consent_log = self.storage.load_consent_log()

    def check_eligibility(self, email: str) -> bool:
        """
        Checks if an email is eligible to receive messages.
        Returns False if suppressed.
        """
        for record in self.suppression_list:
            if record['email'] == email:
                return False
        return True

    def add_to_suppression_list(self, email: str, reason: SuppressionReason):
        """
        Adds an email to the suppression list.
        """
        if not self.check_eligibility(email):
            print(f"Email {email} is already suppressed.")
            return

        record = SuppressionRecord(email=email, reason=reason)
        self.suppression_list.append(record.dict())
        self.storage.save_suppression_list(self.suppression_list)
        self._audit_log("suppress", "system", email, f"Reason: {reason}")
        print(f"Suppressed {email} due to {reason}")

    def log_consent(self, email: str, source: str, consent_type: ConsentType = ConsentType.MARKETING):
        """
        Logs consent for a lead.
        """
        record = ConsentRecord(email=email, source=source, consent_type=consent_type)
        self.consent_log.append(record.dict())
        self.storage.save_consent_log(self.consent_log)
        self._audit_log("consent_grant", "system", email, f"Source: {source}")
        print(f"Logged consent for {email}")

    def process_dsar_delete(self, email: str):
        """
        Handles a DSAR deletion request.
        Redacts PII from consent logs and adds to suppression list (hashed or marked).
        """
        print(f"Processing DSAR deletion for {email}...")
        
        # 1. Redact from Consent Log
        redacted_count = 0
        for record in self.consent_log:
            if record['email'] == email:
                record['email'] = "REDACTED"
                record['ip_address'] = "REDACTED"
                redacted_count += 1
        
        if redacted_count > 0:
            self.storage.save_consent_log(self.consent_log)
            print(f"Redacted {redacted_count} records from consent log.")

        # 2. Ensure Suppression (to prevent re-add)
        # Note: In a real system, we might hash this. For now, we keep the email in suppression 
        # but mark it as DSAR_DELETION so we know why it's there (and maybe don't store other info).
        self.add_to_suppression_list(email, SuppressionReason.DSAR_DELETION)
        
        self._audit_log("dsar_delete", "admin", email, "PII Redacted")

    def _audit_log(self, action: str, actor: str, target: str, details: str):
        # Simple print for now, could write to a separate file
        log = AuditLog(action=action, actor=actor, target_email=target, details=details)
        print(f"[AUDIT] {log.timestamp} - {action}: {target} ({details})")
