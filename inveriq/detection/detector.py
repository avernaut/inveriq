from inveriq.models.threat import ThreatEvent


def demo_bruteforce_event() -> ThreatEvent:
    return ThreatEvent(
        id="THR-001",
        attack="credential_brute_force",
        mitre="T1110",
        source="10.77.0.50",
        target="authentication-api",
        confidence=0.97,
        severity="HIGH",
    )
