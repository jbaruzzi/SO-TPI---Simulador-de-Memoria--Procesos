# Importar dependecias
# from pathlib import Path
# Importar archivos
# from src import utilidades

# Constantes
maximaCantidadProcesos = 5
# carpeta = Path(__file__).resolve().parent / "src" / "test"

# Las diferentes colas
listosSupendidos = []
listos = []
suspendidos = []

# Función que permite seleccionar archivo.csv a utilizar
# def seleccionarArchivo():
#     archivos = sorted(Path(carpeta).glob("*.csv"))
#     if not archivos:
#         raise FileNotFoundError(f"No hay archivos .csv en la carpeta '{carpeta}")
# 
#     print("Archivos disponibles: ")
#     for i, archivo in enumerate(archivos):
#         print(f"{i}. {archivo.name}")
# 
#     while True:
#         opcion = input("Elegi el número correspondiente al archivo a utilizarse: ")
#         if (opcion.isdigit()) and (1 <= int(opcion) <= len(archivos)):
#             return archivos[int(opcion) - 1]
#         else:
#             print("Acción invaldia") 
# 
# ruta = seleccionarArchivo()
