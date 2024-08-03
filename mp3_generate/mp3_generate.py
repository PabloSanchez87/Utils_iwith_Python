import os
from gtts import gTTS

# Obtener la ruta del directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Texto en español
text = "Hola, este es un ejemplo de generación de un archivo de audio en formato MP3 usando la libreria de Python Google Text-to-Speech (gTTS)."

# Generar el archivo de audio
tts = gTTS(text=text, lang='es')

# Ruta completa para guardar el archivo en el mismo directorio del script
audio_file_path = os.path.join(script_dir, "audio_example.mp3")
tts.save(audio_file_path)

print(f"Archivo de audio guardado en: {audio_file_path}")
