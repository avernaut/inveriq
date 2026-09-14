from inveriq.detection.detector import demo_bruteforce_event
from inveriq.enforcement.nftables import build_plan
from inveriq.intent.policy import load_policy
from inveriq.postverify.engine import simulate_post_verification
from inveriq.response.generator import generate_candidates
from inveriq.verification.engine import verify


def test_every_candidate_requires_verification_before_enforcement():
    threat = demo_bruteforce_event()
    policy = load_policy()
    candidates = generate_candidates(threat)
    results = [verify(candidate, threat, policy) for candidate in candidates]

    for candidate, result in zip(candidates, results):
        plan = build_plan(candidate, verified=result.decision == "VERIFIED")
        assert plan.executable is False
        if result.decision == "REJECTED":
            assert plan.command == "# rejected by INVERIQ"


def test_rate_limit_post_verification_passes():
    threat = demo_bruteforce_event()
    candidate = generate_candidates(threat)[2]
    post = simulate_post_verification(candidate)
    assert post.result == "PASS"
    assert post.threat_reduction >= 0.95
    assert post.availability >= 0.95
    assert post.critical_service_up is True
