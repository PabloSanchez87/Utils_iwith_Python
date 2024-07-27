import os
import random
import string
from tkinter import Tk
from tkinter.filedialog import askdirectory


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
        os.makedirs(directory_path)
    
    print(f"Creating {number_of_files} files in '{directory_path}'...")
    for _ in range(number_of_files):
        random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.txt'
        file_path = os.path.join(directory_path, random_filename)
        with open(file_path, 'w') as f:
            f.write("This is a randomly generated file.\n")
        print(f"Created file: {random_filename}")


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
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory.")
        return

    if not prefix:
        print("Error: Prefix cannot be empty.")
        return

    try:
        files = os.listdir(directory_path)
    except FileNotFoundError:
        print(f"Error: Directory '{directory_path}' not found.")
        return
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory_path}'.")
        return

    if not files:
        print(f"No files found in '{directory_path}'.")
        return

    # List the files to be renamed
    print("Files to be renamed:")
    for file_name in files:
        print(file_name)

    # Ask if the user wants to change the file extension
    while True:
        change_extension = input("Do you want to change the file extension of all files? (yes/no): ").strip().lower()
        new_extension = ""
        if change_extension == 'yes':
            
                new_extension = input("Enter the new file extension (include the dot, .pdf, .txt): ").strip()
                if new_extension.startswith('.') and len(new_extension) > 1:
                    break  # Exit the loop if the extension is valid
                else:
                    print("Invalid extension format. Please enter a valid file extension starting with a dot (.pdf., .txt).")

    # Ask for confirmation
    confirm = input("Do you want to proceed with renaming these files? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Renaming cancelled.")
        return

    print(f"Renaming files in '{directory_path}' with prefix '{prefix}'...")
    for counter, file_name in enumerate(files, start=1):
        name, extension = os.path.splitext(file_name)
        if change_extension == 'yes':
            extension = new_extension
        
        new_name = f'{prefix}_{counter}{extension}'

        while os.path.exists(os.path.join(directory_path, new_name)):
            counter += 1
            new_name = f'{prefix}_{counter}{extension}'

        try:
            os.rename(os.path.join(directory_path, file_name), os.path.join(directory_path, new_name))
            print(f'Renamed: {file_name} -> {new_name}')
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except PermissionError:
            print(f"Error: Permission denied for renaming '{file_name}'.")
        except Exception as e:
            print(f"An error occurred: {e}")


# Main #

if __name__ == "__main__":
    # Initialize Tkinter and hide the root window
    root = Tk()
    root.withdraw()

    # Open a file dialog to select the directory
    directory_path = askdirectory(title="Select Directory to Create Files")

    if directory_path:
        # Ask the user if they want to create random files
        create_files = input("Do you want to create random files in the selected directory? (yes/no): ").strip().lower()

        if create_files == 'yes':
            number_of_files = 0
            while number_of_files <= 0:
                try:
                    number_of_files = int(input("Enter the number of files to create: "))
                    if number_of_files <= 0:
                        print("The number of files must be greater than 0.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            # Create random files
            create_random_files(directory_path, number_of_files)
        else:
            print("Skipping file creation.")

        # Get the prefix for renaming files
        prefix = input("Enter the prefix for renaming files: ")

        # Rename the files
        change_names(directory_path, prefix)
    else:
        print("No directory selected.")


