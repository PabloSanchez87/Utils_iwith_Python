import streamlit as st
from fpdf import FPDF
from datetime import datetime
import random
import uuid

# Función para generar la factura en PDF
def generar_factura(datos_empresa, datos_cliente, articulos, subtotal, iva, total):
    pdf = FPDF()
    pdf.add_page()

    # Encabezado de la empresa y cliente
    pdf.set_font('Arial', 'B', 12)
    # Datos de la empresa en la derecha
    pdf.set_xy(120, 10)
    pdf.multi_cell(0, 10, f"{datos_empresa['nombre_empresa']}\n{datos_empresa['direccion_empresa']}\nCIF: {datos_empresa['cif_empresa']}", 0, 'R')
    # Datos del cliente en la izquierda
    pdf.set_xy(10, 10)
    pdf.multi_cell(0, 10, f"{datos_cliente['nombre_cliente']} {datos_cliente['apellidos_cliente']}\nTeléfono: {datos_cliente['telefono_cliente']}\nDNI: {datos_cliente['dni_cliente']}\nCiudad: {datos_cliente['ciudad_cliente']}", 0, 'L')

    pdf.ln(20)

    # Información de la factura
    identificador_factura = 'F' + str(random.randint(1000000, 9999999))
    fecha_factura = datetime.now().strftime('%d/%m/%Y')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'FACTURA', ln=True, align='C')
    pdf.set_font('Arial', size=12)
    pdf.cell(0, 10, f'Número de Factura: {identificador_factura}', ln=True, align='C')
    pdf.cell(0, 10, f'Fecha: {fecha_factura}', ln=True, align='C')

    pdf.ln(10)

    # Detalles de los artículos
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Detalles de la Factura', ln=True, align='L')
    pdf.set_font('Arial', size=12)
    pdf.cell(20, 10, 'Cantidad', border=1)
    pdf.cell(70, 10, 'Descripción', border=1)
    pdf.cell(40, 10, 'Precio Unit. (EUR)', border=1)
    pdf.cell(40, 10, 'Precio Total (EUR)', border=1, ln=True)

    for articulo in articulos:
        pdf.cell(20, 10, str(articulo['cantidad']), border=1)
        pdf.cell(70, 10, articulo['descripcion'], border=1)
        pdf.cell(40, 10, f"{articulo['precio_unitario']:.2f}", border=1)
        pdf.cell(40, 10, f"{articulo['precio_total']:.2f}", border=1, ln=True)

    pdf.ln(10)

    # Subtotal, IVA y Total
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(130, 10, 'Subtotal', border=1)
    pdf.cell(40, 10, f'{subtotal:.2f} EUR', border=1, ln=True)
    pdf.cell(130, 10, f'IVA ({iva}%)', border=1)
    pdf.cell(40, 10, f'{subtotal * (iva / 100):.2f} EUR', border=1, ln=True)
    pdf.cell(130, 10, 'Total con IVA', border=1)
    pdf.cell(40, 10, f'{total:.2f} EUR', border=1, ln=True)

    pdf.ln(20)

    # Agradecimiento
    pdf.set_font('Arial', 'I', 12)
    pdf.cell(0, 10, 'Gracias por su compra!', ln=True, align='C')

    pdf_file = f'Factura_{datos_cliente["nombre_cliente"]}_{datos_cliente["apellidos_cliente"]}.pdf'
    pdf.output(pdf_file, 'F')
    return pdf_file

# Configuración de la página de Streamlit
st.title("Generador de Facturas")

# Entrada de datos de la empresa
st.subheader("Datos de la Empresa")
datos_empresa = {
    "nombre_empresa": st.text_input("Nombre de la Empresa"),
    "direccion_empresa": st.text_input("Dirección de la Empresa"),
    "cif_empresa": st.text_input("CIF de la Empresa"),
}

# Entrada de datos del cliente
st.subheader("Datos del Cliente")
datos_cliente = {
    "nombre_cliente": st.text_input("Nombre del Cliente"),
    "apellidos_cliente": st.text_input("Apellidos del Cliente"),
    "telefono_cliente": st.text_input("Teléfono del Cliente"),
    "dni_cliente": st.text_input("DNI del Cliente"),
    "ciudad_cliente": st.text_input("Ciudad del Cliente"),
}

# Lista para almacenar los artículos
if 'articulos' not in st.session_state:
    st.session_state.articulos = []

def agregar_articulo():
    st.session_state.articulos.append({
        "id": str(uuid.uuid4()),  # Genera un identificador único
        "cantidad": 1,
        "descripcion": "",
        "precio_unitario": 0.0,
        "precio_total": 0.0
    })

def eliminar_articulo(articulo_id):
    st.session_state.articulos = [art for art in st.session_state.articulos if art["id"] != articulo_id]
    # Actualización forzada
    st.session_state.dummy_key = not st.session_state.get('dummy_key', False)

# Sección para agregar artículos
st.subheader("Artículos")
st.write("Agregue los artículos a continuación:")

if st.button("Agregar Artículo"):
    agregar_articulo()
    st.session_state.dummy_key = not st.session_state.get('dummy_key', False)  # Forzar actualización

# Encabezados de columnas
cols = st.columns((1, 2, 1, 1, 0.5))
cols[0].write("Cantidad")
cols[1].write("Descripción")
cols[2].write("Precio Unit. (EUR)")
cols[3].write("Precio Total (EUR)")
cols[4].write("")

for articulo in st.session_state.articulos:
    cols = st.columns((1, 2, 1, 1, 0.5))  # Definir columnas para la tabla
    with cols[0]:
        cantidad = st.number_input("Cantidad", min_value=1, step=1, value=articulo['cantidad'], key=f"cantidad_{articulo['id']}", label_visibility="collapsed")
    with cols[1]:
        descripcion = st.text_input("Descripción", value=articulo['descripcion'], key=f"descripcion_{articulo['id']}", label_visibility="collapsed")
    with cols[2]:
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.01, value=articulo['precio_unitario'], format="%.2f", key=f"precio_unitario_{articulo['id']}", label_visibility="collapsed")
    with cols[3]:
        precio_total = cantidad * precio_unitario
        st.write(f"{precio_total:.2f} EUR")
    # Botón para eliminar artículo con icono de papelera
    with cols[4]:
        if st.button("🗑️", key=f"eliminar_{articulo['id']}"):
            eliminar_articulo(articulo["id"])

# Cálculo del subtotal y total
subtotal = sum([articulo['precio_total'] for articulo in st.session_state.articulos])
iva = st.number_input("IVA (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")
total = subtotal + (subtotal * (iva / 100))

# Mostrar el subtotal, IVA y total
st.subheader("Resumen de Factura")
st.write(f"Subtotal: {subtotal:.2f} EUR")
st.write(f"IVA ({iva}%): {subtotal * (iva / 100): .2f} EUR")
st.write(f"Total: {total:.2f} EUR")

# Botón para generar la factura
if st.button("Generar Factura"):
    if not all([datos_empresa['nombre_empresa'], datos_empresa['direccion_empresa'], datos_empresa['cif_empresa'], 
                datos_cliente['nombre_cliente'], datos_cliente['apellidos_cliente'], datos_cliente['telefono_cliente'], 
                datos_cliente['dni_cliente'], datos_cliente['ciudad_cliente'], len(st.session_state.articulos) > 0]):
        st.error("Por favor, complete todos los campos.")
    else:
        factura_file = generar_factura(datos_empresa, datos_cliente, st.session_state.articulos, subtotal, iva, total)
        st.success(f"Factura generada: {factura_file}")
        st.download_button(
            label="Descargar factura",
            data=open(factura_file, "rb").read(),
            file_name=factura_file,
            mime="application/octet-stream"
        )
