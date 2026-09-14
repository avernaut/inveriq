from fastapi import FastAPI, Request
from pydantic import BaseModel
from time import time

app = FastAPI(title="INVERIQ Demo Authentication API")
COUNTERS = {"total": 0, "login": 0, "health": 0, "started": time()}

class Login(BaseModel):
    username: str
    password: str

@app.get("/health")
def health(request: Request):
    COUNTERS["total"] += 1
    COUNTERS["health"] += 1
    return {"status": "ok", "client": request.client.host}

@app.post("/login")
def login(payload: Login, request: Request):
    COUNTERS["total"] += 1
    COUNTERS["login"] += 1
    # The lab never contains real credentials. Every request is rejected.
    return {"authenticated": False, "client": request.client.host}

@app.get("/metrics")
def metrics():
    elapsed = max(time() - COUNTERS["started"], 0.001)
    return {**COUNTERS, "elapsed_seconds": elapsed, "requests_per_second": COUNTERS["total"] / elapsed}
