from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


RolUsuario = Literal["Alumno", "Docente", "Administrador"]


class UsuarioCreate(BaseModel):
    """Datos requeridos para registrar usuarios del sistema."""

    nombre: str = Field(..., min_length=2, max_length=100)
    correo: str = Field(..., min_length=5, max_length=120)
    rol: RolUsuario = "Alumno"

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, value: str) -> str:
        nombre = value.strip()
        if not nombre:
            raise ValueError("El nombre del usuario es obligatorio")

        return nombre

    @field_validator("correo")
    @classmethod
    def validate_correo(cls, value: str) -> str:
        correo = value.strip().lower()
        if "@" not in correo or "." not in correo:
            raise ValueError("El correo no tiene un formato valido")

        return correo


class UsuarioResponse(UsuarioCreate):
    """Modelo publico para usuarios almacenados en MongoDB."""

    id: str
    fecha_registro: datetime
