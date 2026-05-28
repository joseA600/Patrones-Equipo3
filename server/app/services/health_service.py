from app.models import HealthResponse


def get_health_status() -> HealthResponse:
    """Centraliza la respuesta inicial del servidor."""

    return HealthResponse(status="ok", message="Servidor funcionando")
