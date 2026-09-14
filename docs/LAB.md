# INVERIQ v0.3 isolated enforcement lab

The v0.3 lab demonstrates real `nftables` enforcement without modifying the host firewall.
All filtering occurs inside the `inveriq-gateway` Docker container, which is the only service granted `NET_ADMIN`.

## Topology

- `gateway` — `10.77.0.10`, protected authentication API and nftables enforcement point
- `attacker` — `10.77.0.50`, synthetic high-rate login client
- `trusted` — `10.77.0.60`, continuous health-check client

The Docker bridge subnet is `10.77.0.0/24`.

## Start the lab

```bash
docker compose -f docker-compose.lab.yml up --build -d
```

Check service metrics:

```bash
python scripts/lab_status.py
```

Inspect the isolated firewall:

```bash
docker exec inveriq-gateway nft list table inet inveriq
```

## Demonstrate the verification gate

An unsafe broad-block candidate is rejected and cannot execute:

```bash
python scripts/lab_enforce.py --candidate MIT-UNSAFE
```

Apply the verified rate-limit candidate:

```bash
python scripts/lab_enforce.py --candidate MIT-RATE
```

Then inspect metrics and confirm the trusted `/health` flow remains available.

## Reset

```bash
python scripts/lab_reset.py
```

Or destroy the complete isolated lab:

```bash
docker compose -f docker-compose.lab.yml down -v --remove-orphans
```

## Safety boundary

The enforcement helper is deliberately hard-wired to `docker exec inveriq-gateway`. It does not invoke `nft` on the host. The repository does not provide a host-firewall execution path.
