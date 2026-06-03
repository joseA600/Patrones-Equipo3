from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


EstadoPrestamo = Literal["activo", "devuelto"]


class PrestamoCreate(BaseModel):
    """Datos minimos para registrar un prestamo academico."""

    material_id: str
    solicitante: str = Field(..., min_length=2, max_length=100)

    @field_validator("solicitante")
    @classmethod
    def validate_solicitante(cls, value: str) -> str:
        """Evita prestamos sin responsable."""

        solicitante = value.strip()
        if not solicitante:
            raise ValueError("El solicitante es obligatorio")

        return solicitante


class PrestamoResponse(BaseModel):
    """Modelo de salida para prestamos registrados."""

    id: str
    material_id: str
    material_nombre: str
    solicitante: str
    estado: EstadoPrestamo
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime] = None
