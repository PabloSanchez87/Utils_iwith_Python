
# AI Image Generator App

## Descripción
Esta aplicación web, desarrollada con Streamlit, permite a los usuarios generar imágenes utilizando la API de OpenAI. La aplicación toma un prompt descriptivo proporcionado por el usuario y genera una imagen basada en ese texto, utilizando el modelo DALL-E.

## Características
- **Generación de imágenes AI**: Utiliza el modelo DALL-E de OpenAI para crear imágenes basadas en descripciones de texto.
- **Interfaz de usuario intuitiva**: Fácil de usar, con un campo de texto para ingresar la descripción y un botón para generar la imagen.
- **Descarga de imágenes**: Las imágenes generadas pueden ser descargadas directamente desde la aplicación.

## Requisitos

- **Python 3.7 o superior**
- **Paquetes de Python**:
  - `requests`
  - `streamlit`

## Instalación

1. **Clonar el repositorio**:
   ```bash
   https://github.com/PabloSanchez87/Utils_with_Python.git
   cd ai-image-generator
   ```

2. **Crear un entorno virtual (opcional pero recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/MacOS
   .\venv\Scripts\activate  # En Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Configurar la clave de API de OpenAI**:

   - Colocar tu clave de API directamente en el código:
     ```python
     api_key = 'TU_CLAVE_DE_API'
     ```
   - O usar una **variable de entorno para mayor seguridad**:
     ```python
     import os
     api_key = os.getenv('OPENAI_API_KEY')
     if not api_key:
         st.error("API key is missing. Please set the OPENAI_API_KEY environment variable.")
         st.stop()
     ```
   - **Asegúrate de no compartir tu clave de API públicamente para evitar usos no autorizados.**

2. **Ejecutar la aplicación**:
   ```bash
   streamlit run openAI_image_creator.py
   ```

3. **Interactuar con la aplicación**:
   - Introduce una descripción en el campo de texto y presiona "Generate Image" para crear una imagen.
   - Descarga la imagen generada usando el botón de descarga.

## Notas
- Recuerda mantener tu clave de API segura y no compartirla públicamente.
- Para un mejor manejo de las claves de API, considera usar un archivo de configuración seguro o variables de entorno.
