# Simulador de Asignación de Memoria y Planificación de Procesos

TPI de Sistemas Operativos — UTN FRRe — Grupo 3

Simulador por consola de:

- **Memoria:** particiones variables (MVT), 100K para el SO y 450K para procesos de usuario, política **Best-Fit**.
- **CPU:** un solo procesador con planificación **SRTF** (expropiativo).
- **Grado de multiprogramación:** como máximo 5 procesos entre Ejecución, Listos y Listos/Suspendidos.
- **Estados:** Nuevo, Listo, Listo/Suspendido, Ejecución y Terminado.

---

## HOWTO: cómo ejecutarlo

### Opción A: con el ejecutable (no hace falta instalar Python)

Los ejecutables están en la carpeta `ejecutable/`, cada uno con su carpeta `test/` con los lotes de prueba al lado:

```
ejecutable/
├── windows/
│   ├── simulador.exe
│   └── test/
└── linux/
    ├── simulador
    └── test/
```

**Windows**

1. Abrir la carpeta `ejecutable\windows`.
2. Hacer doble clic en `simulador.exe`, o desde una consola (cmd / PowerShell):
   ```
   cd ejecutable\windows
   simulador.exe
   ```

> Si Windows SmartScreen muestra "Windows protegió su PC", hacer clic en **Más información → Ejecutar de todas formas** (el ejecutable no está firmado digitalmente).

**Linux**

```bash
cd ejecutable/linux
chmod +x simulador   # solo la primera vez, si no tiene permiso de ejecución
./simulador
```

> La carpeta `test/` tiene que quedar **al lado del ejecutable**: de ahí se toma el lote de prueba por defecto.

### Opción B: desde el código fuente

Requisito: **Python 3.10 o superior** (no usa librerías externas).

```bash
python simulador.py      # Windows
python3 simulador.py     # Linux / macOS
```

Ejecutarlo desde la carpeta del proyecto (donde está `simulador.py`).

---

## Uso del simulador

Al iniciar se muestra el menú:

```
1. Cargar archivos .csv
2. Iniciar simulación
3. Información sobre el simulador
4. Salir
```

1. **Cargar archivos .csv** — pide la ruta del archivo con los procesos. Se puede escribir la ruta o arrastrar el archivo a la consola. El archivo se valida en el momento.
2. **Iniciar simulación** — corre la simulación con el archivo cargado. **Si no se cargó ninguno, usa `test/lotePrueba1.csv`.**
3. **Información sobre el simulador** — resumen de las reglas de la simulación.
4. **Salir.**

Durante la simulación, el programa **se detiene en cada evento** (llega un proceso o termina un proceso) y muestra:

- el estado del procesador (proceso en ejecución),
- la tabla de particiones de memoria (Id de partición, dirección de comienzo, tamaño, proceso asignado y fragmentación interna),
- la cola de Listos, la de Listos/Suspendidos y los procesos nuevos esperando cupo.

Hay que presionar **Enter** para avanzar al siguiente evento. Al terminar todos los procesos se muestra el **informe final**: tiempo de retorno y de espera de cada proceso, los promedios y el rendimiento del sistema (procesos terminados por unidad de tiempo).

---

## Formato del archivo de procesos (.csv)

Primera línea con el encabezado `ID,TA,TI,TAM` y luego un proceso por línea:

| Columna | Significado | Restricción |
|---|---|---|
| `ID` | Identificador del proceso | Único, no vacío |
| `TA` | Tiempo de arribo | Entero ≥ 0 |
| `TI` | Tiempo de irrupción (CPU) | Entero > 0 |
| `TAM` | Tamaño del proceso en K | Entero > 0 y ≤ 450 |

Como máximo **10 procesos** por archivo.

Ejemplo:

```csv
ID,TA,TI,TAM
P1,3,2,120
P2,10,4,130
P3,10,1,40
P4,14,2,60
P5,20,2,90
```

### Lotes de prueba incluidos (`test/`)

| Archivo | Contenido |
|---|---|
| `lotePrueba1.csv` | 5 procesos con arribos espaciados (lote por defecto). |
| `lotePrueba3.csv` | 8 procesos, varios llegan juntos: muestra el límite de 5 procesos, Listo/Suspendido por falta de hueco y la expropiación de SRTF. |
| `lotePrueba6.csv` | 12 procesos: el simulador lo rechaza por superar el máximo de 10. |

---

## Estructura del código

| Archivo | Responsabilidad |
|---|---|
| `simulador.py` | Menú, bucle principal de la simulación por eventos, salidas e informe final. |
| `procesarArchivo.py` | Lectura y validación del CSV. |
| `proceso.py` | Clase `Proceso` (datos y estado de cada proceso). |
| `asignacionMemoria.py` | Memoria MVT: Best-Fit, liberación de particiones y unión de huecos contiguos. |
| `algoritmoSRTF.py` | Selección del proceso con menor tiempo restante. |

---

## Cómo regenerar los ejecutables

Se generan con [PyInstaller](https://pyinstaller.org/) (un ejecutable por sistema operativo; hay que generarlo **en** ese sistema):

```bash
pip install pyinstaller
pyinstaller --onefile --name simulador simulador.py
```

El ejecutable queda en `dist/`. Copiar la carpeta `test/` al lado del ejecutable.
