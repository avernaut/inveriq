from inveriq.detection.detector import demo_bruteforce_event
from inveriq.intent.policy import load_policy
from inveriq.response.generator import generate_candidates
from inveriq.verification.engine import verify


def test_unsafe_candidate_is_rejected():
    threat = demo_bruteforce_event()
    policy = load_policy()
    candidates = generate_candidates(threat)
    result = verify(candidates[0], threat, policy)
    assert result.decision == "REJECTED"
    assert result.reachability == "FAIL"
    assert result.availability == "FAIL"
    assert result.blast_radius == "FAIL"


def test_rate_limit_candidate_is_verified():
    threat = demo_bruteforce_event()
    policy = load_policy()
    candidates = generate_candidates(threat)
    result = verify(candidates[2], threat, policy)
    assert result.decision == "VERIFIED"
