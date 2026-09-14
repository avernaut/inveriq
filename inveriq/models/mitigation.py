from pydantic import BaseModel


class MitigationCandidate(BaseModel):
    id: str
    threat_id: str
    action: str
    source: str
    target: str
    duration: int | None = None
    reason: str
    estimated_blast_radius: float = 0.0
    preserves_reachability: bool = True
    preserves_availability: bool = True
    effective: bool = True
