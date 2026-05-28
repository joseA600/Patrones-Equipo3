from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


TipoMaterial = Literal["Laptop", "Router", "Proyector", "Adaptador", "Cable"]
EstadoMaterial = Literal["disponible", "mantenimiento", "no_disponible"]


class MaterialBase(BaseModel):
    """Datos compartidos para crear y responder materiales."""

    nombre: str = Field(..., min_length=2, max_length=100)
    tipo: TipoMaterial
    descripcion: Optional[str] = Field(default=None, max_length=250)
    estado: EstadoMaterial = "disponible"

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, value: str) -> str:
        """Evita nombres vacios o formados solo por espacios."""

        nombre = value.strip()
        if not nombre:
            raise ValueError("El nombre del material es obligatorio")

        return nombre


class MaterialCreate(MaterialBase):
    """Modelo de entrada para registrar un material."""


class MaterialResponse(MaterialBase):
    """Modelo de salida expuesto por la API."""

    id: str
    fecha_registro: datetime
