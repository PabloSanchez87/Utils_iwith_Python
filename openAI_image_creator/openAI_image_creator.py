import requests  # Biblioteca para realizar solicitudes HTTP
import streamlit as st  # Biblioteca para crear aplicaciones web interactivas

################################################
## Si tenemos la API en una variable de entorno
# import os
# Carga de la clave de API desde una variable de entorno para mayor seguridad
# api_key = os.getenv('OPENAI_API_KEY')
# if not api_key:
#     st.error("API key is missing. Please set the OPENAI_API_KEY environment variable.")
#     st.stop()
################################################

# Tu clave de API para autenticarte con el servicio de OpenAI
api_key = 'OPENAI_API_KEY'

def openai_request(prompt):
    """
    Envía una solicitud a la API de OpenAI para generar una imagen basada en el prompt proporcionado.

    Args:
        prompt (str): Texto descriptivo que detalla lo que se debe representar en la imagen.

    Returns:
        str: La URL de la imagen generada por el modelo.
    """
    # Encabezados de la solicitud, incluyendo la autorización con la clave API
    headers = {'Authorization': f'Bearer {api_key}'}
    
    # Realiza la solicitud POST a la API de OpenAI para generar una imagen
    response = requests.post(
        'https://api.openai.com/v1/images/generations',  # Endpoint de la API para generación de imágenes
        headers=headers,  # Encabezados de la solicitud, incluyendo la autenticación
        json={
            'prompt': prompt,  # El prompt o descripción textual para la imagen
            'model': 'dall-e-3',  # Modelo a utilizar (en este caso, DALL-E 3)
            'size': '1792x1024',  # Tamaño de la imagen generada
            'quality': 'standard',  # Calidad de la imagen
            'n': 1  # Número de imágenes a generar
        }
    )
    
    # Verificación del estado de la respuesta
    if response.status_code != 200:
        # Si la solicitud no fue exitosa, se lanza una excepción con el mensaje de error
        st.error(f"Error: {response.status_code} - {response.json().get('error', {}).get('message', 'Unknown error')}")
        return None
    else:
        # Si la solicitud es exitosa, se extrae la URL de la imagen generada
        image_url = response.json()['data'][0]['url']
        return image_url  # Se devuelve la URL de la imagen generada

def download_image(url, filename):
    """
    Descarga una imagen desde una URL y la guarda localmente.

    Args:
        url (str): URL de la imagen a descargar.
        filename (str): Ruta y nombre del archivo donde se guardará la imagen.
    """
    response = requests.get(url)  # Realiza una solicitud GET para obtener la imagen
    with open(filename, 'wb') as file:  # Abre un archivo en modo de escritura binaria
        file.write(response.content)  # Escribe el contenido de la respuesta en el archivo

# Configuración de la página de Streamlit
st.set_page_config(page_title="AI Image Generator", page_icon="../resources/Favicon/favicon.ico", layout="centered")

# Muestra un logo en la página (la ruta debe ser ajustada según la ubicación real del archivo)
st.image("../resources/logohorizontal.png", use_column_width=True)
st.title("Create AI Images")  # Título de la aplicación web

# Área de texto donde el usuario puede ingresar el prompt para la imagen
description = st.text_area("Prompt")

# Botón para iniciar la generación de la imagen
if st.button("Generate Image"):
    if description:
        with st.spinner("Generating your image..."):  # Muestra un indicador de carga mientras se genera la imagen
            url = openai_request(description)  # Llama a la función para generar la imagen y obtiene la URL de la misma
            if url:
                filename = "./images/image_generator.png"  # Define el nombre y la ruta del archivo para guardar la imagen
                download_image(url, filename)  # Descarga la imagen desde la URL y la guarda localmente
                st.image(filename, use_column_width=True)  # Muestra la imagen descargada en la aplicación
                
                # Prepara la imagen para descarga por el usuario
                with open(filename, "rb") as file:  # Abre la imagen en modo de lectura binaria
                    image_data = file.read()  # Lee los datos de la imagen
                
                # Botón para que el usuario descargue la imagen
                st.download_button(label="Download Image", data=image_data, file_name="image_generated.jpg")
    else:
        st.warning("Please enter a description for the image.")  # Mensaje de advertencia si el prompt está vacío
