import pyshorteners
import streamlit as st

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

# Configuración de la página de la aplicación con Streamlit
st.set_page_config(
    page_title="URL Shortener",  # Título de la página
    page_icon="./resources/favicon.ico",  # Favicon de la página
    layout="centered"  # Diseño centrado de la aplicación
)

# Muestra el logo de la aplicación
st.image(
    "./resources/logohorizontal.png",  # Ruta al archivo de imagen
    use_column_width=True  # Ajusta la imagen al ancho de la columna
)

# Título de la aplicación
st.title("URL Shortener")

# Campo de entrada de texto para la URL original
url = st.text_input("Enter the Original URL:")

# Botón para generar la nueva URL acortada
if st.button("Generate new URL"):
    # Si se presiona el botón, se acorta la URL y se muestra
    st.write("Shortened URL: ", url_shortener(url))
