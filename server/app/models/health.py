from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Modelo de respuesta para validar el estado inicial del servidor."""

    status: str
    message: str


class DatabaseStatusResponse(BaseModel):
    """Modelo de respuesta para reportar el estado de MongoDB."""

    status: str
    message: str
    database: str
