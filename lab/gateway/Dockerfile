FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends nftables curl iproute2 && rm -rf /var/lib/apt/lists/*
WORKDIR /lab
COPY lab/gateway/app.py /lab/app.py
RUN pip install --no-cache-dir fastapi uvicorn
CMD ["sh", "-c", "nft list table inet inveriq >/dev/null 2>&1 || (nft add table inet inveriq && nft 'add chain inet inveriq input { type filter hook input priority 0; policy accept; }'); uvicorn app:app --host 0.0.0.0 --port 8080"]
