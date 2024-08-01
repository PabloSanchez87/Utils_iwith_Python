import streamlit as st
import pandas as pd

# Función para cargar los datos iniciales
@st.cache_data
def load_data():
    data = {
        'Nombre': ['Ana', 'Juan', 'Pedro', 'Marta'],
        'Edad': [23, 34, 45, 29],
        'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla']
    }
    return pd.DataFrame(data)

# Cargar datos al iniciar la app si no están en session_state
if 'df' not in st.session_state:
    st.session_state.df = load_data()

st.title("Tabla Interactiva con Streamlit")

# Usar st.data_editor para permitir la edición directa de la tabla
edited_df = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",  # Permitir agregar y eliminar filas
    column_config={
        "Nombre": "Nombre",
        "Edad": "Edad",
        "Ciudad": "Ciudad",
    },
    hide_index=False  # Mostrar el índice de la tabla
)

# Identificar filas eliminadas
deleted_rows = st.session_state.df[~st.session_state.df.index.isin(edited_df.index)]

# Actualizar el DataFrame en el estado de sesión si hubo cambios
if not deleted_rows.empty:
    st.session_state.df = edited_df
    st.success(f"{len(deleted_rows)} filas eliminadas exitosamente.")

# Mostrar el DataFrame actualizado
st.write("Tabla de datos actualizada:")
st.dataframe(st.session_state.df)
