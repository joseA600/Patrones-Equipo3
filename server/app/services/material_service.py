from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
from fastapi import HTTPException, status
from pymongo import ReturnDocument

from app.db import get_database
from app.models import MaterialCreate, MaterialResponse
from app.patterns.factory import MaterialFactory
from patterns.state import (
    EstadoNoValidoError,
    TransicionNoPermitidaError,
    cambiar_estado,
    normalizar_estado,
)
from patterns.observer import get_event_manager


COLLECTION_NAME = "materiales"


def _get_event_type(estado_anterior: str, estado_nuevo: str) -> Optional[str]:
    """Traduce cambios de estado en eventos de negocio observables."""

    if estado_anterior == "Disponible" and estado_nuevo == "Prestado":
        return "prestamo"
    if estado_anterior == "Prestado" and estado_nuevo == "Disponible":
        return "devolucion"
    if estado_nuevo == "EnMantenimiento":
        return "mantenimiento"
    if estado_anterior == "EnMantenimiento" and estado_nuevo == "Disponible":
        return "restauracion"
    if estado_nuevo == "DadoDeBaja":
        return "baja"

    return None


def _build_event_description(
    tipo_evento: str,
    estado_anterior: str,
    estado_nuevo: str,
) -> str:
    """Genera una descripcion simple para la bitacora."""

    descriptions = {
        "prestamo": "Material marcado como prestado",
        "devolucion": "Material devuelto y marcado como disponible",
        "mantenimiento": "Material enviado a mantenimiento",
        "restauracion": "Material restaurado desde mantenimiento a disponible",
        "baja": "Material dado de baja y eliminado del sistema",
    }

    return descriptions.get(
        tipo_evento,
        f"Cambio de estado de {estado_anterior} a {estado_nuevo}",
    )


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
        estado=normalizar_estado(document["estado"]),
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

    documentos = _collection().find(
        {"estado": {"$in": ["Disponible", "disponible"]}},
    ).sort("fecha_registro", -1)

    return [_serialize_material(documento) for documento in documentos]


def update_material_estado(material_id: str, nuevo_estado: str) -> MaterialResponse:
    """Cambia el estado de un material usando el patron State."""

    if not ObjectId.is_valid(material_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de material no valido",
        )

    material = _collection().find_one({"_id": ObjectId(material_id)})
    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material no encontrado",
        )

    estado_anterior = normalizar_estado(material["estado"])

    try:
        estado_validado = cambiar_estado(estado_anterior, nuevo_estado)
    except EstadoNoValidoError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except TransicionNoPermitidaError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    updated_material = _collection().find_one_and_update(
        {"_id": ObjectId(material_id)},
        {
            "$set": {"estado": estado_validado},
            "$push": {
                "historial_estados": {
                    "estado": estado_validado,
                    "motivo": "Cambio validado por patron State",
                    "fecha": datetime.utcnow(),
                },
            },
        },
        return_document=ReturnDocument.AFTER,
    )

    tipo_evento = _get_event_type(estado_anterior, estado_validado)
    if tipo_evento is not None:
        # Observer registra automaticamente la bitacora sin acoplar la ruta a MongoDB.
        get_event_manager().notify(
            {
                "tipo_evento": tipo_evento,
                "material_id": str(updated_material["_id"]),
                "material_nombre": updated_material["nombre"],
                "estado_anterior": estado_anterior,
                "estado_nuevo": estado_validado,
                "descripcion": _build_event_description(
                    tipo_evento,
                    estado_anterior,
                    estado_validado,
                ),
            },
        )

    return _serialize_material(updated_material)


def enviar_material_mantenimiento(material_id: str) -> MaterialResponse:
    """Ejecuta el comando para enviar un material a mantenimiento."""

    from patterns.command.mantenimiento_command import EnviarMantenimientoCommand

    material = EnviarMantenimientoCommand(material_id).execute()

    return _serialize_material(material)


def delete_material(material_id: str) -> None:
    """Da de baja un material: registra el evento en bitacora y lo elimina de MongoDB."""

    if not ObjectId.is_valid(material_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de material no valido",
        )

    material = _collection().find_one({"_id": ObjectId(material_id)})
    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material no encontrado",
        )

    estado_actual = normalizar_estado(material["estado"])

    try:
        cambiar_estado(estado_actual, "DadoDeBaja")
    except TransicionNoPermitidaError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    get_event_manager().notify(
        {
            "tipo_evento": "baja",
            "material_id": str(material["_id"]),
            "material_nombre": material["nombre"],
            "estado_anterior": estado_actual,
            "estado_nuevo": "DadoDeBaja",
            "descripcion": _build_event_description("baja", estado_actual, "DadoDeBaja"),
        },
    )

    _collection().delete_one({"_id": ObjectId(material_id)})
