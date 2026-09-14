from dataclasses import dataclass
from inveriq.models.mitigation import MitigationCandidate


@dataclass(frozen=True)
class EnforcementPlan:
    candidate_id: str
    command: str
    executable: bool = False


def render_nftables(candidate: MitigationCandidate) -> str:
    """Render a Linux nftables command without executing it."""
    if candidate.action == "BLOCK_SOURCE":
        return f"nft add rule inet filter input ip saddr {candidate.source} drop"
    if candidate.action == "RATE_LIMIT_SOURCE":
        return (
            "nft add rule inet filter input "
            f"ip saddr {candidate.source} limit rate 10/second accept"
        )
    if candidate.action == "ISOLATE_DEVICE":
        return f"# isolate {candidate.target} using a deployment-specific adapter"
    return "# no enforcement adapter available"


def build_plan(candidate: MitigationCandidate, verified: bool) -> EnforcementPlan:
    """Build an enforcement plan only for a verified candidate.

    v0.2 deliberately remains preview-only: the command is never executed by
    the application. Real enforcement will require an isolated demo namespace
    and an explicit adapter in a later version.
    """
    command = render_nftables(candidate) if verified else "# rejected by INVERIQ"
    return EnforcementPlan(candidate.id, command, executable=False)
