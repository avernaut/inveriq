from inveriq.models.mitigation import MitigationCandidate
from inveriq.models.threat import ThreatEvent


def generate_candidates(threat: ThreatEvent) -> list[MitigationCandidate]:
    """Deterministic offline-safe candidate generation for the expo MVP."""
    return [
        MitigationCandidate(
            id="MIT-UNSAFE",
            threat_id=threat.id,
            action="BLOCK_SOURCE",
            source="10.0.0.0/16",
            target=threat.target,
            duration=600,
            reason="Broad block intended to stop attack traffic",
            estimated_blast_radius=0.82,
            preserves_reachability=False,
            preserves_availability=False,
            effective=True,
        ),
        MitigationCandidate(
            id="MIT-BLOCK",
            threat_id=threat.id,
            action="BLOCK_SOURCE",
            source=threat.source,
            target=threat.target,
            duration=600,
            reason="Block the confirmed malicious source",
            estimated_blast_radius=0.004,
            preserves_reachability=True,
            preserves_availability=True,
            effective=True,
        ),
        MitigationCandidate(
            id="MIT-RATE",
            threat_id=threat.id,
            action="RATE_LIMIT_SOURCE",
            source=threat.source,
            target=threat.target,
            duration=600,
            reason="Rate-limit the confirmed malicious source",
            estimated_blast_radius=0.002,
            preserves_reachability=True,
            preserves_availability=True,
            effective=True,
        ),
    ]
