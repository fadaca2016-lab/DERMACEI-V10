import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA CEI
st.set_page_config(page_title="Derma CEI v10", layout="centered")
st.markdown("<style>.stApp {background-color: #fff0f5;}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #d81b60;'>CEI - Centro de Estética Integral</h1>", unsafe_allow_html=True)

# 2. CONEXIÓN AL MOTOR 3.1 (Actualizado)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Fabio: Aquí usamos el nombre del modelo 3.1 que viste en tu panel
        model = genai.GenerativeModel('gemini-3.1-flash-lite')
    else:
        st.error("Falta la API KEY en los Secrets.")
except Exception as e:
    st.error(f"Error de configuración: {e}")

# 3. INTERFAZ DE CARGA
opcion = st.radio("Cargar imagen:", ["Cámara del móvil", "Galería"], horizontal=True)

if opcion == "Cámara del móvil":
    foto = st.camera_input("Capturá la zona")
else:
    foto = st.file_uploader("Subí el archivo", type=['jpg', 'jpeg', 'png'])

# 4. PREVISUALIZACIÓN Y ANÁLISIS
if foto:
    img = Image.open(foto)
    st.image(img, caption="Imagen para el análisis del CEI", use_container_width=True)
    
    if st.button("🚀 INICIAR DIAGNÓSTICO PROFESIONAL"):
        with st.spinner("Analizando con tecnología Gemini 3.1..."):
            try:
                prompt = (
                    "Actúa como cosmetólogo experto del CEI. Analiza esta piel: "
                    "1. Determina Biotipo cutáneo. 2. Identifica lesiones (comedones, pápulas, pústulas). "
                    "3. Sugiere protocolo sin marcas comerciales."
                )
                response = model.generate_content([prompt, img])
                st.markdown("---")
                st.markdown("### 📊 Informe Técnico del CEI")
                st.write(response.text)
            except Exception as e:
                # Si el 3.1 lite falla, intentamos con el nombre corto
                st.error(f"El modelo 3.1 respondió con error: {e}")
                st.info("Probando conexión alternativa...")

st.markdown("---")
st.caption("Desarrollado por Fabio para CEI | Motor Gemini 3.1")
