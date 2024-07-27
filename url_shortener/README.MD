# URL Shortener
Este proyecto de Python permite acortar URLs utilizando la API de is.gd, con la opción de usar un alias personalizado para la URL acortada.

## Probar en Línea

Puedes probar este script directamente en tu navegador sin necesidad de instalar nada. Visita el siguiente enlace para ejecutar el script en Replit:

[Ejecutar rápida de URL Shortener en Replit](https://replit.com/@PabloSanchez53/UtilswithPython#url_shortener/url_shortener.py)

[Ejecutar URL Shortener en Github.dev codespaces](https://github.dev/PabloSanchez87/Utils_with_Python/blob/main/url_shortener/url_shortener.py)


## Características
- Acorta URLs utilizando la API de [is.gd](https://is.gd/create.php)
- Permite definir un alias personalizado para la URL acortada.
- Verifica si la URL es válida y accesible antes de acortarla.
- [URL Shortening API Reference](https://is.gd/apishorteningreference.php)

## Requisitos Previos
- Python 3.x
- Biblioteca `requests`

### Instalación
1. Clona este repositorio o descarga los archivos `url_shortener.py` y `test_url_shortener.py`.
   
    ```bash
    https://github.com/PabloSanchez87/Utils_with_Python.git
    ```
2. Asegúrate de tener Python 3.x instalado en tu sistema.
   ```bash
   python3 -V
   ```
3. Instala la biblioteca requests necesaria:
    ```bash
    pip install requests
    ```

## Uso
**1. Ejecutar el Script Principal**
- Para acortar una URL, ejecuta `url_shortener.py`. 
- El script pedirá una URL a acortar y un alias personalizado opcional. 
- Si el alias ya está en uso, te pedirá que ingreses otro.
  
    ```bash
    python3 url_shortener.py
    ```

- Ejemplo de entrada y salida:
    ```
    Ingrese la URL a acortar: https://github.com/PabloSanchez87/Utils_with_Python
    Ingrese un alias personalizado para la URL acortada: repository_github_ps87
        · Original URL: https://github.com/PabloSanchez87/Utils_with_Python
        · Shortened URL: https://is.gd/repository_github_ps87
    ```

**2. Verificar la Validez de la URL**
- El script verifica si la URL es válida y accesible antes de intentar acortarla utilizando la función `is_valid_url()`.


## Test
- El archivo `test_url_shortener.py` contiene pruebas unitarias para verificar la funcionalidad de las funciones url_shortener e `is_valid_url`. 
- Utiliza el módulo *unittest* de Python y *mocks de requests* para simular respuestas HTTP.
- Para ejecutar las pruebas, usa el siguiente comando:
  
    ```bash
    python3 test_url_shortener.py
    ```

**Las pruebas incluyen:**

- `test_is_valid_url_success`: Verifica que una URL válida devuelve True.
- `test_is_valid_url_failure`: Verifica que una URL inválida o no accesible devuelve False.
- `test_url_shortener_success`: Verifica que se puede acortar una URL con un alias disponible.
- `test_url_shortener_alias_exists`: Verifica el manejo del error cuando el alias ya está en uso.

## Notas
- La función `url_shortener` utiliza la biblioteca requests para hacer solicitudes HTTP GET a la **API de is.gd**.

- El parámetro `nick_url` permite especificar un alias personalizado para la URL acortada. Si el alias ya está tomado, la API devolverá un error.

## Agradecimientos
- Al servicio [is.gd](https://is.gd/create.php) por proporcionar la API de acortamiento de URLs