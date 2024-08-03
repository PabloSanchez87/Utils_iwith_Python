import whisper
from translate import Translator
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from pydub import AudioSegment
from io import BytesIO
import os

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
        return None, [f"Se ha producido un error transcribiendo el texto: {str(e)}"]

    # 2. Traducir texto
    try:
        translations = {
            'en': Translator(from_lang="es", to_lang="en").translate(transcription),
            'it': Translator(from_lang="es", to_lang="it").translate(transcription),
            'fr': Translator(from_lang="es", to_lang="fr").translate(transcription),
            'ja': Translator(from_lang="es", to_lang="ja").translate(transcription),
        }
    except Exception as e:
        return None, [f"Se ha producido un error traduciendo el texto: {str(e)}"]

    # 3. Generar audio traducido
    for lang, text in translations.items():
        audio, error = text_to_speech(text, lang)
        if audio:
            audios[lang] = audio
        if error:
            error_messages.append(error)

    return audios, error_messages

# Función para verificar la duración del audio
def check_audio_duration(audio_file, max_duration=20):
    audio = AudioSegment.from_file(audio_file)
    duration = len(audio) / 1000.0  # Duration in seconds
    return duration <= max_duration
