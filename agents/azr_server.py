"""azr_server.py
Modulo FastAPI che espone l'endpoint introspect per il Reasoner AZR.
Utilizzabile da Mercurius∞ per sapere se AZR è attivo.
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="AZR Server")

@app.get("/introspect")
def introspect():
    return {"status": "AZR is running", "version": "1.0", "agent": "AZR"}

def start_server(host: str = "0.0.0.0", port: int = 4010):
    uvicorn.run("agents.azr_server:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    start_server()
