from collections import defaultdict
import time
import numpy as np


# 🔥 Proper port → service mapping
COMMON_PORTS = {
    80: "HTTP",
    443: "HTTPS",
    53: "DNS",
    22: "SSH",
    21: "FTP",
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
    8080: "HTTP",
    8443: "HTTPS",
    3306: "MySQL",
}


def map_service(port):
    if port in COMMON_PORTS:
        return COMMON_PORTS[port]

    # 🔥 Ephemeral ports (client-side)
    if port >= 49152:
        return "Ephemeral"

    return "Other"


def map_layer(service, proto):
    # 🔥 Layer classification (this makes your UI look pro)
    if service in ["HTTP", "HTTPS", "DNS", "SMTP", "FTP"]:
        return "Application"

    if proto in ["TCP", "UDP"]:
        return "Transport"

    return "Network"


class Flow:
    def __init__(self):
        self.start_time = time.time()

        # Directional tracking
        self.fwd_packet_times = []
        self.bwd_packet_times = []

        self.fwd_packet_lengths = []
        self.bwd_packet_lengths = []

        self.fwd_packets = 0
        self.bwd_packets = 0

        # TCP flags
        self.syn_count = 0
        self.ack_count = 0
        self.rst_count = 0
        self.fin_count = 0

    def update(self, packet_len, direction="fwd", flags=None):
        now = time.time()

        if direction == "fwd":
            self.fwd_packet_times.append(now)
            self.fwd_packet_lengths.append(packet_len)
            self.fwd_packets += 1
        else:
            self.bwd_packet_times.append(now)
            self.bwd_packet_lengths.append(packet_len)
            self.bwd_packets += 1

        # TCP flags tracking
        if flags is not None:
            if flags & 0x02:
                self.syn_count += 1
            if flags & 0x10:
                self.ack_count += 1
            if flags & 0x04:
                self.rst_count += 1
            if flags & 0x01:
                self.fin_count += 1

    def compute_iat(self, times):
        if len(times) < 2:
            return [0]
        return np.diff(times)

    def total_packets(self):
        return self.fwd_packets + self.bwd_packets

    def to_feature_dict(self, key):
        src_ip, dst_ip, src_port, dst_port, proto = key

        fwd_lengths = np.array(self.fwd_packet_lengths)
        bwd_lengths = np.array(self.bwd_packet_lengths)

        all_times = self.fwd_packet_times + self.bwd_packet_times
        iat = self.compute_iat(sorted(all_times))

        duration = max((time.time() - self.start_time), 1e-6)

        # 🔥 NEW: service + layer mapping
        service = map_service(dst_port)
        layer = map_layer(service, proto)

        return {
            "Destination Port": dst_port,
            "Service": service,
            "Layer": layer,
            "Protocol": proto,

            "Flow Duration": int(duration * 1e6),

            "Total Fwd Packets": self.fwd_packets,
            "Total Backward Packets": self.bwd_packets,

            "Total Length of Fwd Packets": fwd_lengths.sum() if len(fwd_lengths) else 0,
            "Total Length of Bwd Packets": bwd_lengths.sum() if len(bwd_lengths) else 0,

            # Forward stats
            "Fwd Packet Length Max": fwd_lengths.max() if len(fwd_lengths) else 0,
            "Fwd Packet Length Min": fwd_lengths.min() if len(fwd_lengths) else 0,
            "Fwd Packet Length Mean": fwd_lengths.mean() if len(fwd_lengths) else 0,
            "Fwd Packet Length Std": fwd_lengths.std() if len(fwd_lengths) else 0,

            # Backward stats
            "Bwd Packet Length Max": bwd_lengths.max() if len(bwd_lengths) else 0,
            "Bwd Packet Length Min": bwd_lengths.min() if len(bwd_lengths) else 0,
            "Bwd Packet Length Mean": bwd_lengths.mean() if len(bwd_lengths) else 0,
            "Bwd Packet Length Std": bwd_lengths.std() if len(bwd_lengths) else 0,

            "Flow Bytes/s": (fwd_lengths.sum() + bwd_lengths.sum()) / duration,
            "Flow Packets/s": self.total_packets() / duration,

            "Flow IAT Mean": np.mean(iat) if len(iat) else 0,
            "Flow IAT Std": np.std(iat) if len(iat) else 0,
            "Flow IAT Max": np.max(iat) if len(iat) else 0,
            "Flow IAT Min": np.min(iat) if len(iat) else 0,

            # TCP flags
            "SYN Flag Count": self.syn_count,
            "ACK Flag Count": self.ack_count,
            "RST Flag Count": self.rst_count,
            "FIN Flag Count": self.fin_count,
        }


class FlowBuilder:
    def __init__(self, timeout=1):
        self.flows = defaultdict(Flow)
        self.timeout = timeout

    def get_flow_key(self, packet):
        from scapy.all import IP, TCP, UDP

        if IP not in packet:
            return None

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        proto = "OTHER"
        src_port = 0
        dst_port = 0

        if TCP in packet:
            proto = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport

        elif UDP in packet:
            proto = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport

        # 🔥 Bidirectional normalization
        if (src_ip, src_port) < (dst_ip, dst_port):
            return (src_ip, dst_ip, src_port, dst_port, proto)
        else:
            return (dst_ip, src_ip, dst_port, src_port, proto)

    def process_packet(self, packet):
        from scapy.all import IP, TCP

        key = self.get_flow_key(packet)
        if key is None:
            return None

        src_ip = packet[IP].src
        flow = self.flows[key]

        direction = "fwd" if src_ip == key[0] else "bwd"

        flags = None
        if packet.haslayer(TCP):
            flags = packet[TCP].flags

        flow.update(len(packet), direction, flags)

        # 🔥 Emit flow
        if (
            time.time() - flow.start_time > self.timeout
            or flow.total_packets() > 20
        ):
            features = flow.to_feature_dict(key)
            del self.flows[key]
            return features

        return None