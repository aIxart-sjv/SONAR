import time
from collections import deque

class TrafficMonitor:
    def __init__(self, window=10):
        self.timestamps = deque()
        self.window = window  # seconds

    def update(self):
        now = time.time()
        self.timestamps.append(now)

        # remove old timestamps
        while self.timestamps and now - self.timestamps[0] > self.window:
            self.timestamps.popleft()

        return len(self.timestamps)  # packets in window