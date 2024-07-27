
# Renombrador masivo de Archivos

## Descripción General

- Este script permite a los usuarios crear un número específico de archivos de texto con nombres generados aleatoriamente en un directorio elegido si es necesario. 
- También proporciona una opción para renombrar estos archivos con un prefijo definido por el usuario y cambiar sus extensiones.

## Características

1. **Creación de Archivos Aleatorios**(para pruebas): 
   - Genera un número definido por el usuario de archivos de texto con nombres aleatorios.
   - Cada archivo contiene una línea de texto que indica que es un archivo generado aleatoriamente.

2. **Renombrado de Archivos**: 
   - Renombra los archivos generados usando un prefijo especificado.
   - Opción para cambiar la extensión de archivo para todos los archivos.

## Uso

### Requisitos

- Python 3.x
- Biblioteca `tkinter` 
  
### Cómo Ejecutar

1. Clona el repositorio o descarga el archivo del script.
2. Ejecuta el script utilizando un intérprete de Python.
   
   ```bash
   python nombre_del_script.py
   ```

3. Aparecerá un cuadro de diálogo para seleccionar el directorio de trabajo.
4. Elige si deseas crear archivos aleatorios y, de ser así, especifica el número de archivos.
5. Ingresa un prefijo para renombrar los archivos.
6. Elige si deseas cambiar la extensión de los archivos y, de ser así, proporciona la nueva extensión.
7. El script mostrará la lista de archivos a renombrar y pedirá confirmación antes de proceder.

## Descripción del Código

### `create_random_files(directory_path, number_of_files)`

Crea un número específico de archivos de texto con nombres aleatorios en el directorio proporcionado.

- `directory_path`: La ruta del directorio donde se crearán los archivos.
- `number_of_files`: El número de archivos a generar.

### `change_names(directory_path, prefix)`

Renombra los archivos en el directorio especificado utilizando un prefijo proporcionado por el usuario.

- `directory_path`: La ruta del directorio que contiene los archivos a renombrar.
- `prefix`: El prefijo que se usará para los nuevos nombres de archivo.

## Ejemplo

1. Selecciona el directorio: `/ruta/al/directorio`
2. Crear 5 archivos aleatorios.
3. Prefijo para renombrar: `archivo_prueba`
4. Nueva extensión (si aplica): `.log`

