from typing import Literal
from pydantic import BaseModel

Status = Literal["PASS", "FAIL"]


class VerificationResult(BaseModel):
    candidate: str
    authorization: Status
    target: Status
    reachability: Status
    availability: Status
    blast_radius: Status
    effectiveness: Status
    decision: Literal["VERIFIED", "REJECTED"]


class PostVerificationResult(BaseModel):
    candidate: str
    attack_rate_before: float
    attack_rate_after: float
    legitimate_rate_before: float
    legitimate_rate_after: float
    critical_service_up: bool
    threat_reduction: float
    availability: float
    result: Literal["PASS", "FAIL"]
