from inveriq.models.mitigation import MitigationCandidate


def render_nftables(candidate: MitigationCandidate) -> str:
    """Render only. Execution is intentionally disabled in the starter MVP."""
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
