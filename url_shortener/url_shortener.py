import requests

def url_shortener(original_url, nick_url):
    """
    Acorta una URL utilizando la API de is.gd, con la opción de usar un alias personalizado.

    Args:
        original_url (str): La URL original que se desea acortar.
        nick_url (str): El alias personalizado para la URL acortada.

    Returns:
        str: La URL acortada si tiene éxito, None si falla.
    """
    base_url = 'https://is.gd/create.php'  # URL base de la API de is.gd
    
    # Parámetros para la solicitud
    params = {
        'format': 'json',     # Especifica el formato de respuesta como JSON
        'url': original_url,  # URL original a acortar
        'shorturl': nick_url  # Alias personalizado para la URL acortada
    }
    
    # Realiza una solicitud GET a la API con los parámetros especificados
    response = requests.get(base_url, params=params)
    # Convierte la respuesta en un diccionario Python
    response_data = response.json()
    
    # Muestra la respuesta completa para depuración
    print(response_data)
    
    # Verifica si la respuesta contiene la clave 'shorturl' (éxito)
    if 'shorturl' in response_data:
        shorted_url = response_data['shorturl']
        return shorted_url
    else:
        # Muestra un mensaje de error si ocurre un problema
        print(f"Error in URL shortening. {response_data['errormessage']}")
        return None

# URL original que se desea acortar
original_url = 'https://github.com/PabloSanchez87/Utils_with_Python'
# Alias personalizado deseado para la URL acortada
nick_url = "repository_github_ps87"

# Intenta acortar la URL con el alias proporcionado
shorted_url = url_shortener(original_url, nick_url)

# Imprime las URLs originales y acortadas si la operación tiene éxito
if shorted_url:
    print(f'· Original URL: {original_url}')
    print(f'· Shorted URL: {shorted_url}')
