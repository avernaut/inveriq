# IoT Tech Expo demo flow — v0.3

1. Start the isolated Docker lab.
2. Show that the trusted client continuously reaches the protected service.
3. Show synthetic high-rate authentication traffic from `10.77.0.50`.
4. Create `ThreatEvent` for credential brute force / MITRE ATT&CK T1110.
5. Generate three mitigation candidates.
6. Run V1–V6 on each candidate.
7. Show `MIT-UNSAFE` rejected because reachability, availability and blast-radius gates fail.
8. Select `MIT-RATE` as the lowest-blast-radius verified candidate.
9. Apply its nftables rule inside `inveriq-gateway` only.
10. Verify threat reduction while the trusted health flow remains available.
11. Reset the lab before the next demonstration.

Target speaking time: 90 seconds. Target full interactive demonstration: under 3 minutes.
