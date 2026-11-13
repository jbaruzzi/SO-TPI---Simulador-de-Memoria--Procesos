"""Lectura y validación del archivo CSV de procesos."""

import csv
import sys
from pathlib import Path

from proceso import Proceso


MAX_PROCESOS_CARGADOS = 10
MEMORIA_USUARIOS = 450  # K disponibles para procesos (el SO ocupa los 100K restantes)

# Carpeta donde está el programa: si se entrega como ejecutable (.exe) es la
# carpeta del ejecutable, si se corre con Python es la carpeta de este módulo.
if getattr(sys, "frozen", False):
    CARPETA_BASE = Path(sys.executable).resolve().parent
else:
    CARPETA_BASE = Path(__file__).resolve().parent

# Archivo que se usa cuando no se carga ningún .csv desde el menú
ARCHIVO_POR_DEFECTO = CARPETA_BASE / "test" / "lotePrueba1.csv"
COLUMNAS_REQUERIDAS = {"ID", "TA", "TI", "TAM"}


def _leer_entero(fila: dict[str, str | None], columna: str, numero_fila: int) -> int:
    valor = (fila.get(columna) or "").strip()
    if not valor:
        raise ValueError(f"Falta el valor de {columna} en la fila {numero_fila}.")

    try:
        return int(valor)
    except ValueError as error:
        raise ValueError(
            f"El valor de {columna} en la fila {numero_fila} debe ser un entero."
        ) from error


def leer_archivo(ruta: str | Path | None = None) -> list[Proceso]:
    """Lee ID, TA (arribo), TI (CPU) y TAM (memoria en KB) desde un CSV.

    Si no se indica una ruta, usa el archivo de prueba que está junto a este
    módulo. Las rutas relativas que se pasan como argumento se resuelven desde
    el directorio desde donde se ejecutó el programa.
    """
    archivo = Path(ruta) if ruta is not None else ARCHIVO_POR_DEFECTO
    procesos: list[Proceso] = []
    ids_vistos: set[str] = set()

    with archivo.open("r", newline="", encoding="utf-8-sig") as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        if lector.fieldnames is None:
            raise ValueError("El archivo CSV está vacío o no tiene encabezado.")

        lector.fieldnames = [(nombre or "").strip() for nombre in lector.fieldnames]
        faltantes = COLUMNAS_REQUERIDAS - set(lector.fieldnames)
        if faltantes:
            columnas = ", ".join(sorted(faltantes))
            raise ValueError(f"Faltan columnas requeridas en el CSV: {columnas}.")

        for numero_fila, fila in enumerate(lector, start=2):
            # Ignora líneas vacías entre registros.
            if not any(valor and valor.strip() for valor in fila.values() if isinstance(valor, str)):
                continue

            if len(procesos) == MAX_PROCESOS_CARGADOS:
                raise ValueError(
                    f"El archivo supera el máximo de {MAX_PROCESOS_CARGADOS} procesos."
                )

            identificador = (fila.get("ID") or "").strip()
            if not identificador:
                raise ValueError(f"Falta el ID del proceso en la fila {numero_fila}.")
            if identificador in ids_vistos:
                raise ValueError(f"El ID {identificador} está repetido en el CSV.")

            arribo = _leer_entero(fila, "TA", numero_fila)
            irrupcion = _leer_entero(fila, "TI", numero_fila)
            tamano = _leer_entero(fila, "TAM", numero_fila)

            if arribo < 0:
                raise ValueError(f"El arribo de la fila {numero_fila} no puede ser negativo.")
            if irrupcion <= 0:
                raise ValueError(f"El tiempo de CPU de la fila {numero_fila} debe ser positivo.")
            if tamano <= 0:
                raise ValueError(f"El tamaño de la fila {numero_fila} debe ser positivo.")
            if tamano > MEMORIA_USUARIOS:
                raise ValueError(
                    f"El tamaño de la fila {numero_fila} supera los {MEMORIA_USUARIOS}K de memoria para procesos."
                )

            procesos.append(
                Proceso(
                    id=identificador,
                    arribo=arribo,
                    irrupcion=irrupcion,
                    tamano=tamano,
                )
            )
            ids_vistos.add(identificador)

    return procesos
