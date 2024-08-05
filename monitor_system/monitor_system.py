import psutil
import time
import logging
import platform

def get_size(bytes, suffix="B"):
    """
    Escala bytes a su tamaño apropiado en KB, MB, GB, etc.
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

def validate_thresholds(thresholds):
    """
    Valida que el diccionario de umbrales contenga todas las claves necesarias y que los valores sean válidos.
    
    Parámetros:
    thresholds (dict): Diccionario que contiene los valores umbral para 'cpu', 'memory', 'disk', 'swap', 'processes' y 'temp'.
    
    Lanza:
    ValueError: Si falta alguna clave requerida o si algún valor no es un número positivo.
    """
    required_keys = ['cpu', 'memory', 'disk', 'swap', 'processes', 'temp']
    for key in required_keys:
        if key not in thresholds:
            raise ValueError(f"Falta el umbral requerido: {key}")
        if not isinstance(thresholds[key], (int, float)) or thresholds[key] <= 0:
            raise ValueError(f"El umbral para {key} debe ser un número positivo.")

def log_system_info():
    """
    Muestra la información básica del sistema.
    """
    uname = platform.uname()
    print("·"*80)
    print("··· Sistema ···")
    logging.info(f"Sistema: {uname.system}")
    logging.info(f"Nodo de red: {uname.node}")
    logging.info(f"Versión del sistema: {uname.release}")
    logging.info(f"Versión: {uname.version}")
    logging.info(f"Máquina: {uname.machine}")
    logging.info(f"Procesador: {uname.processor}")
    
    # Información de la CPU
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    logging.info(f"Núcleos físicos de la CPU: {cpu_cores}")
    logging.info(f"Hilos de la CPU: {cpu_threads}")
    
    # Información de la memoria
    svmem = psutil.virtual_memory()
    logging.info(f"Memoria total: {get_size(svmem.total)}")
    
    # Información del disco
    disk = psutil.disk_usage('/')
    logging.info(f"Espacio total del disco: {get_size(disk.total)}")
    print("·"*80)
    
def monitor_system(thresholds):
    """
    Monitorea los recursos del sistema (CPU, memoria, disco, red, temperatura, swap, procesos y uptime)
    y muestra advertencias si el uso supera los umbrales definidos.

    Parámetros:
    thresholds (dict): Diccionario que contiene los valores umbral para 'cpu', 'memory', 'disk', 'swap', 'processes' y 'temp'.
    """
    # Validar umbrales
    validate_thresholds(thresholds)
    
    # Configuración básica del registro
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Mostrar información del sistema
    log_system_info()
    
    # Bucle infinito para monitorear los recursos del sistema
    while True:
        
        # Obtener el porcentaje de uso de la CPU
        cpu = psutil.cpu_percent(interval=1)
        # Obtener el porcentaje de uso de la memoria
        memory = psutil.virtual_memory().percent
        # Obtener el porcentaje de uso del disco
        disk = psutil.disk_usage('/').percent
        # Obtener los contadores de E/S de red
        net = psutil.net_io_counters()
        # Obtener el porcentaje de uso de la memoria swap
        swap = psutil.swap_memory().percent
        # Obtener el número total de procesos en ejecución
        processes = len(psutil.pids())
        # Calcular el tiempo de actividad del sistema
        uptime = time.time() - psutil.boot_time()
        # Inicializar la temperatura del CPU
        temp = None
        
        # Intentar obtener la temperatura del CPU (puede no ser soportado en todas las plataformas)
        try:
            temp = psutil.sensors_temperatures()['coretemp'][0].current
        except (KeyError, AttributeError):
            temp = "N/A"
        
        # Registrar la información del uso actual de los recursos
        print("··· Uso actual ···")
        logging.info(f'Uso actual de CPU: {cpu}%')
        logging.info(f'Uso actual de la memoria: {memory}%')
        logging.info(f'Uso actual del disco: {disk}%')
        logging.info(f'Tráfico de red: Enviados {get_size(net.bytes_sent)}, Recibidos {get_size(net.bytes_recv)}')
        logging.info(f'Uso de la swap: {swap}%')
        logging.info(f'Número de procesos: {processes}')
        logging.info(f'Tiempo de actividad del sistema: {uptime:.2f} segundos')
        if temp != "N/A":
            logging.info(f'· Temperatura del CPU: {temp}°C')
        
        # Verificar si el uso de la CPU supera el umbral definido
        if cpu > thresholds['cpu']:
            logging.warning(f'Uso de CPU al {cpu}%')
        
        # Verificar si el uso de la memoria supera el umbral definido
        if memory > thresholds['memory']:
            logging.warning(f'Uso de memoria al {memory}%')
           
        # Verificar si el uso del disco supera el umbral definido
        if disk > thresholds['disk']:
            logging.warning(f'Uso de disco al {disk}%')
        
        # Verificar si el uso de la swap supera el umbral definido
        if swap > thresholds['swap']:
            logging.warning(f'Uso de swap al {swap}%')
        
        # Verificar si el número de procesos supera el umbral definido
        if processes > thresholds['processes']:
            logging.warning(f'Número de procesos alto: {processes}')
        
        # Verificar si la temperatura del CPU supera el umbral definido
        if temp != "N/A" and temp > thresholds['temp']:
            logging.warning(f'Temperatura del CPU alta: {temp}°C')
        
        print("·"*80)
        
        # Esperar 10 segundos antes de la siguiente verificación
        time.sleep(10)

if __name__ == "__main__":
    # Datos del sistema con los umbrales definidos
    systemData = {
        'cpu': 10,  # Umbral de uso de la CPU
        'memory': 80,  # Umbral de uso de la memoria
        'disk': 90,  # Umbral de uso del disco
        'swap': 20,  # Umbral de uso de la memoria swap
        'processes': 200,  # Umbral del número de procesos
        'temp': 70  # Umbral de temperatura en grados Celsius
    }

    # Ejecutar la función de monitoreo del sistema con los datos del sistema
    try:
        monitor_system(systemData)
    except Exception as e:
        logging.error(f"Ocurrió un error durante la ejecución: {e}")