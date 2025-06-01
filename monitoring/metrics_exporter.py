# monitoring/metrics_exporter.py

"""
Modulo: metrics_exporter.py
Descrizione: Esporta metriche Prometheus per Mercurius∞ (HTTP 9100/metrics).
Raccoglie l’utilizzo di CPU e memoria e le espone come metriche Prometheus.

Metriche disponibili:
  • mercurius_cpu_usage_percent  → Percentuale di utilizzo CPU
  • mercurius_mem_usage_mb      → Memoria usata in MB

Il servizio HTTP di Prometheus viene avviato sulla porta 9100 all’esecuzione dello script.
Le metriche vengono aggiornate ogni 5 secondi.
"""

import time

import psutil
from prometheus_client import Gauge, start_http_server

# Creazione dei gauge Prometheus
CPU_USAGE = Gauge("mercurius_cpu_usage_percent", "CPU usage in percent")
MEM_USAGE = Gauge("mercurius_mem_usage_mb", "Memory usage in MB")


def collect_metrics():
    """
    Raccoglie le metriche di sistema:
      - CPU usage percentuale (valore 0-100)
      - Memoria usata in Megabyte (RAM utilizzata dal sistema)
    e aggiorna i corrispondenti Gauge Prometheus.
    """
    CPU_USAGE.set(psutil.cpu_percent())
    MEM_USAGE.set(psutil.virtual_memory().used / 1024 / 1024)


if __name__ == "__main__":
    # Avvia il server HTTP per Prometheus sulla porta 9100.
    # L’endpoint esposto sarà accessibile su http://<host>:9100/metrics
    start_http_server(9100)

    # Loop infinito: ogni 5 secondi raccoglie e aggiorna le metriche
    while True:
        collect_metrics()
        time.sleep(5)
