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

Puedes instalar la biblioteca `psutil` utilizando pip:

```bash
pip install psutil
```

## Uso
1. Clona el repositorio o descarga el archivo monitor.py.
2. Define los umbrales para los recursos del sistema en el diccionario systemData.
3. Ejecuta el script.


### Parámetros de Configuración

 - `cpu`: Umbral de uso de la CPU (porcentaje).
 - `memory`: Umbral de uso de la memoria (porcentaje).
 - `disk`: Umbral de uso del disco (porcentaje).

### Salida Esperada
El script registrará y mostrará información como la siguiente:
```yaml
2023-08-05 12:00:00 - INFO - · Uso actual de CPU: 15%
2023-08-05 12:00:00 - INFO - · Uso actual de la memoria: 45%
2023-08-05 12:00:00 - INFO - · Uso actual del disco: 60%
2023-08-05 12:00:00 - WARNING - Warning: Uso de CPU al 15%
2023-08-05 12:00:00 - WARNING - Warning: Uso de memoria al 45%
2023-08-05 12:00:00 - WARNING - Warning: Uso de disco al 60%
```


## Contribuciones
Las contribuciones son bienvenidas. Si deseas mejorar el script o añadir nuevas funcionalidades, por favor, abre un issue o envía un pull request.