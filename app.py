import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA CEI
st.set_page_config(page_title="Derma CEI v10", layout="centered")
st.markdown("<style>.stApp {background-color: #fff0f5;}</style>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #d81b60;'>CEI - Centro de Estética Integral</h1>", unsafe_allow_html=True)

# 2. CONEXIÓN (El cable crítico)
# Usamos un bloque try/except para que la app no muera si la llave falla
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # IMPORTANTE: Usamos el nombre exacto del modelo
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.warning("Aún no detecto la API KEY en los Secrets.")
except Exception as e:
    st.error(f"Error de configuración: {e}")

# 3. INTERFAZ PROFESIONAL
st.markdown("---")
opcion = st.radio("Fuente de imagen:", ["Cámara del móvil", "Subir foto de galería"], horizontal=True)

foto = None
if opcion == "Cámara del móvil":
    foto = st.camera_input("Capturá la piel")
else:
    foto = st.file_uploader("Subí el archivo", type=['jpg', 'png', 'jpeg'])

if foto:
    img = Image.open(foto)
    if opcion == "Subir foto de galería":
        st.image(img, width=400)
    
    if st.button("🚀 INICIAR DIAGNÓSTICO PROFESIONAL"):
        with st.spinner("Analizando tejido para el CEI..."):
            try:
                # El prompt técnico de Fabio
                prompt = "Analizá esta piel. Indicá Biotipo cutáneo y lesiones (comedones, pápulas, pústulas)."
                response = model.generate_content([prompt, img])
                st.markdown("### 📊 Informe Técnico")
                st.write(response.text)
            except Exception as e:
                st.error(f"Falla en el motor de IA: {e}")
                st.info("Revisá que la API KEY sea válida y no tenga espacios.")

st.markdown("---")
st.caption("Desarrollado por Fabio para CEI")
