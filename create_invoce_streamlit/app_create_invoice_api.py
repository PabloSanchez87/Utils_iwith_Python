import streamlit as st
import pandas as pd
from create_invoice_api import ApiConnector
import os
import re
import io
from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api

# -------------- CONFIGURACIÓN --------------
page_title = "Generador de facturas"  # Título de la página de la aplicación
page_icon = "📄" # Icono de la página
layout = "wide"  # Disposición amplia de la página
euro_symbol = '\u20AC'  # Símbolo del euro
total_expenses = 0  # Variable para almacenar el total de gastos
final_price = 0  # Variable para almacenar el precio final
logo = "Logo Pablo Sánchez"  # Texto para el logo

# ------------ cloudinary config ------------
cloudinary.config(
  cloud_name='',
  api_key='',
  api_secret=''
)

def upload_image_to_cloudinary(file_path):
    response = cloudinary.uploader.upload(file_path)
    return response['url']


# --------------------------------------------
# Obtener el directorio base del proyecto (un nivel arriba del directorio actual)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


# --------------------------------------------
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

#Título
st.markdown("<h1 style='text-align: center; color: red;'>Generador de facturas</h1>", unsafe_allow_html=True)
  
# Sección de información de la factura
with st.container():
    cc1, ccaux, cc2 = st.columns([2, 0.1, 2])
    cc1.subheader("Datos")
    from_who = cc1.text_area("De: *", placeholder="Nombre completo:\nDirección:\nTeléfono:\nCIF o DNI:\n",)  # Campo para el remitente de la factura
    to_who = cc1.text_area("Para: *", placeholder="Nombre completo:\nDirección:\nTeléfono:\nCIF o DNI:\n")  # Campo para el destinatario de la factura
    
    cc2.subheader("Factura")
    # Fila interna dentro de cc2 para número de factura, fecha y fecha de vencimiento
    with cc2:
        num_invoice_col, date_invoice_col, due_date_col = st.columns([1, 1, 1])
        num_invoice = num_invoice_col.text_input("Número de factura (Personalizable) *", placeholder="Número de factura")  # Campo para el número de factura
        date_invoice = date_invoice_col.date_input("Fecha *")  # Campo para la fecha de la factura
        due_date = due_date_col.date_input("Fecha de vencimiento *")  # Campo para la fecha de vencimiento
    
    # Subida de archivo
    uploaded_file = cc2.file_uploader("Cargar un logo", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Abre la imagen
        image = Image.open(uploaded_file)
        # Muestra la imagen
        # cc2.image(image, caption='Foto subida', use_column_width=True)

        # Convertir la imagen a bytes para subirla
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()

        # Subir la imagen a Cloudinary
        response = cloudinary.uploader.upload(io.BytesIO(image_bytes), folder="logos/")
        url_logo = response['url']

# Formulario para agregar gastos
with st.form("entry_form", clear_on_submit=True):
    if "expense_data" not in st.session_state:
        st.session_state.expense_data = []  # Lista para almacenar los datos de los gastos
    if "invoice_data" not in st.session_state:
        st.session_state.invoice_data = []  # Lista para almacenar los datos de los artículos de la factura

    cex1, cex2, cex3 = st.columns([4,0.5,0.5])
    articulo = cex1.text_input("Artículo", placeholder="Descripción del servicio o producto")  # Descripción del artículo o servicio
    amount_expense = cex2.number_input("Cantidad", step=1, min_value=1)  # Cantidad del artículo o servicio
    precio = cex3.number_input("Precio unitario", min_value=0)  # Precio del artículo o servicio
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
    notes = cc3.text_area("Notas",placeholder="Notas aclaratorias")  # Área de texto para notas adicionales
    term = cc4.text_area("Términos", placeholder="Términos y condiciones")  # Área de texto para términos y condiciones

# Sección de impuestos y descuentos
with st.container():
    cc5, cc6, cc7, cclogo, cclinks  = st.columns([1.5,1.5,4,9,2])  # Ajusta el tamaño de las columnas según sea necesario
    descuento = cc5.number_input("Descuento %: ", min_value=0, max_value=100, step=1, format="%d")  # Campo para el porcentaje de descuento
    if descuento:
        final_price = round(final_price - ((descuento / 100) * final_price), 2)
    impuesto = cc6.number_input("Impuestos %: ", min_value=0, max_value=100, step=1, format="%d")  # Campo para el porcentaje de impuesto
    
    # Calcular el precio después de aplicar impuestos
    if impuesto:
        final_price = final_price * (1 + (impuesto / 100))
    cc5.write(f"Subtotal: {total_expenses:.2f} {euro_symbol}")
    cc6.write(f":red[Total: {final_price:.2f} {euro_symbol}]")
    
    with cclinks:
        st.write(" ")
        ccempty, cclink = st.columns([1,10])
        cclink.link_button(":blue[Linkedin Dev]", "https://www.linkedin.com/in/pablosancheztorres/")
        cclink.link_button(":violet[Github Dev]", "https://github.com/PabloSanchez87")

submit = st.button("Enviar", type="primary")  # Botón para enviar y generar la factura


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
            
            # Norlmalizamos el nombre con la primera palabra del to_who
            to_first_line = to_who.split('\n', 1)[0].strip() if to_who else "SinNombre"
            # Asegurar un nombre de archivo seguro y limpio
            to_first_line = re.sub(r'[^\w\s-]', '', to_first_line)  # Eliminar caracteres no deseados
            filename = f"Factura_{to_first_line}_{num_invoice}.pdf"
            
            st.download_button(label="Descargar factura", data=pdf_data, file_name=filename, mime="application/pdf")
            os.remove(root_invoice)  # Eliminar el archivo PDF temporal después de la descarga
            
        except Exception as excep:
            st.warning(f"Hubo un problema generando la factura pdf: {str(excep)}")
