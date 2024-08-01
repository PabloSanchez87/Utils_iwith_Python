import requests
import os
from config import API_KEY_INVOICE_GENERATOR

class ApiConnector:
    def __init__(self) -> None:
        # Define los encabezados HTTP para las solicitudes, indicando que el contenido es de tipo JSON.
        self.headers = self.headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {API_KEY_INVOICE_GENERATOR}', 
            "Accept-Language": "es-ES"
        }
        # Almacena la URL base del servicio al que se conectará.
        self.url = 'https://invoice-generator.com'
        # Define un directorio para almacenar las facturas generadas. Utiliza `os.path.dirname` y `os.path.abspath`
        # para obtener la ruta absoluta del directorio donde se encuentra el archivo de script actual y luego
        # concatena '/invoices' para especificar el subdirectorio donde se guardarán las facturas.
        self.invoice_directory = f"{os.path.dirname(os.path.abspath(__file__))}/{'invoices'}"
        
    
    # El método recibe varios parámetros que representan los detalles necesarios para crear una factura.
    def connect_api_and_save_invoice_pdf(self, from_who, to_who, logo, number, date, 
                                         due_date, items, tax, discounts, notes, terms):
        
        # El diccionario `invoice_parsed` reúne toda la información necesaria para generar la factura.
        invoice_parsed = {  
                        'from': from_who,   # Dirección de facturación y contacto de la organización que emite la factura.
                        'to': to_who,       # Información del destinatario de la factura.
                        'logo': logo,       # URL del logo de la organización que emite la factura.
                        'number': number,   # Número de la factura.
                        'currency': 'EUR',    # Moneda en la que se emitirá la factura. Aquí está fijada en euros.
                        'date': date,       # Fecha de emisión de la factura.
                        'due_date': due_date, # Fecha de vencimiento de la factura.
                        'items': items,     # Artículos o servicios facturados, que se espera sean proporcionados en un formato específico.
                        'fields':{
                                'tax': '%',           # Definición de los campos para impuestos, descuentos y envío.
                                'discounts': '%',         # Aquí se especifica que los impuestos y descuentos se expresan en porcentajes, 
                                'shipping': False         # y el campo de envío no se incluye.        
                                },
                        'tax': tax,         # Impuestos aplicables a la factura.                          
                        'discounts': discounts, # Descuentos aplicables a la factura.
                        'notes': notes ,    # Notas adicionales que puedan ser relevantes para la factura.
                        'terms': terms,      # Términos y condiciones asociados con la factura.
                        # "custom_fields": custom_fields
                        }
        
        
        # Envía una solicitud POST a la URL de la API con los datos de la factura.
        r = requests.post(self.url, json=invoice_parsed, headers=self.headers)
        # Se utiliza `requests.post` para enviar una solicitud HTTP POST a la URL especificada.
        # La carga útil de la solicitud (`json=invoice_parsed`) contiene los datos de la factura en formato JSON.
        # Los encabezados HTTP (`headers=self.headers`) indican que el contenido de la solicitud es de tipo JSON.
        
        # Verifica si la respuesta de la API fue exitosa, lo cual se indica por los códigos de estado HTTP 200 (OK) o 201 (Created).
        if r.status_code == 200 or r.status_code == 201:
            # Si la solicitud es exitosa, el contenido de la respuesta (que se espera sea un PDF) se almacena en la variable `pdf`.
            pdf = r.content
            
            # Llama a un método  para guardar el PDF en un archivo.
            self.save_invoice_to_pdf(pdf, number)
            
            # Genera el nombre del archivo para la factura en formato PDF utilizando el número de la factura.
            name_file = f'{number}_invoice.pdf'
            # Define la ruta del archivo donde se guardará la factura en el directorio de `invoices`.
            root = f'invoices/{name_file}'
        else:
            root = 'Error al generar la factura'
            print('Error: ', r.text)
            # Si la respuesta de la API no es exitosa, se imprime un mensaje de error junto con el texto de la respuesta de la API.
            
        return root # Devuelve la ruta del archivo PDF generado y guardado.
        
    
    
    def save_invoice_to_pdf(self, pdf_content:str, invoice_number) -> None:
        # Este método toma dos argumentos:
        # - `pdf_content`: Un string que contiene los datos binarios del PDF.
        # - `invoice_number`: Un identificador para la factura, que se usa para nombrar el archivo PDF.

        # El nombre del archivo sigue el formato "<número_de_factura>_invoice.pdf".
        invoice_name = f'{invoice_number}_invoice.pdf'
        # Construye la ruta completa donde se guardará el archivo PDF.
        invoice_path = f'{self.invoice_directory}/{invoice_name}'
        
        # Abre el archivo en el modo de escritura binaria (`'wb'`).
        # El modo binario es necesario para escribir el contenido PDF correctamente, que es un formato binario.
        with open(invoice_path, 'wb') as file:
            file.write(pdf_content) # Escribe el contenido del PDF en el archivo.
            
        # Note: El bloque `with` asegura que el archivo se cierre automáticamente después de escribir en él,
        # lo que es importante para liberar recursos y evitar posibles corrupciones de archivo.