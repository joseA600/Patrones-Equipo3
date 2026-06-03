from abc import ABC, abstractmethod
from typing import Any


class EventObserver(ABC):
    """Contrato base para cualquier observador de eventos del sistema."""

    @abstractmethod
    def update(self, event: dict[str, Any]) -> None:
        """Recibe un evento emitido por el sujeto observado."""
