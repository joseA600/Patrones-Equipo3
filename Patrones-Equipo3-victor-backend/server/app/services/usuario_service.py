from datetime import datetime
from typing import Any

from fastapi import HTTPException, status

from app.db import get_database
from app.models import UsuarioCreate, UsuarioResponse


COLLECTION_NAME = "usuarios"


def _collection():
    """Obtiene la coleccion de usuarios desde MongoDB."""

    return get_database()[COLLECTION_NAME]


def _serialize_usuario(document: dict[str, Any]) -> UsuarioResponse:
    """Convierte un documento de MongoDB al contrato publico de usuarios."""

    return UsuarioResponse(
        id=str(document["_id"]),
        nombre=document["nombre"],
        correo=document["correo"],
        rol=document["rol"],
        fecha_registro=document["fecha_registro"],
    )


def get_usuarios() -> list[UsuarioResponse]:
    """Lista usuarios registrados ordenados por fecha."""

    documentos = _collection().find().sort("fecha_registro", -1)

    return [_serialize_usuario(documento) for documento in documentos]


def create_usuario(payload: UsuarioCreate) -> UsuarioResponse:
    """Registra un usuario evitando correos duplicados."""

    if _collection().find_one({"correo": payload.correo}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese correo",
        )

    document = {
        "nombre": payload.nombre,
        "correo": payload.correo,
        "rol": payload.rol,
        "fecha_registro": datetime.utcnow(),
    }
    inserted_id = _collection().insert_one(document).inserted_id
    usuario = _collection().find_one({"_id": inserted_id})

    return _serialize_usuario(usuario)
