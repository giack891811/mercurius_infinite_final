from fastapi import FastAPI, WebSocket
from llm.llm_router import LLMRouter
import uvicorn

app = FastAPI(title="Aion API")
router = LLMRouter()

@app.post("/ask")
async def ask(payload: dict) -> dict:
    text = payload.get("prompt", "")
    if not text:
        return {"response": ""}
    reply = router.query(text)
    return {"response": reply}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            reply = router.query(data)
            await websocket.send_text(reply)
    except Exception:
        await websocket.close()


def start_api(host: str = "0.0.0.0", port: int = 8000) -> None:
    uvicorn.run(app, host=host, port=port)
