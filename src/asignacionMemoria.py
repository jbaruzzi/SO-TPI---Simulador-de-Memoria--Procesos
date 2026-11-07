from dataclasses import dataclass

@dataclass
class particionesMemoria:
    id: int
    inicio: int
    tamano: int
    proceso: str | None = None