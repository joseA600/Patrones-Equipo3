from typing import Any

from patterns.observer.bitacora_observer import BitacoraObserver
from patterns.observer.observer import EventObserver


class EventManager:
    """Sujeto observado que notifica eventos a todos sus observadores."""

    def __init__(self) -> None:
        self._observers: list[EventObserver] = []

    def attach(self, observer: EventObserver) -> None:
        """Registra un observador si aun no esta suscrito."""

        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: EventObserver) -> None:
        """Retira un observador registrado."""

        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: dict[str, Any]) -> None:
        """Propaga el evento a cada observador suscrito."""

        for observer in self._observers:
            observer.update(event)


event_manager = EventManager()
event_manager.attach(BitacoraObserver())


def get_event_manager() -> EventManager:
    """Devuelve el administrador global de eventos del backend."""

    return event_manager
