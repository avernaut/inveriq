# Expo release-candidate policy

INVERIQ v0.9.0 is the feature-frozen Expo release candidate.

## Rules

- No external LLM/API dependency is required for the live demo.
- All attack scenarios are generated locally.
- All enforcement is confined to the Docker lab.
- No new feature should be merged into the Expo branch after freeze.
- Only bug fixes, reliability improvements, documentation fixes, and security fixes are allowed.
- Public benchmark claims must come from repeated measured runs, not single-run values.

## Recommended tag

`v0.9.0-expo-rc2`
