import os
import re
from connect_to_api import ApiConnector
import streamlit as st

def process_invoice(from_who, to_who, num_invoice, date_invoice, due_date, url_logo, items_invoice, impuesto, descuento, notes, term):
    # Validar que los campos obligatorios estén llenos
    if not from_who or not to_who or not num_invoice or not date_invoice or not due_date:
        st.warning("Completa los campos obligatorios")
    elif not items_invoice:
        st.warning("Añade algún artículo")
    else:
        try:
            # Crear una instancia de ApiConnector para interactuar con la API
            api = ApiConnector()
            
            # Llamada a la API para generar la factura y obtener el path del archivo PDF
            root_invoice = api.connect_api_and_save_invoice_pdf(
                from_who, to_who, url_logo, num_invoice,
                str(date_invoice), str(due_date), items_invoice,
                impuesto, descuento, notes, term
            )

            # Leer el archivo PDF generado
            with open(root_invoice, "rb") as file:
                pdf_data = file.read()
                
            st.success("Desde aquí puedes descargar la factura generada")
            
            # Extraer la primera línea de 'to_who' para usar como parte del nombre del archivo
            to_first_line = to_who.split('\n', 1)[0].strip() if to_who else "SinNombre"
            
            # Limpiar el nombre de archivo de caracteres no deseados para asegurarse de que sea seguro
            to_first_line = re.sub(r'[^\w\s-]', '', to_first_line)
            filename = f"Factura_{to_first_line}_{num_invoice}.pdf"
            
            # Proporcionar un botón de descarga del PDF generado
            st.download_button(label="Descargar factura", data=pdf_data, file_name=filename, mime="application/pdf")
            
            # Eliminar el archivo PDF temporal después de la descarga para liberar espacio
            os.remove(root_invoice)
            
        except Exception as excep:
            st.warning(f"Hubo un problema generando la factura pdf: {str(excep)}")
