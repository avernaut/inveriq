from inveriq.detection.detector import demo_bruteforce_event
from inveriq.enforcement.nftables import build_plan, render_nftables
from inveriq.intent.policy import load_policy
from inveriq.response.generator import generate_candidates
from inveriq.verification.engine import verify


def _candidate(cid: str):
    threat = demo_bruteforce_event()
    return threat, next(c for c in generate_candidates(threat) if c.id == cid)


def test_lab_source_matches_static_attacker_ip():
    threat = demo_bruteforce_event()
    assert threat.source == "10.77.0.50"


def test_verified_rate_limit_can_execute_only_in_explicit_lab_mode():
    threat, candidate = _candidate("MIT-RATE")
    result = verify(candidate, threat, load_policy())
    assert result.decision == "VERIFIED"
    assert build_plan(candidate, verified=True, lab_mode=False).executable is False
    plan = build_plan(candidate, verified=True, lab_mode=True)
    assert plan.executable is True
    assert "10.77.0.50" in plan.command
    assert "limit rate over 10/second drop" in plan.command
    assert "INVERIQ:MIT-RATE" in plan.command


def test_rejected_candidate_never_executes_even_in_lab_mode():
    threat, candidate = _candidate("MIT-UNSAFE")
    result = verify(candidate, threat, load_policy())
    assert result.decision == "REJECTED"
    plan = build_plan(candidate, verified=False, lab_mode=True)
    assert plan.executable is False
    assert plan.command == "# rejected by INVERIQ"


def test_block_rule_is_scoped_to_inveriq_table():
    _, candidate = _candidate("MIT-BLOCK")
    cmd = render_nftables(candidate)
    assert cmd.startswith("nft add rule inet inveriq input")
    assert cmd.endswith('comment "INVERIQ:MIT-BLOCK"')
