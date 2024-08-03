
# Traductor de Voz

Esta aplicación de Streamlit permite a los usuarios subir un archivo de audio en español y obtener traducciones de texto y audio en varios idiomas (Inglés, Italiano, Francés, Japonés). La aplicación utiliza las APIs de Whisper para la transcripción de audio, MyMemory para la traducción de texto y ElevenLabs para la conversión de texto a voz.

## Requisitos

- Python 3.8+
- Streamlit
- Whisper
- Translate
- ElevenLabs
- Pydub
- dotenv

## Instalación

1. Clona el repositorio o descarga los archivos.

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

2. Instala las dependencias necesarias.

```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` en el directorio raíz del proyecto y añade tu clave de API de ElevenLabs.

```
ELEVENLABS_API_KEY=tu_clave_api
```

## Estructura del Proyecto

- `app.py`: Contiene la lógica principal de la aplicación Streamlit.
- `config.py`: Contiene la configuración inicial de la página Streamlit.
- `functions.py`: Contiene las funciones auxiliares para transcribir, traducir y convertir texto a voz.

## Uso

1. Ejecuta la aplicación Streamlit.

```bash
streamlit run app.py
```

2. Abre tu navegador web y ve a `http://localhost:8501`.

3. Sube un archivo de audio en español y espera a que la aplicación procese y genere las traducciones.

## Descripción de los Archivos

### app.py

Este archivo contiene la lógica principal de la aplicación Streamlit. Incluye la configuración de la página, la carga de archivos y la interfaz de usuario.

### config.py

Este archivo contiene la configuración inicial de la página Streamlit, como el título y el layout.

### functions.py

Este archivo contiene las funciones auxiliares:

- `text_to_speech(text: str, language: str) -> BytesIO`: Convierte el texto a voz utilizando la API de ElevenLabs.
- `translator(audio_file)`: Transcribe el audio, traduce el texto y genera los audios traducidos.
- `check_audio_duration(audio_file, max_duration=20) -> bool`: Verifica la duración del archivo de audio.

## Notas

- Asegúrate de no exceder los límites de uso gratuito de las APIs utilizadas en esta aplicación.
- Si encuentras algún problema, verifica los mensajes de error en la interfaz de Streamlit para más detalles.
- 
## Autor

[Pablo Sánchez Torres](https://www.linkedin.com/in/pablosancheztorres/) - Desarrollador de la aplicación

## Contribuciones
Las contribuciones son bienvenidas. Puedes forkear el proyecto, hacer tus mejoras y enviar un pull request.
