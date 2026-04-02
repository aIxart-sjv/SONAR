from collections import defaultdict
import time


class RSTDetector:
    def __init__(self, threshold=10, window=5):
        self.history = defaultdict(list)
        self.threshold = threshold
        self.window = window

    def update(self, src_ip, rst_count):
        now = time.time()

        if rst_count == 0:
            return False

        self.history[src_ip].append((rst_count, now))

        # keep recent entries
        self.history[src_ip] = [
            (count, t) for count, t in self.history[src_ip]
            if now - t < self.window
        ]

        total_rst = sum(count for count, _ in self.history[src_ip])

        if total_rst >= self.threshold:
            return True

        return False