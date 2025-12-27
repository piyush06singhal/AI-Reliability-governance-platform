"""Core data models for the LLM Governance Platform."""
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from uuid import uuid4


class LLMRequest(BaseModel):
    """Represents an incoming LLM request."""
    trace_id: str = Field(default_factory=lambda: str(uuid4()))
    prompt: str
    model: str
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class LLMResponse(BaseModel):
    """Represents an LLM response."""
    trace_id: str
    response: str
    model: str
    latency_ms: float
    tokens_used: int
    cost_usd: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RiskAssessment(BaseModel):
    """Risk assessment for an LLM response."""
    trace_id: str
    risk_score: float = Field(ge=0.0, le=1.0)
    risk_category: str
    evidence: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PolicyDecision(BaseModel):
    """Policy enforcement decision."""
    trace_id: str
    action: str  # "allow", "block", "rewrite", "fallback"
    policy_id: str
    reason: str
    modified_response: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AuditLog(BaseModel):
    """Immutable audit log entry."""
    trace_id: str
    event_type: str
    user_id: Optional[str]
    prompt: str
    response: str
    risk_assessment: Optional[RiskAssessment]
    policy_decision: Optional[PolicyDecision]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
