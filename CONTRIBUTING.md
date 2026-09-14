# Contributing to INVERIQ

INVERIQ is currently a private Avernaut project. Contributions are accepted only from explicitly authorized collaborators.

## Development principles

1. Safety-critical enforcement paths must remain deterministic and testable.
2. AI/LLM output must never be executed directly against infrastructure.
3. Every mitigation must be represented as a structured action.
4. Verification gates must fail closed.
5. Tests must cover both safe and intentionally unsafe mitigation candidates.
6. Demo functionality must remain reproducible offline.

## Changes

Use focused branches and small commits. Each pull request should describe:

- problem addressed;
- implementation approach;
- security implications;
- tests added or updated;
- impact on the demo path.
