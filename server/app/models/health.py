from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Modelo de respuesta para validar el estado inicial del servidor."""

    status: str
    message: str
