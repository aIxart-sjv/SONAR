from collections import defaultdict
import time


class SynScanDetector:
    def __init__(self, threshold=20, window=5):
        self.history = defaultdict(list)
        self.threshold = threshold
        self.window = window

    def update(self, src_ip, syn_count):
        now = time.time()

        # store SYN events
        self.history[src_ip].append((syn_count, now))

        # keep only recent
        self.history[src_ip] = [
            (count, t) for count, t in self.history[src_ip]
            if now - t < self.window
        ]

        total_syn = sum(count for count, _ in self.history[src_ip])

        if total_syn > self.threshold:
            return True

        return False