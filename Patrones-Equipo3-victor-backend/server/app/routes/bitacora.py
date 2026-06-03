from fastapi import APIRouter

from app.models import BitacoraResponse
from app.services import get_bitacora


router = APIRouter(prefix="/bitacora", tags=["bitacora"])


@router.get("", response_model=list[BitacoraResponse])
def list_bitacora() -> list[BitacoraResponse]:
    """Lista los eventos generados automaticamente por el patron Observer."""

    return get_bitacora()
