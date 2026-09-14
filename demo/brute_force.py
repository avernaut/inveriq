from pprint import pprint

from inveriq.detection.detector import demo_bruteforce_event
from inveriq.intent.policy import load_policy
from inveriq.response.generator import generate_candidates
from inveriq.verification.engine import verify


if __name__ == "__main__":
    threat = demo_bruteforce_event()
    policy = load_policy()
    for candidate in generate_candidates(threat):
        pprint(candidate.model_dump())
        pprint(verify(candidate, threat, policy).model_dump())
        print()
