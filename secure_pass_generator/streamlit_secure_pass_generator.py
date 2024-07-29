import os
import streamlit as st
import string
import secrets

# Función para generar una contraseña basada en los parámetros seleccionados
def generate_password(length, use_letters, use_digits, use_punctuation):
    character_pool = ''
    if use_letters:
        character_pool += string.ascii_letters
    if use_digits:
        character_pool += string.digits
    if use_punctuation:     # string.punctuation si los quisieramos todos.
        character_pool += "!@#%&*()-_=+.,:;[]"
    
    if not character_pool:
        st.error("Se debe seleccionar al menos un tipo de carácter.")
        return None
    
    password = ''.join(secrets.choice(character_pool) for _ in range(length))
    return password

# Validar la longitud
def is_valid_length(length_str):
    try:
        length = int(length_str)
        return length > 0
    except ValueError:
        return False

# Obtener el directorio base del proyecto (un nivel arriba del directorio actual)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Construir la ruta a los archivos
favicon_path = os.path.join(base_dir, "resources", "Favicon", "favicon.ico")
logo_path = os.path.join(base_dir, "resources", "logohorizontal.png")

# Configuración de la página de Streamlit
st.set_page_config(page_title="Secure Pass Generator", page_icon=favicon_path, layout="centered")

# Verificar si el archivo de logo existe y luego usarlo
if not os.path.exists(logo_path):
    st.error(f"No se encontró el archivo de imagen en: {logo_path}")
else:
    st.image(logo_path, use_column_width=True)

# Configuración de la aplicación
st.title("Generador de Contraseñas")

# Crear un formulario para las entradas y el botón
with st.form(key='password_form'):
    # Variables de entrada
    length_input = st.text_input("Longitud de la contraseña")
    use_letters = st.checkbox("Incluir letras", value=True)
    use_digits = st.checkbox("Incluir dígitos", value=True)
    use_punctuation = st.checkbox("Incluir puntuación", value=True)
    
    # Validar la longitud en tiempo real
    valid_length = is_valid_length(length_input)
    
    # Botón para generar contraseña, habilitado solo si la longitud es válida
    submit_button = st.form_submit_button("Generar contraseña")

    if submit_button or valid_length:
        if valid_length:
            password = generate_password(int(length_input), use_letters, use_digits, use_punctuation)
            if password:
                # Mostrar la contraseña generada en el área de código (textarea)
                st.subheader("Contraseña generada")
                st.code(password)
        else:
            st.error("Debe ingresar una longitud válida para generar la contraseña.")


# Añadir enlaces a LinkedIn y GitHub con logos como botones
st.markdown(
    """
    <div style="display: flex; justify-content: center; gap: 20px;">
        <a href="https://github.com/PabloSanchez87" target="_blank" style="text-decoration: none;">
            <button style="background-color:transparent; border: none; cursor: pointer;">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="40" height="40" alt="GitHub Logo"/>
            </button>
        </a>
        <a href="https://www.linkedin.com/in/pablosancheztorres/" target="_blank" style="text-decoration: none;">
            <button style="background-color:transparent; border: none; cursor: pointer;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="40" height="40" alt="LinkedIn Logo"/>
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

