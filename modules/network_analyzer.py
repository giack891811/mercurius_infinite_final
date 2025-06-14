# modules/network_analyzer.py
"""
Network scanner & keyword extractor — versione **fixed**.
Ora usa Bleak invece del vecchio modulo bluetooth.
"""

from scapy.all import ARP, Ether, srp, sniff, DNSQR

# 🔄 nuovo import BLE
try:
    from bleak import BleakScanner            # libreria cross-platform
except ImportError:                           # pragma: no cover
    BleakScanner = None                       # fallback se bleak assente

# ------------------------------------------------------------------
def scan_bluetooth(timeout: int = 4) -> list[str]:
    """Ritorna una lista di MAC address BLE trovati."""
    if BleakScanner is None:
        return []            # nessuna scansione, libreria non presente
    devices = BleakScanner.discover(timeout=timeout)
    return [d.address for d in devices]

# (Altre funzioni originali restano qui, intatte / placeholder)
# ------------------------------------------------------------------