from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class LeadStatus(str, Enum):
    NEW = "new"
    NEGOTIATING = "negotiating"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    ESCALATED = "escalated"

class Lead(BaseModel):
    email: str
    name: Optional[str] = "there"
    company: Optional[str] = None
    acv: float = 0.0  # Account Contract Value
    status: LeadStatus = LeadStatus.NEW

class ProposalOption(BaseModel):
    name: str
    description: str
    action_link: Optional[str] = None

class Proposal(BaseModel):
    lead: Lead
    product_name: str
    price_range: str
    roi_estimate: str
    timeline: str
    options: List[ProposalOption]
    generated_at: datetime = Field(default_factory=datetime.now)

class Meeting(BaseModel):
    lead_email: str
    time_slot: str
    link: str
