from ipaddress import ip_network
from typing import Literal

from pydantic import BaseModel, Field, field_validator


Action = Literal["BLOCK_SOURCE", "RATE_LIMIT_SOURCE", "ISOLATE_DEVICE", "SHUTDOWN_SERVICE"]


class MitigationCandidate(BaseModel):
    id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
    threat_id: str
    action: Action
    source: str
    target: str
    duration: int | None = Field(default=None, ge=0)
    reason: str
    estimated_blast_radius: float = Field(default=0.0, ge=0.0, le=1.0)
    preserves_reachability: bool = True
    preserves_availability: bool = True
    effective: bool = True

    @field_validator("source")
    @classmethod
    def validate_source(cls, value: str) -> str:
        """Accept only a valid IPv4/IPv6 host or network expression.

        Enforcement ultimately interpolates this field into an nftables rule, so
        rejecting non-address input at the model boundary prevents accidental
        command-language injection as new candidate sources are added later.
        """
        try:
            ip_network(value, strict=False)
        except ValueError as exc:
            raise ValueError("source must be a valid IP address or CIDR network") from exc
        return value
