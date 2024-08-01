import streamlit as st
import pandas as pd
from PIL import Image
import cloudinary.uploader
from config import cloudinary, set_page_config, euro_symbol, total_expenses, final_price
import io
from create_invoice import process_invoice

#------------ CONFIGURACION STREAMLIT ------------
set_page_config()  # Configuración inicial de la página, como título y layout

#-------------- VARIABLES DE ESTADO --------------
# Estas variables de estado persisten a lo largo de la sesión del usuario
if "expense_data" not in st.session_state:
    st.session_state.expense_data = []  # Lista para almacenar los artículos añadidos
if "invoice_data" not in st.session_state:
    st.session_state.invoice_data = []  # Lista para almacenar los datos procesados para la factura

#-------------- CÓDIGO DE INTERFAZ ----------------
# Título principal de la aplicación
st.markdown("<h1 style='text-align: center; color: red;'>Generador de facturas</h1>", unsafe_allow_html=True)

# Sección de información de la factura
with st.container():
    cc1, ccaux, cc2 = st.columns([2, 0.1, 2])
    cc1.subheader("Datos")
    
    # Datos del remitente de la factura (quien emite)
    from_who = cc1.text_area("De: *", placeholder="Nombre completo:\nDirección:\nTeléfono:\nCIF o DNI:\n", height=110)
    
    # Datos del destinatario de la factura (quien recibe)
    to_who = cc1.text_area("Para: *", placeholder="Nombre completo:\nDirección:\nTeléfono:\nCIF o DNI:\n", height=110)
    
    cc2.subheader("Factura")
    # Campos para el número de factura, fecha y fecha de vencimiento
    with cc2:
        num_invoice_col, date_invoice_col, due_date_col = st.columns([1, 1, 1])
        num_invoice = num_invoice_col.text_input("Número de factura (Personalizable) *", placeholder="Número de factura")
        date_invoice = date_invoice_col.date_input("Fecha *")
        due_date = due_date_col.date_input("Fecha de vencimiento *")
    
    # Opción para subir un logo a la factura
    uploaded_file = cc2.file_uploader("Cargar un logo", type=["jpg", "jpeg", "png"])
    url_logo = None
    if uploaded_file is not None:
        try:
            # Cargar y preparar la imagen para subida
            image = Image.open(uploaded_file)
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes = image_bytes.getvalue()

            # Subir la imagen a Cloudinary y obtener la URL
            response = cloudinary.uploader.upload(io.BytesIO(image_bytes), folder="logos/")
            url_logo = response['url']
            cc2.success("Logo cargado exitosamente.")
        except Exception as e:
            cc2.error(f"Error inesperado: {str(e)}")

# Formulario para añadir artículos a la factura
with st.form("entry_form", clear_on_submit=True):
    cex1, cex2, cex3 = st.columns([6, 0.5, 0.5])
    
    # Campos para ingresar los detalles de cada artículo
    articulo = cex1.text_input("Artículo", placeholder="Descripción del servicio o producto")
    cantidad = cex2.number_input("Cantidad", step=1, min_value=1)
    precio_unit = cex3.number_input("Precio unitario", min_value=0.0, format="%.2f")
    
    # Botón para añadir el artículo
    submitted_expense = st.form_submit_button("Añadir artículo")
    
    if submitted_expense:
        if articulo == "":
            st.warning("Añade una descripción del artículo o servicio")
        else:
            # Calcular el subtotal para el artículo añadido
            subtotal = precio_unit * cantidad
            st.success("Artículo añadido")
            # Guardar los datos del artículo en el estado de sesión
            st.session_state.expense_data.append({
                "name": articulo, 
                "quantity": cantidad,  
                "unit_cost": precio_unit, 
                "subtotal": subtotal
            })

# Uso de st.data_editor para edición interactiva de la tabla de artículos
if st.session_state.expense_data:
    df_expense = pd.DataFrame(st.session_state.expense_data)  # Convertir los datos a un DataFrame de pandas
    st.subheader("Artículos añadidos")
    
    # Editor interactivo para modificar los artículos añadidos
    edited_df = st.data_editor(
        df_expense,
        num_rows="dynamic",
        column_config={
            "quantity": st.column_config.NumberColumn("Cantidad", 
                                                      width="small", 
                                                      min_value=1, 
                                                      step=1,
                                                      format="%d"),
            "name": st.column_config.TextColumn("Artículo",
                                                width="large"),
            "unit_cost": st.column_config.NumberColumn(f"Precio unitario({euro_symbol})",
                                                        help="Precio por unidad en EUROS",
                                                        min_value=0, 
                                                        width="small"),
            "subtotal": st.column_config.NumberColumn("Subtotal", 
                                                        disabled=True, 
                                                        width="small")
        },
        hide_index=True, 
        use_container_width=True,
        column_order=("quantity", "name", "unit_cost", "subtotal"),
    )

    # Identificar filas eliminadas
    deleted_rows = df_expense[~df_expense.index.isin(edited_df.index)]
    if not deleted_rows.empty:
        st.success(f"{len(deleted_rows)} filas eliminadas exitosamente.")
        
    # Actualizar el DataFrame y el estado de sesión con los datos editados
    st.session_state.expense_data = edited_df.to_dict('records')
    # Crear una versión sin el campo 'subtotal' para pasar a la API
    invoice_data_clean = edited_df.drop(columns=["subtotal"]).to_dict('records')
    st.session_state.invoice_data = invoice_data_clean  # Actualizar los datos de la factura
    total_expenses = edited_df["subtotal"].sum()  # Calcular el total de gastos (subtotal general)
    st.text(f"Subtotal: {total_expenses:.2f} {euro_symbol}")

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
        total_expenses = round(total_expenses - ((descuento / 100) * total_expenses), 2)
    impuesto = cc6.number_input("Impuestos %: ", min_value=0, max_value=100, step=1, format="%d")  # Campo para el porcentaje de impuesto
    
    # Calcular el precio después de aplicar impuestos
    final_price = total_expenses
    if impuesto:
        final_price = round(total_expenses * (1 + (impuesto / 100)), 2)
    cc5.write(f"Subtotal: {total_expenses:.2f} {euro_symbol}")
    cc6.write(f":red[Total: {final_price:.2f} {euro_symbol}]")

# Botón para enviar y generar la factura
submit = st.button("Enviar", type="primary") 

# Llamada a la función de procesamiento de la factura al enviar
if submit:
    process_invoice(from_who, to_who, num_invoice, date_invoice, due_date, url_logo, st.session_state.invoice_data, impuesto, descuento, notes, term)
