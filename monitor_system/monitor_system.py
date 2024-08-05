import psutil
import time
import logging

def monitor_system(thresholds):
    """
    Monitorea los recursos del sistema (CPU, memoria, disco) y muestra advertencias si el uso supera los umbrales definidos.

    Parámetros:
    thresholds (dict): Diccionario que contiene los valores umbral para 'cpu', 'memory' y 'disk'.
    """
    # Configuración básica del registro
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Bucle infinito para monitorear los recursos del sistema
    while True:
        # Obtener el porcentaje de uso de la CPU
        cpu = psutil.cpu_percent(interval=1)
        # Obtener el porcentaje de uso de la memoria
        memory = psutil.virtual_memory().percent
        # Obtener el porcentaje de uso del disco
        disk = psutil.disk_usage('/').percent
        
        
        # Registrar la información del uso actual de los recursos
        logging.info(f'· Uso actual de CPU: {cpu}%')
        logging.info(f'· Uso actual de la memoria: {memory}%')
        logging.info(f'· Uso actual del disco: {disk}%')      
        
        # Verificar si el uso de la CPU supera el umbral definido
        if cpu > thresholds['cpu']:
            logging.warning(f'Warning: Uso de CPU al {cpu}%')
        
        # Verificar si el uso de la memoria supera el umbral definido
        if memory > thresholds['memory']:
            logging.warning(f'Warning: Uso de memoria al {memory}%')
           
        # Verificar si el uso del disco supera el umbral definido
        if disk > thresholds['disk']:
            logging.warning(f'Warning: Uso de disco al {disk}%') 
           
        # Esperar 10 segundos antes de la siguiente verificación
        time.sleep(10)

if __name__ == "__main__":
    # Datos del sistema con los umbrales definidos
    systemData = {
        'cpu': 10,  # Umbral de uso de la CPU
        'memory': 5,  # Umbral de uso de la memoria
        'disk': 5  # Umbral de uso del disco
    }

    # Ejecutar la función de monitoreo del sistema con los datos del sistema
    monitor_system(systemData)
