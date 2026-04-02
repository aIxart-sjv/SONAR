from fastapi import FastAPI
import json
import os

app = FastAPI()

LOG_FILE = "logs/events.json"


@app.get("/")
def root():
    return {"status": "SONAR API running"}


@app.get("/events")
def get_events():
    if not os.path.exists(LOG_FILE):
        return []

    events = []

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except:
                continue

    return events[-100:]  # last 100 events