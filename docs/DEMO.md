# IoT Tech Expo Demo

## Primary scenario

Credential brute-force attack against an IoT authentication service.

## Story

1. Legitimate traffic is continuously generated.
2. An attacker starts a brute-force sequence.
3. INVERIQ identifies the event as credential brute force and maps it to MITRE ATT&CK T1110.
4. The response engine proposes multiple candidate mitigations.
5. A broad subnet block stops the attack but fails reachability, availability, and blast-radius checks, so INVERIQ rejects it.
6. A source-specific block or rate limit passes all checks.
7. INVERIQ enforces the verified action with `nftables`.
8. Post-verification confirms threat reduction while legitimate service remains operational.

## Closing line

**Both actions can stop the attack. Only one is safe. INVERIQ knows the difference.**
