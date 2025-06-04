"""network_analyzer.py
Analizza dispositivi sulla rete locale e categoriza le ricerche web.
"""

from __future__ import annotations

import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

try:
    from scapy.all import ARP, Ether, srp, sniff, DNSQR
except Exception:  # pragma: no cover - scapy may not be installed
    ARP = Ether = srp = sniff = DNSQR = None  # type: ignore

try:
    import bluetooth
except Exception:  # pragma: no cover - bluetooth may not be installed
    bluetooth = None  # type: ignore

try:
    import pywhatkit
except Exception:  # pragma: no cover - pywhatkit may not be installed
    pywhatkit = None  # type: ignore

# Categoria di parole chiave per le ricerche
CATEGORY_PATTERNS = {
    "salute": ["salute", "medic", "ospedale", "dieta", "farmac"],
    "politica": ["politic", "governo", "elezion"],
    "gossip": ["gossip", "vip", "celebrity"],
    "economia": ["econom", "borsa", "finanza"],
    "viaggi": ["viagg", "hotel", "voli"],
    "religione": ["chiesa", "papa", "religion"],
    "social": ["facebook", "instagram", "tiktok", "twitter"],
}

# Eventuale mappatura IP/MAC -> nome utente
KNOWN_DEVICES = {
    "AA:BB:CC:DD:EE:FF": "PAPA",
}


def scan_wifi_network(network_range: str = "192.168.1.0/24") -> list[dict]:
    """Rileva i dispositivi Wi-Fi sulla rete locale."""
    if ARP is None:
        return []
    arp = ARP(pdst=network_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]
    devices = []
    for sent, received in result:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})
    return devices


def scan_bluetooth_devices() -> list[dict]:
    """Scansione dei dispositivi Bluetooth vicini."""
    if bluetooth is None:
        return []
    devices = []
    try:
        nearby = bluetooth.discover_devices(duration=5, lookup_names=True)
        for addr, name in nearby:
            devices.append({"mac": addr, "name": name})
    except Exception:
        pass
    return devices


def _extract_domain(packet) -> str | None:
    if DNSQR and packet.haslayer(DNSQR):
        try:
            return packet[DNSQR].qname.decode().rstrip('.')
        except Exception:
            return None
    return None


def capture_dns_queries(duration: int = 30) -> list[str]:
    """Sniffa il traffico DNS per un certo periodo."""
    if sniff is None:
        return []
    queries = []
    packets = sniff(filter="udp port 53", timeout=duration)
    for p in packets:
        d = _extract_domain(p)
        if d:
            queries.append(d)
    return queries


def categorize_domain(domain: str) -> str:
    lower = domain.lower()
    for cat, keywords in CATEGORY_PATTERNS.items():
        for kw in keywords:
            if kw in lower:
                return cat
    return "altro"


def analyze_queries(queries: list[str]) -> dict:
    counts = defaultdict(int)
    for q in queries:
        counts[categorize_domain(q)] += 1
    total = sum(counts.values()) or 1
    return {c: round(v / total * 100, 2) for c, v in counts.items()}


def generate_report(devices: list[dict], bt_devices: list[dict], stats: dict) -> str:
    lines = [f"Report generato: {datetime.now().isoformat()}\n"]
    if devices:
        lines.append("Dispositivi Wi-Fi:")
        for d in devices:
            name = KNOWN_DEVICES.get(d.get("mac"), d.get("ip"))
            lines.append(f"- {name} ({d.get('ip')} {d.get('mac')})")
    if bt_devices:
        lines.append("\nDispositivi Bluetooth:")
        for b in bt_devices:
            lines.append(f"- {b.get('name','?')} ({b.get('mac')})")
    lines.append("\nPercentuali ricerche web:")
    for cat, perc in stats.items():
        lines.append(f"- {cat}: {perc}%")
    return "\n".join(lines)


def save_report(text: str, path: str = "logs/network_search_report.txt") -> str:
    Path("logs").mkdir(exist_ok=True)
    report_path = Path(path)
    report_path.write_text(text)
    return str(report_path)


def send_whatsapp_message(message: str):
    """Invia un messaggio WhatsApp se pywhatkit è disponibile."""
    if pywhatkit is None:
        return
    to = os.getenv("WHATSAPP_NUMBER")
    if not to:
        return
    try:
        pywhatkit.sendwhatmsg_instantly(to, message, wait_time=5, tab_close=True)
    except Exception:
        pass


def analyze_and_notify(duration: int = 30, network_range: str = "192.168.1.0/24"):
    wifi_devices = scan_wifi_network(network_range)
    bt_devices = scan_bluetooth_devices()
    queries = capture_dns_queries(duration)
    stats = analyze_queries(queries)
    report = generate_report(wifi_devices, bt_devices, stats)
    path = save_report(report)
    send_whatsapp_message(f"Analisi rete completata. Report in {path}")
    return report


if __name__ == "__main__":
    print(analyze_and_notify(5))
