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
    if use_punctuation:
        character_pool += string.punctuation
    
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
    

# Configuración de la página de Streamlit
st.set_page_config(page_title="Secure Pass Generator", page_icon="../resources/Favicon/favicon.ico", layout="centered")

# Muestra un logo en la página (la ruta debe ser ajustada según la ubicación real del archivo)
st.image("../resources/logohorizontal.png", use_column_width=True)

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
