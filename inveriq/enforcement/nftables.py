from dataclasses import dataclass
from inveriq.models.mitigation import MitigationCandidate

TABLE = "inveriq"
CHAIN = "input"


@dataclass(frozen=True)
class EnforcementPlan:
    candidate_id: str
    command: str
    executable: bool = False


def render_nftables(candidate: MitigationCandidate) -> str:
    """Render a command for the isolated INVERIQ lab nftables table."""
    prefix = f"nft add rule inet {TABLE} {CHAIN} ip saddr {candidate.source}"
    if candidate.action == "BLOCK_SOURCE":
        return f"{prefix} drop comment \"INVERIQ:{candidate.id}\""
    if candidate.action == "RATE_LIMIT_SOURCE":
        # Keep legitimate sources untouched; packets above the per-source rate are dropped.
        return (
            f"{prefix} limit rate over 10/second drop "
            f"comment \"INVERIQ:{candidate.id}\""
        )
    if candidate.action == "ISOLATE_DEVICE":
        return f"# isolate {candidate.target} using a deployment-specific adapter"
    return "# no enforcement adapter available"


def build_plan(candidate: MitigationCandidate, verified: bool, lab_mode: bool = False) -> EnforcementPlan:
    command = render_nftables(candidate) if verified else "# rejected by INVERIQ"
    supported = candidate.action in {"BLOCK_SOURCE", "RATE_LIMIT_SOURCE"}
    return EnforcementPlan(candidate.id, command, executable=bool(verified and lab_mode and supported))
