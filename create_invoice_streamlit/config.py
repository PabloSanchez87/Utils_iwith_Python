# config.py
from dotenv import load_dotenv
import os
import cloudinary

load_dotenv()  # Carga las variables desde el archivo .env

# Variables de entorno
API_KEY_INVOICE_GENERATOR = os.getenv('API_KEY_INVOICE_GENERATOR')
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# -------------- CONFIGURACIÓN STREAMLIT--------------
page_title = "Generador de facturas"  # Título de la página de la aplicación
page_icon = "📄" # Icono de la página
layout = "wide"  # Disposición amplia de la página
euro_symbol = '\u20AC'  # Símbolo del euro
total_expenses = 0  # Variable para almacenar el total de gastos
final_price = 0  # Variable para almacenar el precio final

# Configuración de Streamlit
def set_page_config():
    import streamlit as st
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/PabloSanchez87',
        }
    )

