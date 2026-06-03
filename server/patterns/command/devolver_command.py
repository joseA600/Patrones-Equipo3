from datetime import datetime
from typing import Any

from bson import ObjectId
from fastapi import HTTPException, status
from pymongo import ReturnDocument

from app.db import get_database
from app.services.material_service import update_material_estado
from patterns.command.base_command import Command


class DevolverMaterialCommand(Command):
    """Comando para cerrar un prestamo activo y liberar el material."""

    def __init__(self, prestamo_id: str) -> None:
        self.prestamo_id = prestamo_id

    def execute(self) -> dict[str, Any]:
        if not ObjectId.is_valid(self.prestamo_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Id de prestamo no valido",
            )

        database = get_database()
        prestamo = database["prestamos"].find_one({"_id": ObjectId(self.prestamo_id)})

        if prestamo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prestamo no encontrado",
            )

        if prestamo["estado"] != "activo":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El prestamo ya fue devuelto",
            )

        update_material_estado(prestamo["material_id"], "Disponible")

        return database["prestamos"].find_one_and_update(
            {"_id": ObjectId(self.prestamo_id)},
            {
                "$set": {
                    "estado": "devuelto",
                    "fecha_devolucion": datetime.utcnow(),
                },
            },
            return_document=ReturnDocument.AFTER,
        )
