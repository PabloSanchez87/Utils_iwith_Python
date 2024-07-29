import tkinter as tk
from tkinter import messagebox
import string
import secrets

# Función para generar una contraseña basada en los parámetros seleccionados
def generate_password():
    try:
        # Verificar si el campo de longitud está vacío
        length_str = length_entry.get()
        if not length_str:
            raise ValueError("Debe ingresar una longitud para generar la contraseña.")
        
        # Convertir la longitud a entero
        length = int(length_str)
        
        # Obtener el estado de los checkboxes para determinar qué tipos de caracteres incluir
        use_letters = letters_var.get()
        use_digits = digits_var.get()
        use_punctuation = punctuation_var.get()
        
        # Verificar si la longitud es válida
        if length <= 0:
            raise ValueError("La longitud debe ser mayor que 0.")
        
        # Crear el conjunto de caracteres posibles basados en las selecciones del usuario
        character_pool = ''
        if use_letters:
            character_pool += string.ascii_letters
        if use_digits:
            character_pool += string.digits
        if use_punctuation:
            character_pool += string.punctuation
        
        # Asegurar que al menos un tipo de carácter ha sido seleccionado
        if not character_pool:
            raise ValueError("Se debe seleccionar al menos un tipo de carácter.")
        
        # Generar la contraseña utilizando una selección segura de caracteres
        password = ''.join(secrets.choice(character_pool) for _ in range(length))
        # Mostrar la contraseña generada en la etiqueta
        result_label.config(text="Contraseña generada")
        password_label.config(text=password)
        result_label.grid(row=5, column=0, columnspan=2, pady=5)  # Mostrar la etiqueta de texto
        password_label.grid(row=6, column=0, columnspan=2, pady=5)  # Mostrar la etiqueta de contraseña
        # Habilitar el botón de copiar al portapapeles
        copy_button.config(state=tk.NORMAL)
    except ValueError as e:
        # Mostrar un mensaje de error si ocurre una excepción
        messagebox.showerror("Error", str(e))

# Función para copiar la contraseña generada al portapapeles
def copy_to_clipboard():
    # Obtener la contraseña desde la etiqueta de resultados
    password = password_label.cget("text")
    # Limpiar cualquier contenido previo del portapapeles
    root.clipboard_clear()
    # Añadir la contraseña al portapapeles
    root.clipboard_append(password)
    # Mostrar un mensaje informando que la contraseña ha sido copiada
    messagebox.showinfo("Copiado", "La contraseña ha sido copiada al portapapeles.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Generador de Contraseñas")

# Widgets para la longitud de la contraseña
tk.Label(root, text="Longitud de la contraseña:").grid(row=0, column=0, padx=10, pady=10)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=10)

# Widgets para seleccionar tipos de caracteres
letters_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Incluir letras", variable=letters_var).grid(row=1, column=0, padx=10, pady=5, sticky="w")

digits_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Incluir dígitos", variable=digits_var).grid(row=2, column=0, padx=10, pady=5, sticky="w")

punctuation_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Incluir puntuación", variable=punctuation_var).grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Botón para generar la contraseña
generate_button = tk.Button(root, text="Generar contraseña", command=generate_password)
generate_button.grid(row=4, column=0, columnspan=2, pady=20)

# Etiqueta para mostrar el texto de la contraseña generada
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.grid(row=5, column=0, columnspan=2, pady=5)

# Etiqueta para mostrar la contraseña generada
password_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"))
password_label.grid(row=6, column=0, columnspan=2, pady=5)

# Botón para copiar la contraseña al portapapeles
copy_button = tk.Button(root, text="Copiar al portapapeles", state=tk.DISABLED, command=copy_to_clipboard)
copy_button.grid(row=7, column=0, columnspan=2, pady=20)

# Ejecutar la ventana principal de la aplicación
root.mainloop()
