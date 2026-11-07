from dataclasses import dataclass
from itertools import count

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
    particionMemoria(1, 0, 450)
]

#Implementación algoritmo BEST FIT
#Los parámetros que se pasan desde procesarArchivo
def bestFit (memoria, proceso):
    mejorHueco = None
    for i, v in enumerate(memoria):
        if v.proceso == None and v.proceso >= proceso.tamano:
            if mejorHueco == None or memoria[mejorHueco] < proceso.tamano:
                mejorHueco = i