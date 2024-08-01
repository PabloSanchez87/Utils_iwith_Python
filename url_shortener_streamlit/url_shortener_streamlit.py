import pyshorteners
import requests
import streamlit as st
import qrcode
from io import BytesIO
import validators
import os
import time

# Obtener el directorio base del proyecto (un nivel arriba del directorio actual)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Construir la ruta a los archivos
favicon_path = os.path.join(base_dir, "resources", "Favicon", "favicon.ico")
logo_path = os.path.join(base_dir, "resources", "logohorizontal.png")

# Función para acortar URLs utilizando el servicio TinyURL
def url_shortener(url):
    """
    Acorta una URL utilizando el servicio TinyURL a través de la biblioteca pyshorteners.
    
    Parámetros:
    url (str): La URL que se desea acortar.
    
    Retorna:
    str: La URL acortada.
    """
    shortener = pyshorteners.Shortener()  # Crear una instancia del acortador
    shorted_url = shortener.tinyurl.short(url)  # Acortar la URL usando TinyURL
    return shorted_url

# Función para generar un código QR a partir de una URL
def generate_qr(url):
    """
    Genera un código QR para una URL y lo devuelve como una imagen en bytes.
    
    Parámetros:
    url (str): La URL para la cual se generará el código QR.
    
    Retorna:
    BytesIO: La imagen del código QR en formato de bytes.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Guardar la imagen en un objeto BytesIO para mostrar en Streamlit
    # Utilizar un objeto BytesIO para almacenar la imagen en memoria es una manera eficiente de manejar imágenes sin necesidad de guardarlas en el sistema de archivos.
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def validate_url(url):
    """
    Verifica si la URL es válida y accesible.
    
    Parámetros:
    url (str): La URL que se desea validar.
    
    Retorna:
    bool: True si la URL es válida y accesible, False en caso contrario.
    """
    if not url:
        return False, "The URL field is empty."
    if not validators.url(url):
        return False, "The URL provided is not valid."
    
    for _ in range(3):  # Intentar 3 veces
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code == 503:
                time.sleep(2)  # Esperar 2 segundos antes de reintentar
                continue
            elif response.status_code >= 400:
                return False, f"The URL returned an error: {response.status_code}"
            return True, "The URL is valid."
        except requests.RequestException as e:
            return False, f"An error occurred: {e}"
    
    return False, "The server is temporarily unavailable after multiple attempts (503). Please try again later."
    


# Configuración de la página de la aplicación con Streamlit
st.set_page_config(
    page_title="URL Shortener",  # Título de la página
    page_icon=favicon_path,  # Favicon de la página
    layout="centered"  # Diseño centrado de la aplicación
)

# Muestra el logo de la aplicación
st.image(
    logo_path,  # Ruta al archivo de imagen
    use_column_width=True  # Ajusta la imagen al ancho de la columna
)

# Título de la aplicación
st.title("URL Shortener")

# Campo de entrada de texto para la URL original
url = st.text_input("Enter the Original URL:")

# Botón para generar la nueva URL acortada y el código QR
if st.button("Generate new URL and QR"):
    is_valid, message = validate_url(url)
    if is_valid:
        shortened_url = url_shortener(url)
        st.write("Shortened URL: ", shortened_url)
        
        # Generar y mostrar el código QR
        qr_image = generate_qr(shortened_url)
        st.image(qr_image, caption="QR Code")
    else:
        st.warning(message)
