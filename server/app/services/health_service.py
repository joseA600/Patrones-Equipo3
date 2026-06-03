from app.db import check_database_connection
from app.models import DatabaseStatusResponse, HealthResponse


def get_health_status() -> HealthResponse:
    """Centraliza la respuesta inicial del servidor."""

    return HealthResponse(status="ok", message="Servidor funcionando")


def get_database_status() -> DatabaseStatusResponse:
    """Centraliza la validacion de conexion a MongoDB."""

    status = check_database_connection()

    return DatabaseStatusResponse(**status)
