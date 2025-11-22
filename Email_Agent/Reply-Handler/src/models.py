from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class IntentType(str, Enum):
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    ASK_INFO = "ask_info"
    SPAM = "spam"
    UNSUBSCRIBE = "unsubscribe"
    SCHEDULE_REQUEST = "schedule_request"
    UNKNOWN = "unknown"

class LeadState(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    UNSUBSCRIBED = "unsubscribed"
    SCHEDULED = "scheduled"

class Lead(BaseModel):
    email: str
    name: Optional[str] = None
    state: LeadState = LeadState.NEW
    history: List[str] = Field(default_factory=list)

class EmailLog(BaseModel):
    lead_email: str
    direction: str # "inbound" or "outbound"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    intent: Optional[IntentType] = None

class ExtractionResult(BaseModel):
    intent: IntentType
    confidence: float
    requested_product: Optional[str] = None
    budget_hint: Optional[str] = None
    meeting_time: Optional[str] = None
    language: str = "en"
