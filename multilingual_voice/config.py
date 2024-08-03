from dotenv import load_dotenv
import os

# Cargar configuración desde el archivo .env
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# -------------- CONFIGURACIÓN STREAMLIT--------------
page_title = "Traductor de Voz"  # Título de la página de la aplicación
page_icon = "🎤" # Icono de la página
layout = "wide"  # Disposición amplia de la página

# Configuración de Streamlit
def set_page_config():
    import streamlit as st
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.linkedin.com/in/pablosancheztorres/',
            'Report a bug': 'https://github.com/PabloSanchez87/Utils_with_Python/issues',
            'About': "# Traductor de voz a distintos idiomas\nEsta aplicación traduce de forma gratuita pero limitada archivos de voz a distintos idiomas.\n\nCreada por Pablo Sánchez.\nPara soporte, envíe un correo a sancheztorrespablo@gmail.com."
        }
    )
    
    