from fastapi import FastAPI
from app.api.routes_customers import router as customers_router
from app.db.database import Base, engine

app = FastAPI(title="Veribakery API")

# Crear tablas en SQLite si no existen
Base.metadata.create_all(bind=engine)

app.include_router(customers_router)