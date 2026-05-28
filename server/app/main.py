from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import bitacora_router, health_router, materiales_router, prestamos_router


app = FastAPI(title=settings.app_name)

# CORS permite que el cliente React consuma la API durante desarrollo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(materiales_router)
app.include_router(bitacora_router)
app.include_router(prestamos_router)
