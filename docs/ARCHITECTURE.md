# INVERIQ MVP Architecture

## Objective

INVERIQ inserts a deterministic verification layer between AI-generated cybersecurity decisions and infrastructure enforcement.

```text
Telemetry
   |
   v
Threat Detection
   |
   v
MITRE ATT&CK Mapping
   |
   v
Response Generator
   |
   v
Mitigation Candidates
   |
   v
+-----------------------------+
| INVERIQ Verification Engine |
| V1 Authorization            |
| V2 Target                   |
| V3 Reachability             |
| V4 Availability             |
| V5 Blast Radius             |
| V6 Security Effectiveness   |
+--------------+--------------+
               |
        VERIFIED ONLY
               |
               v
        Enforcement Adapter
               |
               v
          Post-Verify
```

## Trust boundary

AI components operate outside the trusted enforcement boundary. Only structured actions that pass all deterministic verification gates may cross the boundary.
