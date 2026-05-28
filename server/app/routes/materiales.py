from fastapi import APIRouter, status

from app.models import MaterialCreate, MaterialResponse
from app.services import create_material, get_materiales, get_materiales_disponibles


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
