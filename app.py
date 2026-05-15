import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA PROFESIONAL CEI
st.set_page_config(page_title="Derma CEI v12.3", layout="centered")

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

# --- EL LOGO REAL (POR URL EXTERNA) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Fabio, este link apunta DIRECTO a tu logo original
    url_logo_real = "https://storage.googleapis.com/generate-v1-assets-public/c1e2fc8a-2f16-4d2f-9cfc-0b4a22754602/logo%202.jpg"
    try:
        st.image(url_logo_real, use_container_width=True)
    except:
        st.markdown("<h1 style='text-align: center; color: #d81b60;'>CEI</h1>", unsafe_allow_html=True)

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
        st.warning("⚠️ Falta la API KEY en los Secrets de Streamlit.")
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
            with st.spinner("Analizando..."):
                res_piel = model.generate_content(["Actúa como experto del CEI. Analiza biotipo y lesiones.", img_piel])
                st.write(res_piel.text)
        
        with st.expander("👁️ Ver Protocolo (Clave Olga)"):
            pw = st.text_input("Contraseña de experto:", type="password")
            if pw == "Olga123":
                res_pax = model.generate_content(["Sugiere protocolo basado en activos (INCI) para esta piel.", img_piel])
                st.write(res_pax.text)
            elif pw:
                st.error("Clave incorrecta.")

else:
    st.markdown("<h2>🕵️ Inspector de Producto e INCI</h2>", unsafe_allow_html=True)
    foto_prod = st.camera_input("Enfocá marca o código de barras")
    if foto_prod:
        img_prod = Image.open(foto_prod)
        if st.button("🔍 AUDITORÍA TOTAL"):
            with st.spinner("Rastreando activos y precios..."):
                prompt_prod = (
                    "Analiza este producto: 1. Marca y nombre. 2. Lee código de barras. "
                    "3. Activos INCI. 4. Precio actual en Argentina. 5. Veredicto CEI."
                )
                response_prod = model.generate_content([prompt_prod, img_prod])
                st.write(response_prod.text)

st.markdown("---")
st.caption("v12.3 - Logo Real & Radar de Precios | Fabio para CEI")
