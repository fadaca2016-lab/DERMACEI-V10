import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA CEI
st.set_page_config(page_title="Derma CEI v10", layout="centered")
st.markdown("<style>.stApp {background-color: #fff0f5;}</style>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #d81b60;'>CEI - Centro de Estética Integral</h1>", unsafe_allow_html=True)

# 2. CONEXIÓN (Versión Estable)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # En esta versión de librería usamos el nombre directo
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.warning("Configurá la API KEY en los Secrets.")
except Exception as e:
    st.error(f"Error de inicio: {e}")

# 3. INTERFAZ
opcion = st.radio("Cargar imagen:", ["Cámara del móvil", "Galería"], horizontal=True)
foto = st.camera_input("Capturá la zona") if opcion == "Cámara del móvil" else st.file_uploader("Subí el archivo", type=['jpg', 'jpeg', 'png'])

if foto:
    img = Image.open(foto)
    if st.button("🚀 INICIAR DIAGNÓSTICO PROFESIONAL"):
        with st.spinner("Analizando tejido para el CEI..."):
            try:
                prompt = "Analiza esta piel. Indica Biotipo cutáneo y lesiones (comedones, pápulas, pústulas)."
                response = model.generate_content([prompt, img])
                st.markdown("### 📊 Informe Técnico del CEI")
                st.write(response.text)
            except Exception as e:
                st.error(f"Falla técnica: {e}")

st.markdown("---")
st.caption("Desarrollado por Fabio para CEI")
