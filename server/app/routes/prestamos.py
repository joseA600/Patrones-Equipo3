from fastapi import APIRouter, status

from app.models import PrestamoCreate, PrestamoResponse
from app.services import create_prestamo, devolver_prestamo, get_prestamos


router = APIRouter(prefix="/prestamos", tags=["prestamos"])


@router.get("", response_model=list[PrestamoResponse])
def list_prestamos() -> list[PrestamoResponse]:
    """Lista prestamos registrados para reportes y devoluciones."""

    return get_prestamos()


@router.post("", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
def add_prestamo(payload: PrestamoCreate) -> PrestamoResponse:
    """Registra un prestamo y actualiza el estado del material."""

    return create_prestamo(payload)


@router.put("/{prestamo_id}/devolver", response_model=PrestamoResponse)
def return_prestamo(prestamo_id: str) -> PrestamoResponse:
    """Registra la devolucion de un prestamo activo."""

    return devolver_prestamo(prestamo_id)
