import streamlit as st
import whisper
from translate import Translator
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import os

# Cargar configuración desde el archivo .env
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Inicializar el cliente de ElevenLabs con la clave API
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Función para convertir texto a voz
def text_to_speech(text: str, language: str) -> str:
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

        save_file_path = f"{language}.mp3"

        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

    except Exception as e:
        st.error(f"Se ha producido un error creando el audio: {str(e)}")

    return save_file_path

# Función principal para traducir y generar audios
def translator(audio_file):
    # 1. Transcribir texto
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file, language="Spanish", fp16=False)
        transcription = result["text"]
    except Exception as e:
        st.error(f"Se ha producido un error transcribiendo el texto: {str(e)}")
        return

    st.write(f"Texto original: {transcription}")

    # 2. Traducir texto
    try:
        en_transcription = Translator(from_lang="es", to_lang="en").translate(transcription)
        it_transcription = Translator(from_lang="es", to_lang="it").translate(transcription)
        fr_transcription = Translator(from_lang="es", to_lang="fr").translate(transcription)
        ja_transcription = Translator(from_lang="es", to_lang="ja").translate(transcription)
    except Exception as e:
        st.error(f"Se ha producido un error traduciendo el texto: {str(e)}")
        return

    st.write(f"Texto traducido a Inglés: {en_transcription}")
    st.write(f"Texto traducido a Italiano: {it_transcription}")
    st.write(f"Texto traducido a Francés: {fr_transcription}")
    st.write(f"Texto traducido a Japonés: {ja_transcription}")

    # 3. Generar audio traducido
    en_save_file_path = text_to_speech(en_transcription, "en")
    it_save_file_path = text_to_speech(it_transcription, "it")
    fr_save_file_path = text_to_speech(fr_transcription, "fr")
    ja_save_file_path = text_to_speech(ja_transcription, "ja")

    return en_save_file_path, it_save_file_path, fr_save_file_path, ja_save_file_path

# Interfaz de Streamlit
st.title("Traductor de voz")
st.write("Sube tu archivo de audio en español y obtén las traducciones en varios idiomas")

uploaded_file = st.file_uploader("Sube tu archivo de audio", type=["wav", "mp3"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    if st.button("Traducir y generar audios"):
        with open("temp_audio.wav", "wb") as f:
            f.write(uploaded_file.getbuffer())

        en_path, it_path, fr_path, ja_path = translator("temp_audio.wav")

        st.write("Resultados de las traducciones:")
        st.audio(en_path, format="audio/mp3", start_time=0)
        st.audio(it_path, format="audio/mp3", start_time=0)
        st.audio(fr_path, format="audio/mp3", start_time=0)
        st.audio(ja_path, format="audio/mp3", start_time=0)

        # Eliminar archivos generados
        try:
            os.remove(en_path)
            os.remove(it_path)
            os.remove(fr_path)
            os.remove(ja_path)
            os.remove("temp_audio.wav")
        except Exception as e:
            st.error(f"Se ha producido un error eliminando los archivos: {str(e)}")
