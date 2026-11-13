from dataclasses import dataclass
from itertools import count

@dataclass
class particionMemoria:
    id: int
    inicio: int
    tamano: int
    proceso: str | None = None

_id = count(2)  # los ids 0 y 1 son del SO y del hueco inicial

def crearMemoria():
    global _id
    _id = count(2)
    return [
        particionMemoria(0, 0, 100, proceso="SO"),  # reservada para el SO
        particionMemoria(1, 100, 450),  # espacio para procesos
    ]


# Best-Fit: elige el hueco libre más chico donde entre el proceso
def bestFit(memoria, proceso):
    mejorHueco = None
    for i, particion in enumerate(memoria):
        if particion.proceso is None and particion.tamano >= proceso.tamano:
            if mejorHueco is None or particion.tamano < memoria[mejorHueco].tamano:
                mejorHueco = i

    # No encontró espacio: el proceso pasa a listo-suspendido
    if mejorHueco is None:
        return False

    bestFitAgrega(memoria, proceso, mejorHueco)
    return True


def bestFitAgrega(memoria, proceso, mejorHueco):
    hueco = memoria[mejorHueco]
    sobrante = hueco.tamano - proceso.tamano

    # El hueco pasa a medir lo mismo que el proceso y se ocupa
    hueco.tamano = proceso.tamano
    hueco.proceso = str(proceso.id)

    # Si sobró espacio, se crea una partición libre justo a continuación
    if sobrante > 0:
        memoria.insert(
            mejorHueco + 1,
            particionMemoria(next(_id), hueco.inicio + hueco.tamano, sobrante),
        )


# Cuando un proceso termina, su partición queda libre (después se unen los huecos)
def liberarParticion(memoria, proceso):
    for particion in memoria:
        if particion.proceso == str(proceso.id):
            particion.proceso = None


# Une huecos libres contiguos (esto no es compactación)
def unirParticionesMemoria(memoria):
    i = 0
    while i < len(memoria) - 1:
        actual = memoria[i]
        siguiente = memoria[i + 1]
        if actual.proceso is None and siguiente.proceso is None:
            actual.tamano += siguiente.tamano
            memoria.pop(i + 1)
        else:
            i += 1
