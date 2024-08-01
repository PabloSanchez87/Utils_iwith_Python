import streamlit as st
import pandas as pd
from PIL import Image
import cloudinary.uploader
from config import cloudinary, set_page_config, euro_symbol, total_expenses, final_price
import io
from create_invoice import process_invoice


#------------ CONFIGURACION STREAMLIT ------------
set_page_config()

#-------------- VARIABLES DE ESTADO --------------
if "first_time" not in st.session_state:
    st.session_state.first_time = ""  # Marca si es la primera vez que se accede
if "items_invoice" not in st.session_state:
    st.session_state.items_invoice = []  # Lista de artículos para la factura

#-------------- CÓDIGO DE INTERFAZ ----------------
# Título
st.markdown("<h1 style='text-align: center; color: red;'>Generador de facturas</h1>", unsafe_allow_html=True)

# Sección de información de la factura
with st.container():
    cc1, ccaux, cc2 = st.columns([2, 0.1, 2])
    cc1.subheader("Datos")
    from_who = cc1.text_area("De: *", placeholder="Nombre completo:\nDirección:\nTeléfono:\nCIF o DNI:\n",height=110)  # Campo para el remitente de la factura
    to_who = cc1.text_area("Para: *", placeholder="Nombre completo:\nDirección:\nTeléfono:\nCIF o DNI:\n",height=110)  # Campo para el destinatario de la factura
    
    cc2.subheader("Factura")
    # Fila interna dentro de cc2 para número de factura, fecha y fecha de vencimiento
    with cc2:
        num_invoice_col, date_invoice_col, due_date_col = st.columns([1, 1, 1])
        num_invoice = num_invoice_col.text_input("Número de factura (Personalizable) *", placeholder="Número de factura")  # Campo para el número de factura
        date_invoice = date_invoice_col.date_input("Fecha *")  # Campo para la fecha de la factura
        due_date = due_date_col.date_input("Fecha de vencimiento *")  # Campo para la fecha de vencimiento
    
    # Subida de archivo
    uploaded_file = cc2.file_uploader("Cargar un logo", type=["jpg", "jpeg", "png"])
    url_logo = None
    if uploaded_file is not None:
        try:
            # Abre la imagen
            image = Image.open(uploaded_file)
            # Convertir la imagen a bytes para subirla
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes = image_bytes.getvalue()

            # Subir la imagen a Cloudinary
            response = cloudinary.uploader.upload(io.BytesIO(image_bytes), folder="logos/")
            url_logo = response['url']
            cc2.success("Logo cargado exitosamente.")
        except Exception as e:
            cc2.error(f"Error inesperado: {str(e)}")

with st.form("entry_form", clear_on_submit=True):
    if "expense_data" not in st.session_state:
        st.session_state.expense_data = []  # Lista para almacenar los datos de los gastos
    if "invoice_data" not in st.session_state:
        st.session_state.invoice_data = []  # Lista para almacenar los datos de los artículos de la factura

    cex1, cex2, cex3 = st.columns([6, 0.5, 0.5])
    articulo = cex1.text_input("Artículo", placeholder="Descripción del servicio o producto")  # Descripción del artículo o servicio
    amount_expense = cex2.number_input("Cantidad", step=1, min_value=1)  # Cantidad del artículo o servicio
    precio_unit = cex3.number_input("Precio unitario", min_value=0.0, format="%.2f")  # Precio del artículo o servicio
    
    submitted_expense = st.form_submit_button("Añadir artículo")  # Botón para añadir el artículo
    
    if submitted_expense:
        if articulo == "":
            st.warning("Añade una descripción del artículo o servicio")
        else:
            # Calcular subtotal sin descuento
            subtotal = precio_unit * amount_expense
            st.success("Artículo añadido")
            st.session_state.expense_data.append({"Cantidad": amount_expense, "Artículo": articulo,  "Precio unitario": precio_unit, "Subtotal": subtotal})
            st.session_state.invoice_data.append({"name": articulo, "quantity": amount_expense, "unit_cost": precio_unit})

    # Mostrar tabla de artículos añadidos
    if st.session_state.expense_data:
        df_expense = pd.DataFrame(st.session_state.expense_data)  # Convertir datos de gastos a DataFrame de pandas
        st.subheader("Artículos añadidos")
        st.table(df_expense)  # Mostrar tabla con los artículos añadidos
        total_expenses = df_expense["Subtotal"].sum()  # Calcular el total de gastos
        st.text(f"Total: {total_expenses:.2f} {euro_symbol}")
        st.session_state.items_invoice = df_expense.to_dict('records')  # Convertir DataFrame a lista de diccionarios
        final_price = total_expenses

# Sección de información adicional de la factura
with st.container():
    cc3, cc4 = st.columns(2)
    notes = cc3.text_area("Notas", placeholder="Notas aclaratorias")  # Área de texto para notas adicionales
    term = cc4.text_area("Términos", placeholder="Términos y condiciones")  # Área de texto para términos y condiciones

# Sección de impuestos y descuentos
with st.container():
    cc5, cc6, cc7, ccaux  = st.columns([2, 1.5, 4, 9])  # Ajusta el tamaño de las columnas según sea necesario
    descuento = cc5.number_input("Descuento sobre el total %: ", min_value=0, max_value=100, step=1, format="%d")  # Campo para el porcentaje de descuento
    if descuento:
        final_price = round(final_price - ((descuento / 100) * final_price), 2)
    impuesto = cc6.number_input("Impuestos %: ", min_value=0, max_value=100, step=1, format="%d")  # Campo para el porcentaje de impuesto
    
    # Calcular el precio después de aplicar impuestos
    if impuesto:
        final_price = final_price * (1 + (impuesto / 100))
    cc5.write(f"Subtotal: {total_expenses:.2f} {euro_symbol}")
    cc6.write(f":red[Total: {final_price:.2f} {euro_symbol}]")

# Botón para enviar y generar la factura
submit = st.button("Enviar", type="primary") 

if submit:
    process_invoice(from_who, to_who, num_invoice, date_invoice, due_date, url_logo, st.session_state.invoice_data, impuesto, descuento, notes, term)
