import streamlit as st
import pandas as pd
import base64

# 1. CONFIGURACIÓN (Debe ser lo primero)
st.set_page_config(page_title="Localizador de Mesas", page_icon="bluelogo.png", layout="centered")

# 2. FUNCIÓN DE FONDO CON CACHÉ (Para evitar el loop de carga)
@st.cache_data
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(file_name):
    try:
        bin_str = get_base64(file_name)
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 3rem;
            border-radius: 20px;
            margin-top: 2rem;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"No se pudo cargar la imagen: {file_name}. Revisa que el nombre sea idéntico en GitHub.")

# 3. EJECUTAR DISEÑO
set_background('fondopagina.png') # <-- ASEGÚRATE QUE TENGA EL .JPG
st.image("bluelogo.png", width=200)
st.title("Localizador de Mesas")
st.write("Ingresa tu ID para conocer tu ubicación.")

# 4. LÓGICA DE BÚSQUEDA
try:
    df = pd.read_excel("invitados prueba.xlsx")
    id_empleado = st.text_input("ID de Empleado (Ej: E12345)").strip()

    if id_empleado:
        # Buscamos en la columna 'Codigo'
        resultado = df[df['ID EMP'].astype(str).str.upper() == id_empleado.upper()]

        if not resultado.empty:
            nombre = resultado.iloc[0]['Invitado']
            mesa = resultado.iloc[0]['Mesa']
            
            st.success(f"### ¡Hola, {nombre}!")
            
            # Lógica de laptops (agrega tus IDs aquí)
            laptops = ["E11111", "E22222"] 
            
            if id_empleado.upper() in laptops:
                st.info(f"Tu mesa es la **{mesa}**. Has sido elegido para **traer tu laptop:**.")
            else:
                st.info(f"Tu mesa asignada es la **{mesa}**.")
        else:
            st.error("ID no encontrado. Por favor, verifica con Recursos Humanos.")

except Exception as e:
    st.error(f"Error técnico: {e}")






