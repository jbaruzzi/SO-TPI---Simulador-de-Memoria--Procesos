# Importar dependecias
from algoritmoSRTF import seleccionar_proceso, ejecutar_unidad
from asignacionMemoria import crearMemoria, bestFit, liberarParticion, unirParticionesMemoria
from procesarArchivo import leer_archivo, ARCHIVO_POR_DEFECTO

# Constantes
maximaCantidadProcesos = 5
opcionesMenu = [1,2,3,4]

# Archivo .csv que el usuario cargó desde el menú (None = se usa el de la carpeta test)
archivoCargado = None

# Las diferentes colas
listosSupendidos = []
listos = []
suspendidos = []

# Estructura del menú para el simulador (todo por consola)
def mostrarMenu():
    print("=================================================")
    print("SIMULADOR DE PROCESOS Y MEMORIA | SO | GRUPO 3")
    print("=================================================")
    print("1. Cargar archivos .csv")
    print(
        "2. Iniciar simulación \n"
        "   De no cargar un archivo .csv se utilizaran los \n" \
        "   lotes de prueba por defecto"
    )
    print("3. Información sobre el simulador")
    print("4. Salir")
    print("=================================================")

# Opción 1 del menú: el usuario indica la ruta del .csv que quiere usar
def cargarArchivos():
    global archivoCargado
    # Si el usuario arrastra el archivo a la consola la ruta puede venir entre comillas
    ruta = input("Ingrese la ruta del archivo .csv (Enter para cancelar): ").strip().strip('"').strip("'")
    if not ruta:
        print("No se cargó ningún archivo.")
        return

    # Se valida el archivo en el momento para avisar de los errores enseguida
    try:
        procesos = leer_archivo(ruta)
    except (OSError, ValueError) as error:
        print(f"No se pudo cargar el archivo: {error}")
        return

    if not procesos:
        print("El archivo no tiene procesos.")
        return

    archivoCargado = ruta
    print(f"Archivo cargado correctamente ({len(procesos)} procesos).")

# Opción 3 del menú
def mostrarInformacion():
    print("=================================================")
    print("INFORMACIÓN SOBRE EL SIMULADOR")
    print("=================================================")
    print("Memoria: 100K para el SO y 450K para procesos (particiones variables, Best-Fit).")
    print("CPU: planificación SRTF (expropiativo).")
    print(f"Cupo: entre Ejecución, Listos y Listos/Suspendidos como máximo {maximaCantidadProcesos} procesos.")
    print("Archivo .csv: columnas ID, TA (arribo), TI (irrupción) y TAM (tamaño en K),")
    print("              máximo 10 procesos y ninguno de más de 450K.")
    print("La simulación se detiene en cada evento (arribo o fin de proceso): Enter para seguir.")

# Hay cupo si Ejecución + Listos + Listos/Suspendidos no llega al máximo
def hayCupo(procesoCPU):
    ocupados = len(listos) + len(listosSupendidos)
    if procesoCPU is not None:
        ocupados += 1
    return ocupados < maximaCantidadProcesos

# Arma el texto de una cola con el tiempo restante de cada proceso
def formatoCola(cola):
    if not cola:
        return "vacía"
    return ", ".join(f"{proceso.id} (resta {proceso.restante})" for proceso in cola)

# Salida que se muestra en cada arribo / terminación
def mostrarSalida(reloj, eventos, procesoCPU, memoria, nuevos):
    print("=================================================")
    print(f"TIEMPO: {reloj}")
    for evento in eventos:
        print(f" - {evento}")
    print("-------------------------------------------------")

    # Estado del procesador
    if procesoCPU is None:
        print("Procesador: CPU ociosa")
    else:
        print(f"Procesador: ejecutando {procesoCPU.id} (le quedan {procesoCPU.restante} unidades)")

    # Tabla de particiones
    print("Tabla de particiones:")
    print(f"{'Id':<5}{'Inicio':<9}{'Tamaño':<9}{'Proceso':<10}{'Frag. interna'}")
    for particion in memoria:
        proceso = particion.proceso if particion.proceso is not None else "Libre"
        # En MVT cada partición se crea del tamaño justo del proceso: no hay fragmentación interna
        frag = "0K" if particion.proceso is not None else "-"
        print(f"{particion.id:<5}{str(particion.inicio) + 'K':<9}{str(particion.tamano) + 'K':<9}{proceso:<10}{frag}")
    print("-------------------------------------------------")

    # Las colas
    print("Cola de Listos:", formatoCola(listos))
    print("Cola de Listos/Suspendidos:", formatoCola(listosSupendidos))
    print("Nuevos esperando cupo:", formatoCola(nuevos))

# Informe estadístico cuando terminan todos los procesos
def mostrarInforme(procesos, reloj):
    print("=================================================")
    print("INFORME FINAL")
    print("=================================================")
    print(f"{'Proceso':<10}{'Arribo':<9}{'Irrupción':<11}{'Fin':<6}{'Retorno':<9}{'Espera'}")
    totalRetorno = 0
    totalEspera = 0
    for proceso in procesos:
        retorno = proceso.fin - proceso.arribo
        espera = retorno - proceso.irrupcion
        totalRetorno += retorno
        totalEspera += espera
        print(f"{proceso.id:<10}{proceso.arribo:<9}{proceso.irrupcion:<11}{proceso.fin:<6}{retorno:<9}{espera}")
    cantidad = len(procesos)
    print("-------------------------------------------------")
    print(f"Tiempo de retorno promedio: {totalRetorno / cantidad:.2f}")
    print(f"Tiempo de espera promedio: {totalEspera / cantidad:.2f}")
    print(f"Rendimiento del sistema: {cantidad / reloj:.3f} procesos terminados por unidad de tiempo")
    print(f"({cantidad} procesos terminados en {reloj} unidades de tiempo)")
    print("=================================================")

# Bucle principal del simulador
def simulador():
    # Recibe los procesos después de que se váliden
    # (si no se cargó ningún archivo, leer_archivo usa el de la carpeta test)
    if archivoCargado is None:
        print(f"No se cargó ningún archivo: se usa el lote de prueba {ARCHIVO_POR_DEFECTO.name}")
    try:
        procesosSim = leer_archivo(archivoCargado)
    except (OSError, ValueError) as error:
        print(f"No se pudo cargar el archivo: {error}")
        return
    if not procesosSim:
        print("No se pudo cargar el archivo")
        return

    # Las colas son globales: se vacían para que cada simulación empiece de cero
    listosSupendidos.clear()
    listos.clear()
    suspendidos.clear()

    # Función que calcula el próximo evento
    def proximoEvento():
        tiempos = []
        # Próximo arribo (si todavía quedan procesos por llegar)
        if porLlegar:
            tiempos.append(porLlegar[0].arribo)
        # Fin del proceso que está en la CPU (si la CPU está ociosa no hay fin)
        if procesoCPU is not None:
            tiempos.append(reloj + procesoCPU.restante)
        if not tiempos:
            return None
        return min(tiempos)

    # Si todo salio bien se inicializa en el tiempo cero
    reloj = 0

    # Los procesos se ordenan por tiempo de arribo
    procesosSim.sort(key=lambda proceso: proceso.arribo)
    porLlegar = list(procesosSim)   # todavía no arribaron
    nuevos = []                     # arribaron pero esperan cupo
    terminados = []
    procesoCPU = None               # CPU libre
    memoria = crearMemoria()        # SO 100K + un hueco libre de 450K

    # Mientras queden procesos sin terminar
    while len(terminados) < len(procesosSim):
        tEv = proximoEvento()
        if tEv is None:
            print("Error: no hay próximos eventos, se interrumpe la simulación.")
            break

        # Se avanza el reloj y se descuenta el tiempo ejecutado al proceso en CPU
        terminoProceso = False
        if procesoCPU is not None:
            for _ in range(tEv - reloj):
                terminoProceso = ejecutar_unidad(procesoCPU)
        reloj = tEv
        eventos = []

        # ¿Terminó el proceso en CPU? Se libera su partición (y un cupo) y se unen los huecos
        if terminoProceso:
            procesoCPU.estado = "Terminado"
            procesoCPU.fin = reloj
            liberarParticion(memoria, procesoCPU)
            unirParticionesMemoria(memoria)
            terminados.append(procesoCPU)
            eventos.append(f"Terminó el proceso {procesoCPU.id}: se liberó su partición")
            procesoCPU = None

        # Arribos: los procesos con arribo <= reloj pasan al estado Nuevo
        while porLlegar and porLlegar[0].arribo <= reloj:
            proceso = porLlegar.pop(0)
            proceso.estado = "Nuevo"
            nuevos.append(proceso)
            eventos.append(f"Arribó el proceso {proceso.id} ({proceso.tamano}K)")

        # ¿Hay un Listo/Suspendido que entre en memoria? (Best-Fit)
        entro = True
        while entro:
            entro = False
            for proceso in listosSupendidos:
                if bestFit(memoria, proceso):
                    listosSupendidos.remove(proceso)
                    proceso.estado = "Listo"
                    listos.append(proceso)
                    eventos.append(f"El proceso {proceso.id} pasó de Listo/Suspendido a Listo")
                    entro = True
                    break

        # ¿Hay procesos Nuevos y además hay cupo? Se toma el Nuevo de menor arribo
        while nuevos and hayCupo(procesoCPU):
            proceso = nuevos.pop(0)
            if bestFit(memoria, proceso):
                proceso.estado = "Listo"
                listos.append(proceso)
                eventos.append(f"El proceso {proceso.id} pasó a Listo (se le asignó partición)")
            else:
                proceso.estado = "Listo/Suspendido"
                listosSupendidos.append(proceso)
                eventos.append(f"El proceso {proceso.id} pasó a Listo/Suspendido (no hay hueco donde entre)")

        # SRTF (expropiativo) entre los Listos y el que está en la CPU
        # (el de la CPU va primero para que en un empate siga ejecutándose)
        if procesoCPU is None:
            candidatos = list(listos)
        else:
            candidatos = [procesoCPU] + listos
        elegido = seleccionar_proceso(candidatos)
        if elegido is not None and elegido is not procesoCPU:
            if procesoCPU is not None:
                procesoCPU.estado = "Listo"
                listos.append(procesoCPU)
                eventos.append(f"SRTF: el proceso {elegido.id} desalojó al proceso {procesoCPU.id}")
            listos.remove(elegido)
            elegido.estado = "Ejecución"
            procesoCPU = elegido
            eventos.append(f"El proceso {elegido.id} pasó a Ejecución")

        # Salida por cada arribo / terminación y pausa (no hay corridas ininterrumpidas)
        mostrarSalida(reloj, eventos, procesoCPU, memoria, nuevos)
        input("Presione Enter para continuar...")

    # Si terminaron todos los procesos se muestra el informe final
    if len(terminados) == len(procesosSim):
        mostrarInforme(procesosSim, reloj)

# Bucle del menú
def main():
    while True:
        mostrarMenu()
        try:
            opcion = int(input("Seleccione una opción del menú ingresando el número correspondiente: "))
        except ValueError:
            opcion = 0
        if opcion not in opcionesMenu:
            print("Esa opción no es váldia! Ingrese una opción válida.")
            continue
        elif opcion == 1:
            cargarArchivos()
        elif opcion == 2:
            simulador()
        elif opcion == 3:
            mostrarInformacion()
        elif opcion == 4:
            break

# Punto de entrada: python simulador.py
if __name__ == "__main__":
    main()
