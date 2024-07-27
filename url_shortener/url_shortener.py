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
    #print(response_data)
    
    # Verifica si la respuesta contiene la clave 'shorturl' (éxito)
    if 'shorturl' in response_data:
        shorted_url = response_data['shorturl']
        return shorted_url
    else:
        # Muestra un mensaje de error si ocurre un problema
        print(f"Error in URL shortening: {response_data['errormessage']}")
        return None


def is_valid_url(url):
    """
    Verifica si una URL es válida y accesible.

    Args:
        url (str): La URL a verificar.

    Returns:
        bool: True si la URL es válida y accesible, False en caso contrario.
    """
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False



# Main #
if __name__ == "__main__":

    # Pedir al usuario que ingrese la URL original
    original_url = input("Ingrese la URL completa a acortar: ")

    # Verificar si la URL es válida y accesible
    while not is_valid_url(original_url):
        print("La URL ingresada no es válida o no está accesible. Por favor, intente de nuevo.")
        original_url = input("Ingrese la URL a acortar: ")

    # Pedir al usuario que ingrese un alias personalizado
    nick_url = input("Ingrese un alias personalizado para la URL acortada: ")

    # Intentar acortar la URL con el alias proporcionado
    shorted_url = url_shortener(original_url, nick_url)

    # Si el alias ya existe, pedir otro alias
    while shorted_url is None:
        nick_url = input("El alias ya existe o es inválido. Por favor, ingrese otro alias: ")
        shorted_url = url_shortener(original_url, nick_url)

    # Imprimir las URLs originales y acortadas
    print(f'· Original URL: {original_url}')
    print(f'· Shortened URL: {shorted_url}')
