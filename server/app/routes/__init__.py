from app.routes.bitacora import router as bitacora_router
from app.routes.health import router as health_router
from app.routes.materiales import router as materiales_router
from app.routes.prestamos import router as prestamos_router
from app.routes.usuarios import router as usuarios_router

__all__ = [
    "bitacora_router",
    "health_router",
    "materiales_router",
    "prestamos_router",
    "usuarios_router",
]
