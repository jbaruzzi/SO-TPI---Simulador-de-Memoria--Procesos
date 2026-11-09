# Mientras no se defina el formato oficialmente lo tomo como si fuese .csv
import csv
from dataclasses import dataclass

@dataclass
class Proceso:
    id: int
    arribo: int
    irrupcion: int
    tamano: int
    
procesos = []

# Movi el archivo de prueba a src por simplicidad pero después deberia estar en test
def leerArchivo():
    with open('procesosTest1.csv', newline='') as procesosCSV:
        lectura = csv.DictReader(procesosCSV)
        # Por cada linea creo un objeto de Proceso. 
        # Hasta 10 se crean, los demás se ignoran.
        for i in lectura:
            pass