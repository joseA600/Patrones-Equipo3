from datetime import datetime
from typing import Any

from app.db import get_database
from patterns.observer.observer import EventObserver


class BitacoraObserver(EventObserver):
    """Observador encargado de persistir eventos en la coleccion bitacora."""

    collection_name = "bitacora"

    def update(self, event: dict[str, Any]) -> None:
        """Guarda automaticamente el evento recibido en MongoDB."""

        document = {
            "tipo_evento": event["tipo_evento"],
            "material_id": event["material_id"],
            "material_nombre": event["material_nombre"],
            "estado_anterior": event["estado_anterior"],
            "estado_nuevo": event["estado_nuevo"],
            "descripcion": event["descripcion"],
            "fecha": datetime.utcnow(),
        }

        get_database()[self.collection_name].insert_one(document)
