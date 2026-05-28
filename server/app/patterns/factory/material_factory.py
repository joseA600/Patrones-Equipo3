from abc import ABC
from datetime import datetime
from typing import Any

from app.models import MaterialCreate


class MaterialCreator(ABC):
    """Clase base del Factory Method para construir documentos de materiales."""

    material_type: str

    def create(self, material: MaterialCreate) -> dict[str, Any]:
        """Construye el documento comun que sera guardado en MongoDB."""

        return {
            "nombre": material.nombre,
            "tipo": self.material_type,
            "descripcion": material.descripcion,
            "estado": material.estado,
            "fecha_registro": datetime.utcnow(),
        }


class LaptopCreator(MaterialCreator):
    material_type = "Laptop"


class RouterCreator(MaterialCreator):
    material_type = "Router"


class ProyectorCreator(MaterialCreator):
    material_type = "Proyector"


class AdaptadorCreator(MaterialCreator):
    material_type = "Adaptador"


class CableCreator(MaterialCreator):
    material_type = "Cable"


class MaterialFactory:
    """Selecciona el creador correcto segun el tipo solicitado."""

    _creators: dict[str, MaterialCreator] = {
        "Laptop": LaptopCreator(),
        "Router": RouterCreator(),
        "Proyector": ProyectorCreator(),
        "Adaptador": AdaptadorCreator(),
        "Cable": CableCreator(),
    }

    @classmethod
    def create_material(cls, material: MaterialCreate) -> dict[str, Any]:
        """Aplica Factory Method para generar el documento final."""

        creator = cls._creators.get(material.tipo)
        if creator is None:
            raise ValueError("Tipo de material no soportado")

        return creator.create(material)
