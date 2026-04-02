from collections import defaultdict
import time


class PortScanDetector:
    def __init__(self, threshold=20, window=5):
        self.history = defaultdict(list)
        self.threshold = threshold
        self.window = window

    def update(self, src_ip, dst_port):
        now = time.time()

        self.history[src_ip].append((dst_port, now))

        # Keep only recent entries
        self.history[src_ip] = [
            (port, t) for port, t in self.history[src_ip]
            if now - t < self.window
        ]

        # Count unique ports
        ports = set(p for p, _ in self.history[src_ip])

        if len(ports) > self.threshold:
            return True

        return False