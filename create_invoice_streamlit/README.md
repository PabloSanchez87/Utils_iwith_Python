
# Generador de Facturas con Streamlit

## Descripción

Este proyecto es una aplicación web desarrollada con Streamlit para generar facturas de manera interactiva. 

Los usuarios pueden ingresar información sobre el remitente y destinatario de la factura, añadir artículos o servicios, y aplicar descuentos e impuestos. 

La aplicación genera un archivo PDF de la factura, que puede ser descargado por el usuario.

[Ejemplo de factura generada](/create_invoice_streamlit/invoices/Factura_Cliente%20ABC%20SA_INV-2024-001.pdf)

![Factura](/create_invoice_streamlit/invoices/imagen_factura.png)

## Requisitos del Sistema

- Python 3.7 o superior
- Paquetes de Python:
  - streamlit
  - pandas
  - Pillow
  - cloudinary
  - requests

## Instalación

1. Clonar el repositorio o descargar los archivos necesarios.
2. Crear un entorno virtual y activar el entorno:

   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Configuración

### Claves API Necesarias (Gratuitas)
- [**Cloudinary Cloud name, API Key y Secret**](https://cloudinary.com/documentation/cloudinary_glossary#api_key_and_secret)
- [**API Key para Generación de Facturas**](https://invoice-generator.com/developers#getting-started)

  

  
### Archivo `config.py`

Configura las variables necesarias para la aplicación, como las claves de API para Cloudinary, detalles de la página de Streamlit, y símbolos de moneda. Asegúrate de que todos los valores necesarios están configurados correctamente.

### Archivo `connect_to_api.py`

Este archivo contiene la clase `ApiConnector`, que se utiliza para conectarse a una API externa para generar el archivo PDF de la factura. Configura los detalles de la API según sea necesario.

### Archivo `create_invoice.py`

Contiene la lógica para procesar los datos de la factura y conectarse a la API para crear el archivo PDF.

## Uso

1. Ejecuta la aplicación:

   ```bash
   streamlit run app_streamlit.py
   ```

2. Abre el navegador web en la dirección proporcionada (por defecto `http://localhost:8501`).

3. Rellena los campos necesarios:
   - **Datos del remitente y destinatario:** Información básica para la factura.
   - **Número de factura, fechas:** Detalles específicos de la factura.
   - **Artículos o servicios:** Añade artículos con descripción, cantidad, y precio unitario.
   - **Descuentos e impuestos:** Aplica descuentos y calcula impuestos.

4. Genera y descarga la factura en formato PDF.

## Notas de Implementación

- **Estado de Sesión:** Utiliza `st.session_state` para almacenar datos de la sesión como artículos añadidos y detalles de la factura.
- **Manejo de Archivos:** Los archivos PDF generados son temporales y se eliminan después de ser descargados.


## Posibles Extensiones

- Integración con sistemas de pago para generar facturas pagaderas en línea.
- Base de datos para almacenar facturas y clientes.
- Funcionalidad multiusuario con autenticación.

## Autor

[Pablo Sánchez Torres](https://www.linkedin.com/in/pablosancheztorres/) - Desarrollador de la aplicación

## Contribuciones
Las contribuciones son bienvenidas. Puedes forkear el proyecto, hacer tus mejoras y enviar un pull request.


