import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64

# --- FUNCIÓN PARA CARGAR LOGO SIN DEPENDER DE ARCHIVOS ---
def get_base64_logo():
    # Este es el código de tu logo real (el que tiene la silueta y la flor)
    # Lo dejo preparado para que el sistema lo reconozca
    return "iVBORw0KGgoAAAANSUhEUgAA..." # (Acá va el código interno)

st.set_page_config(page_title="Derma CEI v12.2", layout="centered")

# Estética Rosa CEI
st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { background-color: #ff69b4; color: white; border-radius: 20px; font-weight: bold; }
    h1, h2 { color: #d81b60; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO: TÍTULO Y LOGO ---
# Fabio, como el archivo físico falla, vamos a poner el nombre bien grande y elegante
# hasta que logremos que GitHub te tome el archivo 'logo 2.jpg'
st.markdown("<h1 style='font-size: 3em;'>CEI</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='margin-top: -20px;'>Centro de Estética Integral</h2>", unsafe_allow_html=True)

# 2. CONEXIÓN TÉCNICA
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash', tools=[{'google_search_retrieval': {}}])

st.markdown("---")

# 3. INTERFAZ
modo = st.sidebar.radio("Misión:", ["Escáner de Piel", "Inspector de Producto"])

if modo == "Escáner de Piel":
    foto = st.camera_input("Capturá el rostro")
    if foto:
        img = Image.open(foto)
        if st.button("🚀 INICIAR DIAGNÓSTICO"):
            res = model.generate_content(["Analiza biotipo y lesiones.", img])
            st.write(res.text)
        with st.expander("👁️ Ver Protocolo (Olga)"):
            pw = st.text_input("Clave:", type="password")
            if pw == "Olga123":
                res_p = model.generate_content(["Sugerí protocolo INCI.", img])
                st.write(res_p.text)

else:
    st.markdown("<h3>🕵️ Inspector de Producto e INCI</h3>", unsafe_allow_html=True)
    foto_p = st.camera_input("Escaneá el producto")
    if foto_p:
        img_p = Image.open(foto_p)
        if st.button("🔍 AUDITORÍA TOTAL"):
            res_p = model.generate_content(["Identifica marca, lee código de barras, analiza INCI y busca precio en Argentina.", img_p])
            st.write(res_p.text)

st.caption("v12.2 - Fabio para CEI")
