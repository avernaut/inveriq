from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ThreatEvent(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    attack: str
    mitre: str
    source: str
    target: str
    confidence: float = Field(ge=0.0, le=1.0)
    severity: str
