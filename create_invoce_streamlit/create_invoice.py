import streamlit as st
from fpdf import FPDF
from datetime import datetime
import uuid

# Función para generar la factura en PDF
def generar_factura(datos_empresa, datos_cliente, articulos, subtotal, iva, total):
    pdf = FPDF()
    pdf.add_page()

    # Encabezado de la empresa y cliente
    pdf.set_font('Arial', 'B', 12)
    pdf.set_xy(120, 10)
    pdf.multi_cell(0, 10, f"{datos_empresa['nombre_empresa']}\n{datos_empresa['direccion_empresa']}\nCIF: {datos_empresa['cif_empresa']}\nTeléfono: {datos_empresa['telefono_empresa']}\nEmail: {datos_empresa['email_empresa']}", 0, 'R')
    pdf.set_xy(10, 10)
    pdf.multi_cell(0, 10, f"{datos_cliente['nombre_cliente']} {datos_cliente['apellidos_cliente']}\nTeléfono: {datos_cliente['telefono_cliente']}\nDNI: {datos_cliente['dni_cliente']}\nCiudad: {datos_cliente['ciudad_cliente']}", 0, 'L')

    pdf.ln(20)

    # Información de la factura
    identificador_factura = 'F' + datetime.now().strftime('%Y%m%d%H%M%S')
    fecha_factura = datetime.now().strftime('%d/%m/%Y')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'FACTURA', ln=True, align='C')
    pdf.set_font('Arial', size=12)
    pdf.cell(0, 10, f'Número de Factura: {identificador_factura}', ln=True, align='C')
    pdf.cell(0, 10, f'Fecha: {fecha_factura}', ln=True, align='C')

    pdf.ln(10)

    # Detalles de los artículos
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(20, 10, 'Cantidad', border=1)
    pdf.cell(80, 10, 'Descripción', border=1)
    pdf.cell(45, 10, 'Precio Unit. (EUR)', border=1)
    pdf.cell(45, 10, 'Precio Total (EUR)', border=1, ln=True)

    pdf.set_font('Arial', size=12)
    for articulo in articulos:
        precio_total_articulo = articulo['cantidad'] * articulo['precio_unitario']
        pdf.cell(20, 10, str(articulo['cantidad']), border=1)
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(80, 10, articulo['descripcion'], border=1)
        pdf.set_xy(x + 80, y)
        pdf.cell(45, 10, f"{articulo['precio_unitario']:.2f}", border=1)
        pdf.cell(45, 10, f"{precio_total_articulo:.2f}", border=1, ln=True)

    pdf.ln(10)

    # Subtotal, IVA y Total
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(145, 10, 'Subtotal', border=1)
    pdf.cell(45, 10, f'{subtotal:.2f} EUR', border=1, ln=True)
    pdf.cell(145, 10, f'IVA ({iva}%)', border=1)
    pdf.cell(45, 10, f'{subtotal * (iva / 100):.2f} EUR', border=1, ln=True)
    pdf.cell(145, 10, 'Total con IVA', border=1)
    pdf.cell(45, 10, f'{total:.2f} EUR', border=1, ln=True)

    pdf.ln(20)

    pdf.set_font('Arial', 'I', 12)
    pdf.cell(0, 10, 'Gracias por su compra!', ln=True, align='C')

    pdf_file = f'Factura_{datos_cliente["nombre_cliente"]}_{datos_cliente["apellidos_cliente"]}.pdf'
    pdf.output(pdf_file, 'F')
    return pdf_file

st.title("Generador de Facturas")

st.subheader("Datos de la Empresa")
datos_empresa = {
    "nombre_empresa": st.text_input("Nombre de la Empresa"),
    "direccion_empresa": st.text_input("Dirección de la Empresa"),
    "cif_empresa": st.text_input("CIF de la Empresa"),
    "telefono_empresa": st.text_input("Teléfono de la Empresa"),
    "email_empresa": st.text_input("Email de la Empresa"),
}

st.subheader("Datos del Cliente")
datos_cliente = {
    "nombre_cliente": st.text_input("Nombre del Cliente"),
    "apellidos_cliente": st.text_input("Apellidos del Cliente"),
    "telefono_cliente": st.text_input("Teléfono del Cliente"),
    "dni_cliente": st.text_input("DNI del Cliente"),
    "ciudad_cliente": st.text_input("Ciudad del Cliente"),
}

if 'articulos' not in st.session_state:
    st.session_state.articulos = []

st.subheader("Artículos")
st.write("Agregue los artículos a continuación:")
if st.button("Agregar Artículo"):
    st.session_state.articulos.append({
        "id": str(uuid.uuid4()),
        "cantidad": 1,
        "descripcion": "",
        "precio_unitario": 0.0
    })

for articulo in st.session_state.articulos:
    cols = st.columns((1, 3, 1, 1, 0.5))
    with cols[0]:
        cantidad = st.number_input("Cantidad", min_value=1, step=1, value=articulo['cantidad'], key=f"cantidad_{articulo['id']}", label_visibility="collapsed")
        articulo['cantidad'] = cantidad
    with cols[1]:
        descripcion = st.text_area("Descripción", value=articulo['descripcion'], key=f"descripcion_{articulo['id']}", height=100, label_visibility="collapsed")
        articulo['descripcion'] = descripcion
    with cols[2]:
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.01, value=articulo['precio_unitario'], format="%.2f", key=f"precio_unitario_{articulo['id']}", label_visibility="collapsed")
        articulo['precio_unitario'] = precio_unitario
    with cols[3]:
        precio_total = cantidad * precio_unitario
        articulo['precio_total'] = precio_total
        st.write(f"{precio_total:.2f} EUR")
    with cols[4]:
        if st.button("🗑️", key=f"eliminar_{articulo['id']}"):
            st.session_state.articulos = [a for a in st.session_state.articulos if a['id'] != articulo['id']]

subtotal = sum(articulo['precio_total'] for articulo in st.session_state.articulos)
iva = st.number_input("IVA (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")
total = subtotal + (subtotal * (iva / 100))

st.subheader("Resumen de Factura")
st.write(f"Subtotal: {subtotal:.2f} EUR")
st.write(f"IVA ({iva}%): {subtotal * (iva / 100):.2f} EUR")
st.write(f"Total: {total:.2f} EUR")

if st.button("Generar Factura"):
    if not all([datos_empresa['nombre_empresa'], datos_empresa['direccion_empresa'], datos_empresa['cif_empresa'], datos_empresa['telefono_empresa'], datos_empresa['email_empresa'],
                datos_cliente['nombre_cliente'], datos_cliente['apellidos_cliente'], datos_cliente['telefono_cliente'],
                datos_cliente['dni_cliente'], datos_cliente['ciudad_cliente'], st.session_state.articulos]):
        st.error("Por favor, complete todos los campos.")
    else:
        factura_file = generar_factura(datos_empresa, datos_cliente, st.session_state.articulos, subtotal, iva, total)
        st.success(f"Factura generada: {factura_file}")
        st.download_button(
            label="Descargar factura",
            data=open(factura_file, "rb").read(),
            file_name=factura_file,
            mime="application/pdf"
        )
