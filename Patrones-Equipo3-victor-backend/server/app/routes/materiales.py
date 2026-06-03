from fastapi import APIRouter, status

from app.models import MaterialCreate, MaterialResponse, MaterialStateUpdate
from app.services import (
    create_material,
    delete_material,
    enviar_material_mantenimiento,
    get_materiales,
    get_materiales_disponibles,
    update_material_estado,
)


router = APIRouter(prefix="/materiales", tags=["materiales"])


@router.get("", response_model=list[MaterialResponse])
def list_materiales() -> list[MaterialResponse]:
    """Devuelve todos los materiales registrados en MongoDB."""

    return get_materiales()


@router.post("", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
def add_material(material: MaterialCreate) -> MaterialResponse:
    """Registra un nuevo material validado por el modelo y creado por Factory."""

    return create_material(material)


@router.get("/disponibles", response_model=list[MaterialResponse])
def list_materiales_disponibles() -> list[MaterialResponse]:
    """Devuelve solo los materiales marcados como disponibles."""

    return get_materiales_disponibles()


@router.patch("/{material_id}/estado", response_model=MaterialResponse)
def change_material_estado(
    material_id: str,
    payload: MaterialStateUpdate,
) -> MaterialResponse:
    """Actualiza el estado de un material solo si la transicion es valida."""

    return update_material_estado(material_id, payload.estado)


@router.put("/{material_id}/mantenimiento", response_model=MaterialResponse)
def send_material_mantenimiento(material_id: str) -> MaterialResponse:
    """Envia un material a mantenimiento mediante el patron Command."""

    return enviar_material_mantenimiento(material_id)


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_material(material_id: str) -> None:
    """Da de baja un material y lo elimina completamente de MongoDB."""

    delete_material(material_id)
