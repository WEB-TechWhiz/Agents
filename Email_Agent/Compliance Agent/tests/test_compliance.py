import pytest
import os
import json
from src.manager import ComplianceManager
from src.models import SuppressionReason, ConsentType
from src.storage import JsonStorage

@pytest.fixture
def test_storage(tmp_path):
    # Use a temporary directory for tests
    data_dir = tmp_path / "data"
    return JsonStorage(data_dir=str(data_dir))

def test_check_eligibility_new_email(test_storage):
    manager = ComplianceManager(storage=test_storage)
    assert manager.check_eligibility("new@example.com") is True

def test_suppression_logic(test_storage):
    manager = ComplianceManager(storage=test_storage)
    email = "suppressed@example.com"
    
    manager.add_to_suppression_list(email, SuppressionReason.SPAM_COMPLAINT)
    
    assert manager.check_eligibility(email) is False
    
    # Verify it's in the file
    suppression_list = test_storage.load_suppression_list()
    assert len(suppression_list) == 1
    assert suppression_list[0]['email'] == email
    assert suppression_list[0]['reason'] == SuppressionReason.SPAM_COMPLAINT

def test_consent_logging(test_storage):
    manager = ComplianceManager(storage=test_storage)
    email = "consent@example.com"
    
    manager.log_consent(email, "Web Form")
    
    consent_log = test_storage.load_consent_log()
    assert len(consent_log) == 1
    assert consent_log[0]['email'] == email
    assert consent_log[0]['source'] == "Web Form"

def test_dsar_redaction(test_storage):
    manager = ComplianceManager(storage=test_storage)
    email = "delete_me@example.com"
    
    # Add some consent records
    manager.log_consent(email, "Source 1")
    manager.log_consent(email, "Source 2")
    
    # Perform DSAR
    manager.process_dsar_delete(email)
    
    # Verify Redaction
    consent_log = test_storage.load_consent_log()
    for record in consent_log:
        assert record['email'] == "REDACTED"
    
    # Verify Suppression
    assert manager.check_eligibility(email) is False
    suppression_list = test_storage.load_suppression_list()
    assert suppression_list[0]['email'] == email
    assert suppression_list[0]['reason'] == SuppressionReason.DSAR_DELETION
