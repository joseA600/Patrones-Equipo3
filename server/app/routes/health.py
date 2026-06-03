from fastapi import APIRouter

from app.models import DatabaseStatusResponse, HealthResponse
from app.services import get_database_status, get_health_status


router = APIRouter(tags=["health"])


@router.get("/", response_model=HealthResponse)
def root() -> HealthResponse:
    """Endpoint base para confirmar que el servidor esta activo."""

    return get_health_status()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Endpoint explicito para monitoreo y pruebas iniciales."""

    return get_health_status()


@router.get("/db-status", response_model=DatabaseStatusResponse)
def database_status() -> DatabaseStatusResponse:
    """Endpoint para validar la conexion reutilizable a MongoDB."""

    return get_database_status()
