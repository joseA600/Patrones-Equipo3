from fastapi import APIRouter, status

from app.models import UsuarioCreate, UsuarioResponse
from app.services import create_usuario, get_usuarios


router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", response_model=list[UsuarioResponse])
def list_usuarios() -> list[UsuarioResponse]:
    """Lista usuarios disponibles para prestamos y administracion."""

    return get_usuarios()


@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def add_usuario(payload: UsuarioCreate) -> UsuarioResponse:
    """Registra un usuario nuevo en MongoDB."""

    return create_usuario(payload)
