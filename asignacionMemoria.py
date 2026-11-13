from dataclasses import dataclass
from itertools import count

@dataclass
class particionMemoria:
    id: int
    inicio: int
    tamano: int
    proceso: str | None = None

# Se saltea la parte del SO
_id = count(2)

memoria = [
    #Reservada para el SO
    particionMemoria(0, 0, 100, proceso = "SO"),
    #Aca donde se agregan los procesos
    particionMemoria(1, 0, 450)
]

# Implementación algoritmo BEST FIT
# El parámetro proceso se pasa desde procesarArchivo.py
def bestFit (memoria, proceso):
    mejorHueco = None
    for i, v in enumerate(memoria):
        if v.proceso is None and v.proceso >= proceso.tamano:
            if mejorHueco is None or memoria[mejorHueco] < proceso.tamano:
                mejorHueco = i
    # No encontro espacio, pasa a listo-suspendido
    if mejorHueco is None:
        return False
        
    bestFitAgrega(memoria, proceso, mejorHueco)
    return True

def bestFitAgrega(mejorHueco):
    hueco = memoria[mejorHueco]
    sobrante = hueco.tamano - proceso.tamano
    # El hueco pasa a medir lo mismo que el proceso y se ocupa
    hueco.tamano = proceso.tamano
    hueco.proceso = proceso.id

    # Caso donde el hueco se divida entre el proceso y libre
    """
    mejorHueco + 1 -> crea bloque justo al lado de donde ocupamos
    particionMemoria -> llama a la clase para crear nueva instancia
    next(_id) -> id que hace unica a la partición
    hueco.inicio + hueco.tamano -> indican donde comienza el espacio libre
    sobrante -> asigna espacio a la partición libre
    """ 
    if sobrante > 0:
        memoria.insert(mejorHueco + 1, particionMemoria(next(_id), hueco.inicio + hueco.tamano, sobrante))
    return True

# Cuando hayan dos particiones seguidas que esten libres se deben unir para formar una unica partición (esto no es compactación)
def unirParticionesMemoria(memoria):
    i = 0
    while i < len(memoria) - 1:
        actual = memoria[i]
        siguiente = memoria[i + 1]
        if actual.proceso is None and siguiente.proceso is None:
            # Junta ambos huecos y "elimina" de la lista el hueco que absorvio
            actual.tamano += siguiente.tamano
            memoria.pop[i + 1]
        else:
            i += 1
