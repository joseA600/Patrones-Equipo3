from typing import Any

from app.db import get_database
from app.models import PrestamoCreate, PrestamoResponse
from patterns.command import DevolverMaterialCommand, PrestarMaterialCommand


COLLECTION_NAME = "prestamos"


def _serialize_prestamo(document: dict[str, Any]) -> PrestamoResponse:
    """Convierte un documento de MongoDB al contrato publico de prestamos."""

    return PrestamoResponse(
        id=str(document["_id"]),
        material_id=document["material_id"],
        material_nombre=document["material_nombre"],
        solicitante=document["solicitante"],
        estado=document["estado"],
        fecha_prestamo=document["fecha_prestamo"],
        fecha_devolucion=document.get("fecha_devolucion"),
    )


def create_prestamo(payload: PrestamoCreate) -> PrestamoResponse:
    """Ejecuta el comando de prestamo."""

    prestamo = PrestarMaterialCommand(payload).execute()

    return _serialize_prestamo(prestamo)


def get_prestamos() -> list[PrestamoResponse]:
    """Lista prestamos registrados, primero los mas recientes."""

    documentos = get_database()[COLLECTION_NAME].find().sort("fecha_prestamo", -1)

    return [_serialize_prestamo(documento) for documento in documentos]


def devolver_prestamo(prestamo_id: str) -> PrestamoResponse:
    """Ejecuta el comando de devolucion."""

    prestamo = DevolverMaterialCommand(prestamo_id).execute()

    return _serialize_prestamo(prestamo)
