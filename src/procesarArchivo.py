# Mientras no se defina el formato oficialmente lo tomo como si fuese .csv
import csv

def leerArchivo(ruta):
    with open(ruta, newline='') as procesosCSV:
        lectura = csv.DictReader(procesosCSV)

    print(lectura)