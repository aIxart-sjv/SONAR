from scapy.all import sniff, IP, TCP, UDP

from src.engine.flow_builder import FlowBuilder
from src.engine.realtime_detector import RealTimeDetector
from src.engine.scan_detector import PortScanDetector
from src.engine.syn_detector import SynScanDetector
from src.engine.rst_detector import RSTDetector

from src.utils.event_logger import log_event
from src.localization.attack_mapper import map_realtime_context
from src.utils.traffic_monitor import TrafficMonitor


# 🔥 Initialize components
flow_builder = FlowBuilder(timeout=1)
detector = RealTimeDetector()
scan_detector = PortScanDetector()
syn_detector = SynScanDetector()
rst_detector = RSTDetector()
traffic_monitor = TrafficMonitor(window=1)  # packets per second


def process_packet(packet):
    """
    packet → behavior → flow → ML → context → alert → log
    """
    pps = traffic_monitor.update()
    # 🚫 Ignore non-IP packets
    if IP not in packet:
        return

    src_ip = packet[IP].src
    dst_port = None

    # 🔥 Extract destination port
    if packet.haslayer(TCP):
        dst_port = packet[TCP].dport
    elif packet.haslayer(UDP):
        dst_port = packet[UDP].dport

    # 🔥 Port scan detection (cross-flow)
    if dst_port and scan_detector.update(src_ip, dst_port):
        print(f"[⚠️ PORT SCAN DETECTED] Source: {src_ip}")

    # 🔥 Flow processing
    features = flow_builder.process_packet(packet)

    if not features:
        return

    try:
        # 🔥 ML prediction
        result = detector.predict(features)

        # 🔥 Context mapping
        context = map_realtime_context(features, result["prediction"])

        # 🔥 Determine state
        is_attack = context["attack"] != "Benign"
        is_anomaly = result.get("anomaly", False)

        # 🔥 Always log (even benign — for history/API)
        log_event({
            "attack": str(context["attack"]),
            "service": str(context["service"]),
            "layer": str(context["layer"]),
            "port": int(features["Destination Port"]),
            "packets": int(features["Total Fwd Packets"]),
            "pps": int(pps),
            "anomaly": bool(is_anomaly),
            "src_ip": str(src_ip)
        })

        # 🔥 ONLY alert when meaningful
        if is_attack or is_anomaly:
            print(
                f"[ALERT] {context['attack']} | "
                f"{context['layer']} | {context['service']} | "
                f"Port: {features['Destination Port']} | "
                f"Packets: {features['Total Fwd Packets']}"
            )

        # 🔥 Anomaly alert (separate signal)
        if is_anomaly:
            print("[🚨 ANOMALY DETECTED]")

        # 🔥 RST-based detection (failed connections)
        if rst_detector.update(src_ip, features.get("RST Flag Count", 0)):
            print(f"[🚨 HIGH FAILED CONNECTION RATE] Source: {src_ip}")

        # 🔥 SYN-based detection (scan / flood)
        if syn_detector.update(src_ip, features.get("SYN Flag Count", 0)):
            print(f"[🚨 SYN SCAN / FLOOD DETECTED] Source: {src_ip}")

        # 🔥 Fast heuristic (flow-level)
        if (
            features.get("SYN Flag Count", 0) > 3
            and features.get("ACK Flag Count", 0) == 0
        ):
            print("[⚠️ SUSPICIOUS SYN PATTERN]")

    except Exception as e:
        print(f"[ERROR] {e}")


def start_capture(interface=None):
    print("[🚀] Starting live packet capture...\n")

    sniff(
        iface=interface,
        prn=process_packet,
        store=False
    )