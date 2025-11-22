from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class ConsentType(str, Enum):
    MARKETING = "marketing"
    TRANSACTIONAL = "transactional"

class SuppressionReason(str, Enum):
    UNSUBSCRIBED = "unsubscribed"
    SPAM_COMPLAINT = "spam_complaint"
    BOUNCED = "bounced"
    DSAR_DELETION = "dsar_deletion"
    MANUAL_BLOCK = "manual_block"

class ConsentRecord(BaseModel):
    email: str
    source: str
    consent_type: ConsentType
    timestamp: datetime = Field(default_factory=datetime.now)
    ip_address: Optional[str] = None

class SuppressionRecord(BaseModel):
    email: str
    reason: SuppressionReason
    timestamp: datetime = Field(default_factory=datetime.now)

class AuditLog(BaseModel):
    action: str
    actor: str
    target_email: str
    details: str
    timestamp: datetime = Field(default_factory=datetime.now)
