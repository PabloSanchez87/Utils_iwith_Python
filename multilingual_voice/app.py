import streamlit as st
from config import set_page_config
from functions import translator, check_audio_duration
import os

#------------ CONFIGURACION STREAMLIT ------------
set_page_config()  # Configuración inicial de la página, como título y layout

# Interfaz de Streamlit
st.markdown("<h1 style='text-align: center; color: red;'>Traductor de Voz</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center'>Sube tu archivo de audio en español y obtén las traducciones en varios idiomas</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center'>Inglés | Italiano | Francés | Japonés</p>", unsafe_allow_html=True)

with st.container():
    cc1, ccaux, cc2 = st.columns([5, 0.5, 5])
    
    cc1.write("Máximo 20 segundos.", unsafe_allow_html=True)
    uploaded_file = cc1.file_uploader("Sube tu archivo de audio", type=["wav", "mp3"])

    if uploaded_file is not None:
        cc1.audio(uploaded_file, format="audio/wav")
        if check_audio_duration(uploaded_file):
            if cc1.button("Traducir y generar audios"):
                with open("temp_audio.wav", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                audios, error_messages = translator("temp_audio.wav")

                if audios:
                    # Guardar los archivos de audio en el estado de la sesión
                    for lang, audio in audios.items():
                        st.session_state[f'{lang}_audio'] = audio

                # Eliminar el archivo temporal
                os.remove("temp_audio.wav")

                if error_messages:
                    cc2.write(" ")
                    cc2.write(" ")
                    cc2.warning("Resultado de la conexión con la API:")
                    cc2.warning(" ".join(set(error_messages)))
        else:
            cc1.error("El archivo de audio excede los 20 segundos. Por favor, sube un archivo más corto.")

    # Verificar si los archivos de audio están en el estado de la sesión
    if any(f'{lang}_audio' in st.session_state for lang in ['en', 'it', 'fr', 'ja']):
        cc2.write(":green[Resultados de las traducciones]")
        
        if 'en_audio' in st.session_state:
            cc2.write("Inglés")
            cc2.audio(st.session_state['en_audio'], format="audio/mp3", start_time=0)
            # cc2.download_button(
            #     label="Descargar audio en Inglés",
            #     data=st.session_state['en_audio'],
            #     file_name="english_translation.mp3",
            #     mime="audio/mp3"
            # )
            
        if 'it_audio' in st.session_state:
            cc2.write("Italiano")
            cc2.audio(st.session_state['it_audio'], format="audio/mp3", start_time=0)
            # cc2.download_button(
            #     label="Descargar audio en Italiano",
            #     data=st.session_state['it_audio'],
            #     file_name="italian_translation.mp3",
            #     mime="audio/mp3"
            # )
            
        if 'fr_audio' in st.session_state:
            cc2.write("Francés")
            cc2.audio(st.session_state['fr_audio'], format="audio/mp3", start_time=0)
            # cc2.download_button(
            #     label="Descargar audio en Francés",
            #     data=st.session_state['fr_audio'],
            #     file_name="french_translation.mp3",
            #     mime="audio/mp3"
            # )
            
        if 'ja_audio' in st.session_state:
            cc2.write("Japonés")
            cc2.audio(st.session_state['ja_audio'], format="audio/mp3", start_time=0)
            # cc2.download_button(
            #     label="Descargar audio en Japonés",
            #     data=st.session_state['ja_audio'],
            #     file_name="japanese_translation.mp3",
            #     mime="audio/mp3"
            # )
