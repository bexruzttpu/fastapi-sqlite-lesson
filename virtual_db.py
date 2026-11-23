from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime

DATABASE_URL = "sqlite:///./orders.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ServiceDB(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    service = Column(String)
    created_at = Column(String)

Base.metadata.create_all(bind=engine)

# Seed initial data once if empty
db_init = SessionLocal()
if db_init.query(ServiceDB).count() == 0:
    db_init.add_all([
        ServiceDB(title="Express Delivery"),
        ServiceDB(title="Standard Cleaning"),
        ServiceDB(title="VIP Consultation")
    ])
    db_init.add_all([
        OrderDB(name="Ali", phone="+998901234567", service="Express Delivery", created_at="2026-11-23 10:00"),
        OrderDB(name="Madina", phone="+998937654321", service="Standard Cleaning", created_at="2026-11-23 11:30")
    ])
    db_init.commit()
db_init.close()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class OrderIn(BaseModel):
    name: str
    phone: str
    service: str

@app.get("/api/services")
def get_services(db: Session = Depends(get_db)):
    return db.query(ServiceDB).all()

@app.get("/api/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(OrderDB).all()

@app.post("/api/orders")
def create_order(order: OrderIn, db: Session = Depends(get_db)):
    new_order = OrderDB(
        name=order.name,
        phone=order.phone,
        service=order.service,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order