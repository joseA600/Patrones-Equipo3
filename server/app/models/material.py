from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


TipoMaterial = Literal["Laptop", "Router", "Proyector", "Adaptador", "Cable"]
EstadoMaterial = Literal["Disponible", "Prestado", "EnMantenimiento", "DadoDeBaja"]

ESTADOS_LEGACY = {
    "disponible": "Disponible",
    "prestado": "Prestado",
    "mantenimiento": "EnMantenimiento",
    "en_mantenimiento": "EnMantenimiento",
    "no_disponible": "DadoDeBaja",
    "dado_de_baja": "DadoDeBaja",
}


class MaterialBase(BaseModel):
    """Datos compartidos para crear y responder materiales."""

    nombre: str = Field(..., min_length=2, max_length=100)
    tipo: TipoMaterial
    descripcion: Optional[str] = Field(default=None, max_length=250)
    estado: EstadoMaterial = "Disponible"

    @field_validator("estado", mode="before")
    @classmethod
    def normalize_estado(cls, value: str) -> str:
        """Normaliza estados antiguos o escritos en minusculas al formato actual."""

        if not isinstance(value, str):
            return value

        return ESTADOS_LEGACY.get(value.strip(), value.strip())

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

    @model_validator(mode="after")
    def validate_estado_inicial(self) -> "MaterialCreate":
        """Evita crear materiales ya prestados antes de implementar prestamos."""

        if self.estado == "Prestado":
            raise ValueError("No se puede registrar un material inicialmente prestado")

        return self


class MaterialStateUpdate(BaseModel):
    """Modelo de entrada para solicitar un cambio de estado."""

    estado: EstadoMaterial

    @field_validator("estado", mode="before")
    @classmethod
    def normalize_estado(cls, value: str) -> str:
        """Acepta alias simples y los convierte al nombre del estado."""

        if not isinstance(value, str):
            return value

        return ESTADOS_LEGACY.get(value.strip(), value.strip())


class MaterialResponse(MaterialBase):
    """Modelo de salida expuesto por la API."""

    id: str
    fecha_registro: datetime
