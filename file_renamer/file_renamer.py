import os           # Módulo para interactuar con el sistema de archivos
import random       # Módulo para generar números y secuencias aleatorias
import string       # Módulo para operaciones con cadenas de caracteres
from tkinter import Tk  # Módulo para interfaces gráficas
from tkinter.filedialog import askdirectory # Función para abrir un cuadro de diálogo de selección de directorios


def create_random_files(directory_path, number_of_files):
    """
    Crea un número específico de archivos de texto con nombres aleatorios en el directorio proporcionado.

    Parámetros:
    - directory_path (str): La ruta del directorio donde se crearán los archivos.
    - number_of_files (int): El número de archivos a crear.

    Detalles:
    - Si el directorio no existe, se creará automáticamente.
    - Cada archivo contendrá una línea de texto indicando que es un archivo generado aleatoriamente.
    - Los nombres de los archivos consisten en una combinación aleatoria de 8 caracteres alfanuméricos.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path) # Crea el directorio si no existe        
    
    print(f"Creating {number_of_files} files in '{directory_path}'...")
    for _ in range(number_of_files):
        # Genera un nombre de archivo aleatorio de 8 caracteres alfanuméricos
        random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.txt'
        file_path = os.path.join(directory_path, random_filename) # Construye la ruta completa del archivo
        with open(file_path, 'w') as f:
            f.write("This is a randomly generated file. \n") # Escribe una línea de texto en el archivo
        print(f"Created file: {random_filename}")   # Imprime el nombre del archivo creado


def change_names(directory_path, prefix):
    """
    Renombra los archivos en el directorio especificado utilizando un prefijo proporcionado por el usuario.

    Parámetros:
    - directory_path (str): La ruta del directorio que contiene los archivos a renombrar.
    - prefix (str): El prefijo que se agregará a cada archivo renombrado.

    Detalles:
    - Verifica que el directorio sea válido y que contenga archivos.
    - Muestra una lista de archivos que serán renombrados y solicita confirmación del usuario antes de proceder.
    - Permite al usuario elegir mantener o cambiar la extensión de los archivos.
    - Cada archivo es renombrado añadiendo un número secuencial al prefijo proporcionado.
    - Maneja errores comunes como la ausencia de archivos o problemas de permisos.
    """
    if not os.path.isdir(directory_path): # Verifica si la ruta es un directorio válido
        print(f"Error: '{directory_path}' is not a valid directory.")
        return

    if not prefix:  # Verifica si el prefijo es una cadena no vacía
        print("Error: Prefix cannot be empty.")
        return

    try:            # Intenta listar los archivos en el directorio
        files = os.listdir(directory_path)
    except FileNotFoundError:
        print(f"Error: Directory '{directory_path}' not found.") # Error si el directorio no se encuentra
        return
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory_path}'.") # Error si no hay permisos de acceso
        return

    if not files:
        print(f"No files found in '{directory_path}'.") # Mensaje si no se encuentran archivos en el directorio
        return

    # List the files to be renamed
    # Muestra los archivos que se renombrarán
    print("Files to be renamed:")
    for file_name in files:
        print(file_name)

    # Ask if the user wants to change the file extension
    # Pregunta si el usuario quiere cambiar la extensión de los archivos
    while True:
        change_extension = input("Do you want to change the file extension of all files? (yes/no): ").strip().lower() 
        new_extension = ""                                                                      # elimanos espacios en blanco
        if change_extension == 'yes':
                # Pide una nueva extensión y la valida
                new_extension = input("Enter the new file extension (include the dot, .pdf, .txt): ").strip()
                if new_extension.startswith('.') and len(new_extension) > 1:
                    break  # Exit the loop if the extension is valid | # Sale del bucle si la extensión es válida
                else:
                    print("Invalid extension format. Please enter a valid file extension starting with a dot (.pdf., .txt).")

    # Ask for confirmation
    # Pide confirmación al usuario para proceder con el renombramiento
    confirm = input("Do you want to proceed with renaming these files? (yes/no): ").strip().lower() # elimanos espacios en blanco
    if confirm != 'yes':
        print("Renaming cancelled.") # Cancela el renombramiento si el usuario no confirma
        return

    print(f"Renaming files in '{directory_path}' with prefix '{prefix}'...")
    for counter, file_name in enumerate(files, start=1):
        name, extension = os.path.splitext(file_name) # Separa el nombre y la extensión del archivo
        if change_extension == 'yes':
            extension = new_extension # Cambia la extensión si el usuario lo ha solicitado
        
        new_name = f'{prefix}_{counter}{extension}' # Crea el nuevo nombre del archivo

        # Asegura que el nombre del archivo sea único
        while os.path.exists(os.path.join(directory_path, new_name)):
            counter += 1
            new_name = f'{prefix}_{counter}{extension}'

        try: # Intenta renombrar el archivo
            os.rename(os.path.join(directory_path, file_name), os.path.join(directory_path, new_name))
            print(f'Renamed: {file_name} -> {new_name}')    # Muestra el cambio de nombre
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")   # Error si el archivo no se encuentra
        except PermissionError:
            print(f"Error: Permission denied for renaming '{file_name}'.")  # Error si no hay permisos de renombramiento
        except Exception as e:
            print(f"An error occurred: {e}")     # Maneja cualquier otro error


# Main #

if __name__ == "__main__":
    # Initialize Tkinter and hide the root window
    # Inicializa Tkinter y oculta la ventana principal
    root = Tk()
    root.withdraw()

    # Open a file dialog to select the directory
    # Abre un cuadro de diálogo para seleccionar un directorio
    directory_path = askdirectory(title="Select Directory to Create Files")

    if directory_path:
        # Ask the user if they want to create random files
        # Pregunta al usuario si desea crear archivos aleatorios en el directorio seleccionado
        create_files = input("Do you want to create random files in the selected directory? (yes/no): ").strip().lower()

        if create_files == 'yes':
            number_of_files = 0
            while number_of_files <= 0:
                try:   
                    # Solicita el número de archivos a crear
                    number_of_files = int(input("Enter the number of files to create: "))
                    if number_of_files <= 0:     # Verifica que el número sea mayor que cero
                        print("The number of files must be greater than 0.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")    # Maneja la entrada no válida
                    
            # Create random files
            # Crea archivos aleatorios
            create_random_files(directory_path, number_of_files)
        else:
            print("Skipping file creation.") # Omite la creación de archivos si el usuario no lo desea

        # Get the prefix for renaming files
        # Solicita un prefijo para renombrar los archivos
        prefix = input("Enter the prefix for renaming files: ")

        # Rename the files
        # Renombra los archivos
        change_names(directory_path, prefix)
    else:
        print("No directory selected.")
        # Mensaje si no se selecciona un directorio


