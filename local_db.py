import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
DB_FILE = "orders.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Create tables & seed data once
conn = get_conn()
conn.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, service TEXT, created_at TEXT)")

if conn.execute("SELECT COUNT(*) FROM services").fetchone()[0] == 0:
    conn.executemany("INSERT INTO services (title) VALUES (?)", [("Express Delivery",), ("Standard Cleaning",), ("VIP Consultation",)])
    conn.executemany("INSERT INTO orders (name, phone, service, created_at) VALUES (?, ?, ?, ?)", [
        ("Ali", "+998901234567", "Express Delivery", "2026-11-23 10:00"),
        ("Madina", "+998937654321", "Standard Cleaning", "2026-11-23 11:30")
    ])
    conn.commit()
conn.close()

class OrderIn(BaseModel):
    name: str
    phone: str
    service: str

@app.get("/api/services")
def get_services():
    with get_conn() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM services").fetchall()]

@app.get("/api/orders")
def get_orders():
    with get_conn() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM orders").fetchall()]

@app.post("/api/orders")
def create_order(order: OrderIn):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO orders (name, phone, service, created_at) VALUES (?, ?, ?, ?)",
            (order.name, order.phone, order.service, created_at)
        )
        conn.commit()
        return {"id": cur.lastrowid, "name": order.name, "phone": order.phone, "service": order.service, "created_at": created_at}