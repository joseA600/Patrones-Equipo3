from datetime import datetime
from typing import Any

from bson import ObjectId
from fastapi import HTTPException, status

from app.db import get_database
from app.models import PrestamoCreate
from app.services.material_service import update_material_estado
from patterns.command.base_command import Command
from patterns.state import normalizar_estado


class PrestarMaterialCommand(Command):
    """Comando para registrar un prestamo y marcar el material como prestado."""

    def __init__(self, payload: PrestamoCreate) -> None:
        self.payload = payload

    def execute(self) -> dict[str, Any]:
        if not ObjectId.is_valid(self.payload.material_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Id de material no valido",
            )

        database = get_database()
        material = database["materiales"].find_one(
            {"_id": ObjectId(self.payload.material_id)},
        )

        if material is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Material no encontrado",
            )

        if normalizar_estado(material["estado"]) != "Disponible":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Solo se pueden prestar materiales disponibles",
            )

        prestamo = {
            "material_id": self.payload.material_id,
            "material_nombre": material["nombre"],
            "solicitante": self.payload.solicitante,
            "estado": "activo",
            "fecha_prestamo": datetime.utcnow(),
            "fecha_devolucion": None,
        }

        inserted_id = database["prestamos"].insert_one(prestamo).inserted_id
        update_material_estado(self.payload.material_id, "Prestado")

        return database["prestamos"].find_one({"_id": inserted_id})
