from abc import ABC, abstractmethod


class Command(ABC):
    """Contrato base para acciones ejecutables del sistema."""

    @abstractmethod
    def execute(self):
        """Ejecuta la accion concreta del comando."""
