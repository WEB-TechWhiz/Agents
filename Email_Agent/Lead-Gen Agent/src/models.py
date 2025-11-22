from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum

class LeadSegment(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"
    UNQUALIFIED = "unqualified"

class RawLead(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    source: str = "manual"

class EnrichedLead(RawLead):
    industry: Optional[str] = None
    company_size: Optional[str] = None
    tech_stack: List[str] = Field(default_factory=list)
    role: Optional[str] = None
    location: Optional[str] = None

class ScoredLead(EnrichedLead):
    score: int = 0
    segment: LeadSegment = LeadSegment.UNQUALIFIED
    match_reasons: List[str] = Field(default_factory=list)

class ICPProfile(BaseModel):
    target_industries: List[str]
    target_roles: List[str]
    min_company_size: Optional[int] = None
    required_tech: List[str] = Field(default_factory=list)
