# Monitor de Recursos del Sistema

Este proyecto es un script en Python que monitorea los recursos del sistema (CPU, memoria y disco) y muestra advertencias si el uso de estos recursos supera los umbrales definidos.

## Descripción

El script utiliza la biblioteca `psutil` para obtener información sobre el uso de la CPU, la memoria y el disco. Utiliza `logging` para registrar y mostrar la información y las advertencias cuando el uso de los recursos supera los umbrales especificados.

## Funcionalidades

- Monitoreo continuo del uso de la CPU, memoria y disco.
- Registro y visualización del uso actual de los recursos.
- Advertencias cuando el uso de los recursos supera los umbrales definidos.

## Requisitos

- Python 3.x
- Biblioteca `psutil`
- Biblioteca `platform`

Puedes instalar la biblioteca `psutil` utilizando pip:

```bash
pip install psutil
```

## Uso
1. Clona el repositorio o descarga el archivo monitor.py.
2. Define los umbrales para los recursos del sistema en el diccionario systemData.
3. Ejecuta el script.
    ```bash
    python monitor_system.py
    ```


### Parámetros de Configuración
Puedes configurar los umbrales de alerta dentro del script en la sección systemData. Los umbrales son personalizables para CPU, memoria, disco, swap, número de procesos y temperatura del CPU.

 - `cpu`: Umbral de uso de la CPU (porcentaje).
 - `memory`: Umbral de uso de la memoria (porcentaje).
 - `disk`: Umbral de uso del disco (porcentaje).
 - `red`: Indica el uso de la red.
 - `swap`: Umbral de uso de la memoria swap
 - `processes`: Umbral del número de procesos
 - `temp`: Umbral de temperatura en grados Celsius

### Registro de Eventos
Los eventos y las alertas se registrarán en el formato de logging de Python, mostrando la hora y el tipo de alerta generada.

### Salida esperada
El script registrará y mostrará información como la siguiente:
```yaml
··· Sistema ···
2024-08-05 21:11:51,562 - INFO - Sistema: Linux
2024-08-05 21:11:51,563 - INFO - Nodo de red: PS
2024-08-05 21:11:51,563 - INFO - Versión del sistema: 5.15.153.1-microsoft-standard-WSL2
2024-08-05 21:11:51,563 - INFO - Versión: #1 SMP Fri Mar 29 23:14:13 UTC 2024
2024-08-05 21:11:51,563 - INFO - Máquina: x86_64
2024-08-05 21:11:51,563 - INFO - Procesador: x86_64
2024-08-05 21:11:51,564 - INFO - Núcleos físicos de la CPU: 10
2024-08-05 21:11:51,564 - INFO - Hilos de la CPU: 20
2024-08-05 21:11:51,564 - INFO - Memoria total: 15.53 GB
2024-08-05 21:11:51,564 - INFO - Espacio total del disco: 1006.85 GB

················································································

··· Uso actual ···
2024-08-05 21:11:52,565 - INFO - Uso actual de CPU: 0.2%
2024-08-05 21:11:52,565 - INFO - Uso actual de la memoria: 13.9%
2024-08-05 21:11:52,565 - INFO - Uso actual del disco: 2.3%
2024-08-05 21:11:52,565 - INFO - Tráfico de red: Enviados 65.51 MB, Recibidos 73.70 MB
2024-08-05 21:11:52,565 - INFO - Uso de la swap: 0.0%
2024-08-05 21:11:52,565 - INFO - Número de procesos: 79
2024-08-05 21:11:52,565 - INFO - Tiempo de actividad del sistema: 6800.57 segundos
2024-08-05 21:11:52,565 - WARNING - Uso de memoria al 13.9%
```

## Contribuciones
Las contribuciones son bienvenidas. Si deseas mejorar el script o añadir nuevas funcionalidades, por favor, abre un issue o envía un pull request.