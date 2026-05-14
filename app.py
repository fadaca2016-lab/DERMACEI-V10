import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA CEI
st.set_page_config(page_title="Derma CEI v10", layout="centered")
st.markdown("<style>.stApp {background-color: #fff0f5;}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #d81b60;'>CEI - Centro de Estética Integral</h1>", unsafe_allow_html=True)

# 2. CONEXIÓN (Compatible con tu nueva llave 3.1)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Usamos el modelo que ya sabemos que acepta tu llave
        model = genai.GenerativeModel('models/gemini-1.5-flash')
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

# 4. PREVISUALIZACIÓN Y ANÁLISIS (Acá arreglamos lo que no se veía)
if foto:
    img = Image.open(foto)
    
    # ESTA ES LA LÍNEA QUE FALTABA: Muestra la foto en pantalla
    st.image(img, caption="Imagen cargada para el CEI", use_container_width=True)
    
    if st.button("🚀 INICIAR DIAGNÓSTICO PROFESIONAL"):
        with st.spinner("Analizando tejido para el CEI..."):
            try:
                # El enfoque de Fabio: Biotipos y Lesiones
                prompt = (
                    "Actúa como cosmetólogo experto del CEI. Analiza esta piel: "
                    "1. Determina Biotipo cutáneo. 2. Identifica lesiones. "
                    "3. Sugiere protocolo sin marcas comerciales."
                )
                response = model.generate_content([prompt, img])
                st.markdown("---")
                st.markdown("### 📊 Informe Técnico del CEI")
                st.write(response.text)
            except Exception as e:
                st.error(f"Falla técnica: {e}")

st.markdown("---")
st.caption("Desarrollado por Fabio para CEI")
