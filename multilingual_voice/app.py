import streamlit as st
from config import set_page_config
import whisper
from translate import Translator
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from pydub import AudioSegment
import os
from io import BytesIO

# Cargar configuración desde el archivo .env
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Inicializar el cliente de ElevenLabs con la clave API
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Función para convertir texto a voz
def text_to_speech(text: str, language: str) -> BytesIO:
    try:
        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Usar la voz predefinida de Adam
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=0.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        audio_data = BytesIO()

        for chunk in response:
            if chunk:
                audio_data.write(chunk)
        
        audio_data.seek(0)  # Reset the pointer to the beginning of the BytesIO object

    except Exception as e:
        error_message = str(e)
        if 'quota_exceeded' in error_message:
            return None, "Se ha excedido el límite de uso de la API. Por favor, intenta nuevamente más tarde o actualiza tu plan."
        else:
            return None, f"Se ha producido un error creando el audio: {error_message}"

    return audio_data, None

# Función principal para traducir y generar audios
def translator(audio_file):
    error_messages = []
    audios = {}
    
    # 1. Transcribir texto
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file, language="Spanish", fp16=False)
        transcription = result["text"]
    except Exception as e:
        st.error(f"Se ha producido un error transcribiendo el texto: {str(e)}")
        return None, error_messages

    # st.write(f"Texto original: {transcription}")

    # 2. Traducir texto
    try:
        translations = {
            'en':Translator(from_lang="es", to_lang="en").translate(transcription),
            'it': Translator(from_lang="es", to_lang="it").translate(transcription),
            'fr': Translator(from_lang="es", to_lang="fr").translate(transcription),
            'ja': Translator(from_lang="es", to_lang="ja").translate(transcription),
        }
    except Exception as e:
        st.error(f"Se ha producido un error traduciendo el texto: {str(e)}")
        return None, error_messages

    # st.write(f"Texto traducido a Inglés: {en_transcription}")
    # st.write(f"Texto traducido a Italiano: {it_transcription}")
    # st.write(f"Texto traducido a Francés: {fr_transcription}")
    # st.write(f"Texto traducido a Japonés: {ja_transcription}")

    # 3. Generar audio traducido
    for lang, text in translations.items():
        audio, error = text_to_speech(text, lang)
        if audio:
            audios[lang] = audio
        if error:
            error_messages.append(error)

    return audios, error_messages, #translations 

# Función para verificar la duración del audio
def check_audio_duration(audio_file, max_duration=20):
    audio = AudioSegment.from_file(audio_file)
    duration = len(audio) / 1000.0  # Duration in seconds
    return duration <= max_duration

#------------ CONFIGURACION STREAMLIT ------------
set_page_config()  # Configuración inicial de la página, como título y layout
# Interfaz de Streamlit
st.markdown("<h1 style='text-align: center; color: red;'>Traductor de Voz</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center'>Sube tu archivo de audio en español y obtén las traducciones en varios idiomas</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center'>Inglés | Italiano | Francés | Japonés</p>", unsafe_allow_html=True)


with st.container():
    cc1, ccaux ,cc2 = st.columns([5,0.5,5])
    
    cc1.write("Máximo 20 segundos.",unsafe_allow_html=True)
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

