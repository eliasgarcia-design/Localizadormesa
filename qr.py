import streamlit as st
import pandas as pd

# Título de la web
st.title("🎫 Localizador de Mesas")
st.write("Ingresa tu carnet para saber en qué mesa estás.")

# Función para cargar y limpiar datos
@st.cache_data
def cargar_datos():
    # Asegúrate de que el nombre coincida con tu archivo Excel
    df = pd.read_excel('datos.xlsx')
    # Limpiamos la columna Codigo
    df['Codigo'] = df['Codigo'].astype(str).str.strip().str.replace('.0', '', regex=False)
    return df

# Cargar el Excel
try:
    df = cargar_datos()

    # Input del usuario
    carnet_input = st.text_input("Número de Carnet:").strip()

    if carnet_input:
        # Buscar en el DataFrame
        resultado = df[df['Codigo'] == carnet_input]
        
        if not resultado.empty:
            nombre = resultado.iloc[0]['Persona']
            mesa = resultado.iloc[0]['Mesa']
            st.success(f"📍 Hola **{nombre}**, tu mesa asignada es la: **{mesa}**")
            st.balloons()
        else:
            st.error("⚠️ Carnet no encontrado. Revisa el número.")

except Exception as e:
    st.error(f"Error al cargar la base de datos: {e}")