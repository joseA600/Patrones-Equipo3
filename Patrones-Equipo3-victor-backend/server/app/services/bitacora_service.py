from typing import Any

from app.db import get_database
from app.models import BitacoraResponse


COLLECTION_NAME = "bitacora"


def _collection():
    """Obtiene la coleccion de bitacora desde MongoDB."""

    return get_database()[COLLECTION_NAME]


def _serialize_event(document: dict[str, Any]) -> BitacoraResponse:
    """Convierte un documento de MongoDB al modelo publico de bitacora."""

    return BitacoraResponse(
        id=str(document["_id"]),
        tipo_evento=document["tipo_evento"],
        material_id=document["material_id"],
        material_nombre=document["material_nombre"],
        estado_anterior=document["estado_anterior"],
        estado_nuevo=document["estado_nuevo"],
        descripcion=document["descripcion"],
        fecha=document["fecha"],
    )


def get_bitacora() -> list[BitacoraResponse]:
    """Devuelve los eventos mas recientes registrados automaticamente."""

    documentos = _collection().find().sort("fecha", -1)

    return [_serialize_event(documento) for documento in documentos]
