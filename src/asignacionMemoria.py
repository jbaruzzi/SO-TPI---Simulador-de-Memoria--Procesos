from dataclasses import dataclass

@dataclass
class particionMemoria:
    id: int
    inicio: int
    tamano: int
    proceso: str | None = None

memoria = [
    #Reservada para el SO
    particionMemoria(0, 0, 100, proceso = "SO"),
    #Aca donde se agregan los procesos
    particionMemoria()
]