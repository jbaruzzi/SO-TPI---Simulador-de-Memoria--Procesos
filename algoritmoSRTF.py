"""Funciones básicas del planificador SRTF."""

from .proceso import Proceso


def seleccionar_proceso(listos: list[Proceso]) -> Proceso | None:
    """Devuelve el proceso listo con menor tiempo de CPU restante.

    Si dos procesos tienen el mismo tiempo restante, conserva el primero de la
    cola. El simulador debe llamar esta función después de cada llegada para
    permitir que SRTF interrumpa al proceso que estaba ejecutándose.
    """
    if not listos:
        return None

    return min(listos, key=lambda proceso: proceso.restante)


def ejecutar_unidad(proceso: Proceso) -> bool:
    """Descuenta una unidad de CPU y devuelve True si el proceso terminó."""
    if proceso.restante <= 0:
        raise ValueError("No se puede ejecutar un proceso sin tiempo restante.")

    proceso.restante -= 1
    return proceso.restante == 0
