from ipaddress import ip_address, ip_network

from inveriq.models.mitigation import MitigationCandidate
from inveriq.models.threat import ThreatEvent
from inveriq.models.verification import VerificationResult


def _pass(value: bool) -> str:
    return "PASS" if value else "FAIL"


def verify(candidate: MitigationCandidate, threat: ThreatEvent, policy: dict) -> VerificationResult:
    intent = policy["intent"]
    constraints = intent["constraints"]

    authorization_ok = (
        candidate.action in intent["permitted_actions"]
        and candidate.action not in intent.get("forbidden_actions", [])
        and (candidate.duration or 0) <= constraints.get("max_block_duration", 10**9)
    )

    try:
        source_match = ip_address(threat.source) in ip_network(candidate.source, strict=False)
    except ValueError:
        source_match = candidate.source == threat.source
    target_ok = candidate.target == threat.target and source_match

    reachability_ok = candidate.preserves_reachability
    availability_ok = candidate.preserves_availability
    blast_ok = candidate.estimated_blast_radius <= constraints["max_blast_radius"]
    effectiveness_ok = candidate.effective

    checks = [
        authorization_ok,
        target_ok,
        reachability_ok,
        availability_ok,
        blast_ok,
        effectiveness_ok,
    ]

    return VerificationResult(
        candidate=candidate.id,
        authorization=_pass(authorization_ok),
        target=_pass(target_ok),
        reachability=_pass(reachability_ok),
        availability=_pass(availability_ok),
        blast_radius=_pass(blast_ok),
        effectiveness=_pass(effectiveness_ok),
        decision="VERIFIED" if all(checks) else "REJECTED",
    )
