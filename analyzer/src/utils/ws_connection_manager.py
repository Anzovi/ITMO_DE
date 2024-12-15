from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        client_key = str(websocket.client)
        if client_key in self.active_connections:
            await self.active_connections[client_key].close()
        self.active_connections[client_key] = websocket

    async def disconnect(self, websocket: WebSocket):
        client_key = str(websocket.client)
        if client_key in self.active_connections:
            try:
                await websocket.close()
            except:  # noqa: E722
                pass
            finally:
                del self.active_connections[client_key]

    def is_connected(self, client_key: str):
        return client_key in self.active_connections

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in list(self.active_connections.values()):
            try:
                await connection.send_text(message)
            except (RuntimeError, ConnectionResetError, WebSocketDisconnect):
                await self.disconnect(connection)
