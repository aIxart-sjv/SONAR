from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from collections import Counter, defaultdict

app = FastAPI()

# 🔥 CORS (REQUIRED for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ dev only (restrict in prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FILE = "logs/events.json"


# ✅ Health check
@app.get("/")
def root():
    return {"status": "SONAR API running"}


# ✅ Load logs safely (JSON lines)
def load_events():
    if not os.path.exists(LOG_FILE):
        return []

    events = []

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except:
                continue

    return events


# ✅ Raw events (last 100)
@app.get("/events")
def get_events():
    events = load_events()
    return events[-100:]


# ✅ Aggregated stats (for charts)
@app.get("/stats")
def get_stats():
    events = load_events()

    ports = Counter()
    services = Counter()
    layers = Counter()
    attacks = Counter()

    total_packets = 0

    for e in events:
        ports[str(e.get("port", 0))] += 1
        services[e.get("service", "Unknown")] += 1
        layers[e.get("layer", "Unknown")] += 1
        attacks[e.get("attack", "Unknown")] += 1

        total_packets += int(e.get("packets", 0))

    return {
        "total_packets": total_packets,
        "ports": dict(ports),
        "services": dict(services),
        "layers": dict(layers),
        "attacks": dict(attacks),
    }


# ✅ Time-series (for graph)
@app.get("/timeseries")
def get_timeseries():
    events = load_events()

    series = defaultdict(lambda: {
        "timestamp": "",
        "pps": 0,
        "attack": "Benign"
    })

    for e in events:
        ts = e.get("timestamp", "")[:19]  # group per second

        if not ts:
            continue

        series[ts]["timestamp"] = ts
        series[ts]["pps"] += int(e.get("pps", 0))

        # prioritize attacks over benign
        if e.get("attack") != "Benign":
            series[ts]["attack"] = e.get("attack")

    return list(series.values())