from typing import Any

from bson import ObjectId

from app.db import get_database
from app.models import MaterialCreate, MaterialResponse
from app.patterns.factory import MaterialFactory


COLLECTION_NAME = "materiales"


def _collection():
    """Obtiene la coleccion de materiales desde la conexion reutilizable."""

    return get_database()[COLLECTION_NAME]


def _serialize_material(document: dict[str, Any]) -> MaterialResponse:
    """Convierte el documento de MongoDB al modelo de respuesta de la API."""

    return MaterialResponse(
        id=str(document["_id"]),
        nombre=document["nombre"],
        tipo=document["tipo"],
        descripcion=document.get("descripcion"),
        estado=document["estado"],
        fecha_registro=document["fecha_registro"],
    )


def get_materiales() -> list[MaterialResponse]:
    """Lista todos los materiales registrados."""

    documentos = _collection().find().sort("fecha_registro", -1)

    return [_serialize_material(documento) for documento in documentos]


def create_material(material: MaterialCreate) -> MaterialResponse:
    """Crea un material usando Factory Method y lo guarda en MongoDB."""

    material_document = MaterialFactory.create_material(material)
    inserted_id: ObjectId = _collection().insert_one(material_document).inserted_id
    inserted_document = _collection().find_one({"_id": inserted_id})

    return _serialize_material(inserted_document)


def get_materiales_disponibles() -> list[MaterialResponse]:
    """Lista unicamente materiales disponibles para futuros prestamos."""

    documentos = _collection().find({"estado": "disponible"}).sort(
        "fecha_registro",
        -1,
    )

    return [_serialize_material(documento) for documento in documentos]
