import streamlit as st
import pandas as pd
import re
from create_invoice_api import ApiConnector
import os

# -------------- CONFIGURACIÓN --------------
page_title = "Generador de facturas"  # Título de la página de la aplicación
page_icon = "📄" # Icono de la página
layout = "wide"  # Disposición amplia de la página
euro_symbol = '\u20AC'  # Símbolo del euro
total_expenses = 0  # Variable para almacenar el total de gastos
final_price = 0  # Variable para almacenar el precio final
css = "style/main.css"  # Archivo CSS para estilos personalizados
logo = "Logo Pablo Sánchez"  # Texto para el logo

# Obtener el directorio base del proyecto (un nivel arriba del directorio actual)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Construir la ruta del archivo
url_logo = os.path.join(base_dir, "resources", "logohorizontal.png")

# Configuración de la página de Streamlit
st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/PabloSanchez87',
    }
)

#-------------- VARIABLES DE ESTADO --------------
if "first_time" not in st.session_state:
    st.session_state.first_time = ""  # Marca si es la primera vez que se accede
if "items_invoice" not in st.session_state:
    st.session_state.items_invoice = []  # Lista de artículos para la factura

#-------------- CÓDIGO DE INTERFAZ ----------------

# Sección de información de la factura
with st.container():
    cc1, cc2 = st.columns(2)
    cc1.image(url_logo, caption="Pablo Sánchez", width=100)
    from_who = cc1.text_input("De: *", placeholder="Quién envía esta factura")  # Campo para el remitente de la factura
    to_who = cc1.text_input("Cobrar a: *", placeholder="Para quién es la factura")  # Campo para el destinatario de la factura
    cc2.subheader("FACTURA")
    num_invoice = cc2.text_input("#", placeholder="Número de factura")  # Campo para el número de factura
    date_invoice = cc2.date_input("Fecha *")  # Campo para la fecha de la factura
    due_date = cc2.date_input("Fecha de vencimiento *")  # Campo para la fecha de vencimiento

# Formulario para agregar gastos
with st.form("entry_form", clear_on_submit=True):
    if "expense_data" not in st.session_state:
        st.session_state.expense_data = []  # Lista para almacenar los datos de los gastos
    if "invoice_data" not in st.session_state:
        st.session_state.invoice_data = []  # Lista para almacenar los datos de los artículos de la factura

    cex1, cex2, cex3 = st.columns(3)
    articulo = cex1.text_input("Articulo", placeholder="Descripción del servicio o producto")  # Descripción del artículo o servicio
    amount_expense = cex2.number_input("Cantidad", step=1, min_value=1)  # Cantidad del artículo o servicio
    precio = cex3.number_input("Precio", min_value=0)  # Precio del artículo o servicio
    submitted_expense = st.form_submit_button("Añadir artículo")  # Botón para añadir el artículo
    if submitted_expense:
        if articulo == "":
            st.warning("Añade una descripción del artículo o servicio")
        else:
            st.success("Artículo añadido")
            st.session_state.expense_data.append({"Artículo": articulo, "Cantidad": amount_expense, "Precio": precio, "Total": amount_expense * precio})
            st.session_state.invoice_data.append({"name": articulo, "quantity": amount_expense, "unit_cost": precio})


     # Mostrar tabla de artículos añadidos
    if st.session_state.expense_data:
        df_expense = pd.DataFrame(st.session_state.expense_data)  # Convertir datos de gastos a DataFrame de pandas
        df_expense_invoice = pd.DataFrame(st.session_state.invoice_data)  # Convertir datos de factura a DataFrame de pandas
        st.subheader("Artículos añadidos")
        st.table(df_expense)  # Mostrar tabla con los artículos añadidos
        total_expenses = df_expense["Total"].sum()  # Calcular el total de gastos
        st.text(f"Total: {total_expenses} {euro_symbol}")
        st.session_state.items_invoice = df_expense.to_dict('records')  # Convertir DataFrame a lista de diccionarios
        st.session_state.invoice_data = df_expense_invoice.to_dict('records')
        final_price = total_expenses

# Sección de información adicional de la factura
with st.container():
    cc3, cc4 = st.columns(2)
    notes = cc3.text_area("Notas")  # Área de texto para notas adicionales
    term = cc4.text_area("Términos")  # Área de texto para términos y condiciones
    cc3.write("Subtotal: " + str(total_expenses) + " " + euro_symbol)
    impuesto = cc3.number_input("Impuesto %: ", min_value=0)  # Campo para el porcentaje de impuesto
    if impuesto:
        imp = 1 + (impuesto / 100)
        final_price = final_price * imp
    descuento = cc3.number_input("Descuento %: ", min_value=0)  # Campo para el porcentaje de descuento
    if descuento:
        final_price = round(final_price - ((descuento / 100) * final_price), 2)
    cc3.write("Total: " + str(final_price) + " " + euro_symbol)

submit = st.button("Enviar")  # Botón para enviar y generar la factura

# Acciones después de enviar el formulario
if submit:
    if not from_who or not to_who or not num_invoice or not date_invoice or not due_date:
        st.warning("Completa los campos obligatorios")
    elif len(st.session_state.items_invoice) == 0:
        st.warning("Añade algún artículo")
    else:
        try:
            # Generar factura en PDF
            api = ApiConnector()  # Crear instancia de ApiConnector
            root_invoice = api.connect_api_and_save_invoice_pdf(from_who, to_who, url_logo, num_invoice, str(date_invoice), str(due_date), st.session_state.invoice_data, impuesto, descuento, notes, term)

            with open(root_invoice, "rb") as file:
                pdf_data = file.read()
            st.success("Desde aquí puedes descargar la factura generada")
            st.download_button(label="Descargar factura", data=pdf_data, file_name=f"Factura_{to_who}_{num_invoice}.pdf", mime="application/pdf")
            os.remove(root_invoice)  # Eliminar el archivo PDF temporal después de la descarga
        except Exception as excep:
            st.warning(f"Hubo un problema generando la factura pdf: {str(excep)}")
