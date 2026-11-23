from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

services = [
    {"id": 1, "title": "Express Delivery"},
    {"id": 2, "title": "Standard Cleaning"},
    {"id": 3, "title": "VIP Consultation"}
]

orders = [
    {"id": 1, "name": "Ali", "phone": "+998901234567", "service": "Express Delivery", "created_at": "2026-11-23 10:00"},
    {"id": 2, "name": "Madina", "phone": "+998937654321", "service": "Standard Cleaning", "created_at": "2026-11-23 11:30"}
]

class OrderIn(BaseModel):
    name: str
    phone: str
    service: str

@app.get("/api/services")
def get_services():
    return services

@app.get("/api/orders")
def get_orders():
    return orders

@app.post("/api/orders")
def create_order(order: OrderIn):
    new_order = {
        "id": len(orders) + 1,
        "name": order.name,
        "phone": order.phone,
        "service": order.service,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    orders.append(new_order)
    return new_order