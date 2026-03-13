from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import time
import uuid

app = FastAPI(title="DevOps Todo API", version="1.0.0")

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── File-based storage (temporary until Docker phase) ──
DB_FILE = "todos.json"

def read_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def write_db(todos):
    with open(DB_FILE, "w") as f:
        json.dump(todos, f, indent=2)

# ── Pydantic models ──
class TodoCreate(BaseModel):
    task: str

# ── Health check ──
@app.get("/health")
async def health():
    return {"status": "ok", "uptime": time.time()}

# ── GET all todos ──
@app.get("/api/todos")
async def get_todos():
    todos = read_db()
    return todos

# ── POST create todo ──
@app.post("/api/todos", status_code=201)
async def create_todo(todo: TodoCreate):
    if not todo.task.strip():
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    todos = read_db()
    new_todo = {
        "id":        str(uuid.uuid4()),
        "task":      todo.task,
        "completed": False,
        "createdAt": str(time.time())
    }
    todos.append(new_todo)
    write_db(todos)
    return new_todo

# ── PATCH toggle complete ──
@app.patch("/api/todos/{todo_id}")
async def toggle_todo(todo_id: str):
    todos = read_db()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            write_db(todos)
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

# ── DELETE todo ──
@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: str):
    todos = read_db()
    filtered = [t for t in todos if t["id"] != todo_id]
    if len(filtered) == len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    write_db(filtered)
    return {"message": "Deleted successfully"}





