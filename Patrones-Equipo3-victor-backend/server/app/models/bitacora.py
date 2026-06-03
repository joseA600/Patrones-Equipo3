from datetime import datetime
from typing import Literal

from pydantic import BaseModel


TipoEventoBitacora = Literal["prestamo", "devolucion", "mantenimiento", "restauracion", "baja"]


class BitacoraResponse(BaseModel):
    """Modelo de salida para eventos registrados en la bitacora."""

    id: str
    tipo_evento: TipoEventoBitacora
    material_id: str
    material_nombre: str
    estado_anterior: str
    estado_nuevo: str
    descripcion: str
    fecha: datetime
