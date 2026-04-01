from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
from prometheus_fastapi_instrumentator import Instrumentator
import os
import time
import psutil

load_dotenv()

app = FastAPI(title="DevOps Todo API", version="1.0.0")
# ── Prometheus metrics ──
Instrumentator().instrument(app).expose(app)

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── MongoDB Connection ──
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client     = AsyncIOMotorClient(MONGO_URI)
db         = client.tododb
collection = db.todos

# ── Models ──
class TodoCreate(BaseModel):
    task: str

# ── Helper ──
def serialize(todo) -> dict:
    return {
        "id":        str(todo["_id"]),
        "task":      todo["task"],
        "completed": todo.get("completed", False),
        "createdAt": todo.get("createdAt", "")
    }

# ── Health Check ──
@app.get("/health")
async def health():
    return {"status": "ok", "uptime": time.time()}

# ── GET all todos ──
@app.get("/api/todos")
async def get_todos():
    try:
        todos = await collection.find().sort("_id", -1).to_list(100)
        return [serialize(t) for t in todos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── POST create todo ──
@app.post("/api/todos", status_code=201)
async def create_todo(todo: TodoCreate):
    if not todo.task.strip():
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    doc = {"task": todo.task, "completed": False, "createdAt": str(time.time())}
    result = await collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize(doc)

# ── PATCH toggle ──
@app.patch("/api/todos/{todo_id}")
async def toggle_todo(todo_id: str):
    todo = await collection.find_one({"_id": ObjectId(todo_id)})
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    new_status = not todo.get("completed", False)
    await collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": {"completed": new_status}}
    )
    todo["completed"] = new_status
    return serialize(todo)

# ── DELETE todo ──
@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: str):
    result = await collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Deleted successfully"}