"""
dashboard_stub.py
=================
Stub di interfaccia CLI / Web Mercurius∞.
"""

class DashboardStub:
    def __init__(self):
        self.kpi = {}

    def update(self, name, value):
        self.kpi[name] = value

    def show(self):
        print("=== MERCURIUS∞ DASHBOARD ===")
        for k, v in self.kpi.items():
            print(f"{k:<15}: {v}")
