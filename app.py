import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO

# 1. ESTÉTICA PROFESIONAL CEI
st.set_page_config(page_title="Derma CEI v12.1", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { 
        background-color: #ff69b4; color: white; 
        border-radius: 20px; width: 100%; border: none; font-weight: bold; height: 3.5em;
    }
    h1, h2 { color: #d81b60; text-align: center; font-family: 'Helvetica', sans-serif; }
    .stRadio > label { color: #ad1457; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO CON LOGO POR URL (PARA QUE NO FALLE) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Fabio, acá le puse el link directo a la imagen que me mandaste
    # Esto es infalible porque ya no depende de tu GitHub
    url_logo = "https://storage.googleapis.com/generate-v1-assets-public/fd20a627-4afd-4b62-894b-bf50fc16eb2a/logo%202.jpg"
    try:
        st.image(url_logo, use_container_width=True)
    except:
        st.markdown("<h2 style='text-align: center; color: #d81b60;'>CEI</h2>", unsafe_allow_html=True)

st.markdown("<h1>Centro de Estética Integral</h1>", unsafe_allow_html=True)

# 2. CONEXIÓN TÉCNICA
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[{'google_search_retrieval': {}}] 
        )
    else:
        st.warning("⚠️ Falta API KEY en los Secrets.")
except Exception as e:
    st.error(f"Error de conexión: {e}")

st.markdown("---")

# 3. INTERFAZ
modo = st.sidebar.radio("Misión:", ["Escáner de Piel", "Inspector de Producto (Barcode/INCI)"])

if modo == "Escáner de Piel":
    st.markdown("<h2>Diagnóstico de Rostro</h2>", unsafe_allow_html=True)
    foto_piel = st.camera_input("Capturá el rostro")
    if foto_piel:
        img_piel = Image.open(foto_piel)
        if st.button("🚀 INICIAR DIAGNÓSTICO"):
            res_piel = model.generate_content(["Analiza biotipo y lesiones.", img_piel])
            st.write(res_piel.text)
        with st.expander("👁️ Ver Protocolo (Clave Olga)"):
            pw = st.text_input("Contraseña:", type="password")
            if pw == "Olga123":
                res_pax = model.generate_content(["Sugerí protocolo INCI.", img_piel])
                st.write(res_pax.text)

else:
    st.markdown("<h2>🕵️ Inspector de Producto</h2>", unsafe_allow_html=True)
    foto_prod = st.camera_input("Enfocá marca o código de barras")
    if foto_prod:
        img_prod = Image.open(foto_prod)
        if st.button("🔍 AUDITORÍA TOTAL"):
            prompt_prod = (
                "1. Identifica marca y producto. "
                "2. Lee código de barras si existe. "
                "3. Analiza activos INCI. "
                "4. Busca precio aproximado en Argentina. "
                "5. Da veredicto para el CEI."
            )
            response_prod = model.generate_content([prompt_prod, img_prod])
            st.write(response_prod.text)

st.markdown("---")
st.caption("v12.1 - Radar de Precios & Logo Blindado | Fabio para CEI")
