from abc import ABC, abstractmethod


class EstadoNoValidoError(ValueError):
    """Indica que el estado solicitado no existe dentro del patron State."""


class TransicionNoPermitidaError(ValueError):
    """Indica que una accion intenta mover el material a un estado invalido."""


class MaterialState(ABC):
    """Estado base para validar cambios de estado de un material."""

    nombre: str
    transiciones_permitidas: tuple[str, ...]

    @abstractmethod
    def puede_cambiar_a(self, nuevo_estado: str) -> bool:
        """Define si el estado actual permite moverse al siguiente estado."""


class Disponible(MaterialState):
    nombre = "Disponible"
    transiciones_permitidas = ("Prestado", "EnMantenimiento", "DadoDeBaja")

    def puede_cambiar_a(self, nuevo_estado: str) -> bool:
        return nuevo_estado in self.transiciones_permitidas


class Prestado(MaterialState):
    nombre = "Prestado"
    transiciones_permitidas = ("Disponible", "EnMantenimiento")

    def puede_cambiar_a(self, nuevo_estado: str) -> bool:
        return nuevo_estado in self.transiciones_permitidas


class EnMantenimiento(MaterialState):
    nombre = "EnMantenimiento"
    transiciones_permitidas = ("Disponible", "DadoDeBaja")

    def puede_cambiar_a(self, nuevo_estado: str) -> bool:
        return nuevo_estado in self.transiciones_permitidas


class DadoDeBaja(MaterialState):
    nombre = "DadoDeBaja"
    transiciones_permitidas: tuple[str, ...] = ()

    def puede_cambiar_a(self, nuevo_estado: str) -> bool:
        return False


_ESTADOS: dict[str, type[MaterialState]] = {
    Disponible.nombre: Disponible,
    Prestado.nombre: Prestado,
    EnMantenimiento.nombre: EnMantenimiento,
    DadoDeBaja.nombre: DadoDeBaja,
}

_ESTADOS_LEGACY = {
    "disponible": "Disponible",
    "prestado": "Prestado",
    "mantenimiento": "EnMantenimiento",
    "en_mantenimiento": "EnMantenimiento",
    "no_disponible": "DadoDeBaja",
    "dado_de_baja": "DadoDeBaja",
}


def normalizar_estado(nombre_estado: str) -> str:
    """Convierte alias antiguos al nombre oficial del estado."""

    return _ESTADOS_LEGACY.get(nombre_estado, nombre_estado)


def crear_estado(nombre_estado: str) -> MaterialState:
    """Crea el objeto estado correspondiente al nombre recibido."""

    nombre_estado = normalizar_estado(nombre_estado)
    estado = _ESTADOS.get(nombre_estado)
    if estado is None:
        raise EstadoNoValidoError(f"Estado no valido: {nombre_estado}")

    return estado()


def cambiar_estado(estado_actual: str, nuevo_estado: str) -> str:
    """Valida la transicion y devuelve el nuevo estado si esta permitida."""

    estado_actual = normalizar_estado(estado_actual)
    nuevo_estado = normalizar_estado(nuevo_estado)
    estado = crear_estado(estado_actual)
    crear_estado(nuevo_estado)

    if estado_actual == nuevo_estado:
        return nuevo_estado

    if not estado.puede_cambiar_a(nuevo_estado):
        raise TransicionNoPermitidaError(
            f"No se permite cambiar de {estado_actual} a {nuevo_estado}",
        )

    return nuevo_estado
