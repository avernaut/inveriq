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
