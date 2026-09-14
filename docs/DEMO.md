# INVERIQ Expo Demo — v0.2.0

## Goal
Demonstrate why autonomous cyber response needs a deterministic verification gate.

## Flow
1. A synthetic credential brute-force event is detected and mapped to MITRE ATT&CK T1110.
2. INVERIQ generates three deterministic response candidates.
3. V1-V6 verification rejects the broad unsafe block and verifies safer alternatives.
4. The candidate with the smallest estimated blast radius is selected.
5. The nftables adapter renders an enforcement preview; v0.2 does not execute it.
6. Offline-safe post-verification counters demonstrate threat reduction and preserved service availability.

## Safety
The v0.2 public demo does not launch hostile traffic and does not alter host firewall state. This makes the demo repeatable, offline-capable, and suitable for development laptops. Real isolated enforcement belongs to a later testbed-only milestone.
