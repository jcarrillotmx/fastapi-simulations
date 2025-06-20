from fastapi import WebSocket, APIRouter, Form
from fastapi.responses import HTMLResponse
from typing import List
import json

notification = APIRouter()

# Conexiones WebSocket activas
active_connections: List[WebSocket] = []


@notification.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    print("📡 WebSocket conexión entrante...")
    await websocket.accept()
    print("✅ WebSocket aceptado")
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print("📥 Recibido:", data)
    except Exception as e:
        print("❌ WebSocket desconectado:", e)
        active_connections.remove(websocket)


@notification.get("/notification", response_class=HTMLResponse)
def get_form():
    return """
    <form action="/send-notification" method="post">
        <input type="text" name="title" placeholder="Título"/><br/>
        <input type="text" name="body" placeholder="Mensaje"/><br/>
        <button type="submit">Enviar Notificación</button>
    </form>
    """


@notification.post("/send-notification")
async def send_notification(
    title: str = Form(...),
    body: str = Form(...),
):
    payload = {
        "title": title,
        "body": body,
    }

    # Enviar la notificación a todos los clientes WebSocket conectados
    for connection in active_connections:
        await connection.send_text(json.dumps(payload))

    return {"success": True, "message": "Notificación enviada"}
