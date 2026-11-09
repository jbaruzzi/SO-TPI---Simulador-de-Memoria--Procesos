"""Modelo compartido de un proceso del simulador."""

from dataclasses import dataclass, field


@dataclass
class Proceso:
    id: str
    arribo: int
    irrupcion: int
    tamano: int
    restante: int = field(init=False)
    estado: str = "Nuevo"  # Nuevo, Listo, Listo/Suspendido, Ejecución o Terminado.
    fin: int | None = None

    def __post_init__(self) -> None:
        self.restante = self.irrupcion
