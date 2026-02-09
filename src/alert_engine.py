def generate_alerts(predictions):
    alerts = []
    for i, pred in enumerate(predictions):
        if pred == -1:
            alerts.append(f"Anomaly detected at index {i}")
    return alerts