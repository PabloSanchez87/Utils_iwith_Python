import os
import re
from connect_to_api import ApiConnector
import streamlit as st

def process_invoice(from_who, to_who, num_invoice, date_invoice, due_date, url_logo, items_invoice, impuesto, descuento, notes, term):
    if not from_who or not to_who or not num_invoice or not date_invoice or not due_date:
        st.warning("Completa los campos obligatorios")
    elif not items_invoice:
        st.warning("Añade algún artículo")
    else:
        try:
            # Generar factura en PDF
            api = ApiConnector()  # Crear instancia de ApiConnector
            root_invoice = api.connect_api_and_save_invoice_pdf(from_who, to_who, url_logo, num_invoice, str(date_invoice), str(due_date), items_invoice, impuesto, descuento, notes, term)

            with open(root_invoice, "rb") as file:
                pdf_data = file.read()
            st.success("Desde aquí puedes descargar la factura generada")
            
            # Norlmalizamos el nombre con la primera palabra del to_who
            to_first_line = to_who.split('\n', 1)[0].strip() if to_who else "SinNombre"
            # Asegurar un nombre de archivo seguro y limpio
            to_first_line = re.sub(r'[^\w\s-]', '', to_first_line)  # Eliminar caracteres no deseados
            filename = f"Factura_{to_first_line}_{num_invoice}.pdf"
            
            st.download_button(label="Descargar factura", data=pdf_data, file_name=filename, mime="application/pdf")
            os.remove(root_invoice)  # Eliminar el archivo PDF temporal después de la descarga
            
        except Exception as excep:
            st.warning(f"Hubo un problema generando la factura pdf: {str(excep)}")
