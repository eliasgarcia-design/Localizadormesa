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
        
        # Juntamos TODO el diseño en una sola variable 'estilos'
        estilos = f'''
        <style>
        /* 1. EL FONDO (Capa de atrás) */
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* 2. EL CUADRO BLANCO (Capa de adelante) */
        /* Usamos !important para asegurar que el cuadro aparezca */
        [data-testid="stAppViewBlockContainer"] {{
            background-color: rgba(255, 255, 255, 0.90) !important;
            padding: 3rem !important;
            border-radius: 20px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
            margin-top: 2rem !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
        }}
        </style>
        '''
        # Aplicamos todo el diseño de una sola vez
        st.markdown(estilos, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error al cargar el diseño: {e}")
# 3. EJECUTAR DISEÑO
set_background('fondopagina.png') # <-- ASEGÚRATE QUE TENGA EL .JPG
st.markdown("""
    <style>
    /* Cambiar la fuente general a una más corporativa */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Estilo para el título principal */
    .titulo-pro {
        font-size: 32px !important;
        font-weight: 700;
        color: #201f1e;
        margin-bottom: 0px;
    }
    /* Estilo para las instrucciones */
    .instrucciones {
        font-size: 16px !important;
        color: #605e5c;
    }
    /* Hacer que el botón se vea más como el de la imagen */
    .stButton>button {
        background-color: #0078d4;
        color: white;
        border-radius: 2px;
        border: none;
        padding: 0.5rem 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("bluelogo.png", use_column_width=True)

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











