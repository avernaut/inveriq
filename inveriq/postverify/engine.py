from inveriq.models.mitigation import MitigationCandidate
from inveriq.models.verification import PostVerificationResult


def simulate_post_verification(candidate: MitigationCandidate) -> PostVerificationResult:
    """Offline-safe deterministic measurement model for the expo MVP.

    The v0.2 demo does not generate hostile traffic. It uses measured-style
    synthetic counters so the verification pipeline can be exercised safely
    and repeatably without Internet access.
    """
    before_attack = 487.0
    before_legitimate = 121.0

    if candidate.action == "RATE_LIMIT_SOURCE":
        after_attack = 8.0
        after_legitimate = 120.0
        service_up = True
    elif candidate.action == "BLOCK_SOURCE" and candidate.estimated_blast_radius <= 0.05:
        after_attack = 0.0
        after_legitimate = 121.0
        service_up = True
    else:
        after_attack = 0.0
        after_legitimate = 22.0
        service_up = False

    threat_reduction = max(0.0, (before_attack - after_attack) / before_attack)
    availability = after_legitimate / before_legitimate
    passed = threat_reduction >= 0.95 and availability >= 0.95 and service_up

    return PostVerificationResult(
        candidate=candidate.id,
        attack_rate_before=before_attack,
        attack_rate_after=after_attack,
        legitimate_rate_before=before_legitimate,
        legitimate_rate_after=after_legitimate,
        critical_service_up=service_up,
        threat_reduction=threat_reduction,
        availability=availability,
        result="PASS" if passed else "FAIL",
    )
