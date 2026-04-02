import json
import os
from datetime import datetime

LOG_FILE = "logs/events.json"


def log_event(event):
    event["timestamp"] = datetime.utcnow().isoformat()

    # 🔥 Ensure directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")