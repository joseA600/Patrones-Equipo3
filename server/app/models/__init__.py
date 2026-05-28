from app.models.bitacora import BitacoraResponse
from app.models.health import DatabaseStatusResponse, HealthResponse
from app.models.material import MaterialCreate, MaterialResponse, MaterialStateUpdate
from app.models.prestamo import PrestamoCreate, PrestamoResponse

__all__ = [
    "BitacoraResponse",
    "DatabaseStatusResponse",
    "HealthResponse",
    "MaterialCreate",
    "MaterialResponse",
    "MaterialStateUpdate",
    "PrestamoCreate",
    "PrestamoResponse",
]
