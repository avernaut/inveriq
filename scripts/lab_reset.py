#!/usr/bin/env python3
import subprocess

subprocess.run(
    ["docker", "exec", "inveriq-gateway", "sh", "-lc", "nft flush chain inet inveriq input"],
    check=True,
)
print("INVERIQ lab enforcement rules cleared.")
