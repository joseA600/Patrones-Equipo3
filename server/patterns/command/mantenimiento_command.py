from typing import Any

from bson import ObjectId
from fastapi import HTTPException, status

from app.db import get_database
from app.services.material_service import update_material_estado
from patterns.command.base_command import Command


class EnviarMantenimientoCommand(Command):
    """Comando para enviar un material existente a mantenimiento."""

    def __init__(self, material_id: str) -> None:
        self.material_id = material_id

    def execute(self) -> dict[str, Any]:
        if not ObjectId.is_valid(self.material_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Id de material no valido",
            )

        material = get_database()["materiales"].find_one(
            {"_id": ObjectId(self.material_id)},
        )
        if material is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Material no encontrado",
            )

        update_material_estado(self.material_id, "EnMantenimiento")

        return get_database()["materiales"].find_one({"_id": ObjectId(self.material_id)})
