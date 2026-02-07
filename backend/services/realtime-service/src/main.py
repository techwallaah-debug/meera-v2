"""
Real-time Service - WebSocket for live updates
Port: 8009
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Set
import json
import asyncio
from datetime import datetime

app = FastAPI(title="Real-time Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        self.user_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        self.user_connections[id(websocket)] = user_id
    
    def disconnect(self, websocket: WebSocket):
        user_id = self.user_connections.get(id(websocket))
        if user_id and user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        if id(websocket) in self.user_connections:
            del self.user_connections[id(websocket)]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def broadcast_to_user(self, user_id: int, message: dict):
        if user_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.add(connection)
            for conn in disconnected:
                self.active_connections[user_id].discard(conn)
    
    async def broadcast_to_all(self, message: dict):
        disconnected_users = []
        for user_id, connections in self.active_connections.items():
            disconnected = set()
            for connection in connections:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.add(connection)
            for conn in disconnected:
                connections.discard(conn)
            if not connections:
                disconnected_users.append(user_id)
        for user_id in disconnected_users:
            del self.active_connections[user_id]

manager = ConnectionManager()

@app.get("/")
async def root():
    return {
        "service": "Real-time Service",
        "status": "running",
        "version": "1.0.0",
        "active_connections": sum(len(conns) for conns in manager.active_connections.values())
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        # Send welcome message
        await manager.send_personal_message({
            "type": "connected",
            "message": "Connected to real-time service",
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
        
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                if message_type == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    }, websocket)
                elif message_type == "subscribe":
                    # Subscribe to specific channels
                    channels = message.get("channels", [])
                    await manager.send_personal_message({
                        "type": "subscribed",
                        "channels": channels,
                        "timestamp": datetime.utcnow().isoformat()
                    }, websocket)
                
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON"
                }, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# API endpoints to trigger broadcasts
@app.post("/notify/user/{user_id}")
async def notify_user(user_id: int, notification: dict):
    """Send notification to specific user"""
    await manager.broadcast_to_user(user_id, {
        "type": "notification",
        "data": notification,
        "timestamp": datetime.utcnow().isoformat()
    })
    return {"message": "Notification sent", "user_id": user_id}

@app.post("/notify/all")
async def notify_all(notification: dict):
    """Broadcast to all connected users"""
    await manager.broadcast_to_all({
        "type": "broadcast",
        "data": notification,
        "timestamp": datetime.utcnow().isoformat()
    })
    return {"message": "Broadcast sent"}

@app.post("/notify/post/{post_id}")
async def notify_post_update(post_id: int, update: dict):
    """Notify users about post updates (likes, comments)"""
    # TODO: Get users following/interested in this post
    # For now, broadcast to all
    await manager.broadcast_to_all({
        "type": "post_update",
        "post_id": post_id,
        "data": update,
        "timestamp": datetime.utcnow().isoformat()
    })
    return {"message": "Post update broadcasted", "post_id": post_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
