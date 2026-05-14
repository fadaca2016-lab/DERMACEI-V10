import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA CEI (Fondo Rosa y Minimalismo)
st.set_page_config(page_title="Derma CEI v10", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { 
        background-color: #ff69b4; color: white; 
        border-radius: 20px; width: 100%; border: none; font-weight: bold;
    }
    h1 { color: #d81b60; text-align: center; font-family: 'Helvetica', sans-serif; }
    .stRadio > label { color: #ad1457; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>CEI - Centro de Estética Integral</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ad1457;'>Escáner de Piel Profesional v10.2</p>", unsafe_allow_html=True)

# 2. CONFIGURACIÓN DEL MOTOR (Con bypass de errores)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Intentamos con el nombre más directo para evitar el error de la imagen 767462.jpg
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Revisá la API Key en los Secrets.")

# 3. INTERFAZ DE CARGA
st.markdown("---")
opcion = st.radio("¿Cómo querés cargar la imagen?", ["Cámara del móvil", "Subir foto de galería"], horizontal=True)

foto = None
if opcion == "Cámara del móvil":
    foto = st.camera_input("Capturá la zona a analizar")
else:
    foto = st.file_uploader("Seleccioná la imagen", type=['jpg', 'png', 'jpeg'])

# 4. ANÁLISIS TÉCNICO
if foto:
    img = Image.open(foto)
    if opcion == "Subir foto de galería":
        st.image(img, width=400, caption="Imagen lista para el CEI")
    
    if st.button("🚀 INICIAR DIAGNÓSTICO PROFESIONAL"):
        with st.spinner("Analizando tejido..."):
            # El prompt de Fabio para sus clases
            prompt = (
                "Actúa como experto cosmetólogo del CEI. "
                "Analiza la piel en la imagen y determina: "
                "1. Biotipo cutáneo. 2. Mapa de lesiones. "
                "3. Sugerencia de protocolo técnico (ej. electroporación) sin marcas."
            )
            
            try:
                # Intento 1: Motor Flash (el rápido)
                response = model.generate_content([prompt, img])
                st.markdown("### 📊 Informe Técnico del CEI")
                st.write(response.text)
            except Exception as e:
                # Si falla el primero (como en la imagen 767462.jpg), saltamos al Pro
                try:
                    model_alt = genai.GenerativeModel('gemini-pro-vision')
                    response = model_alt.generate_content([prompt, img])
                    st.write(response.text)
                except Exception as e2:
                    st.error(f"Error persistente en Google: {e2}")
                    st.info("Fabio, esto es un problema de Google. Intentá un 'Reboot' en Manage App.")

st.markdown("---")
st.caption("Desarrollado por Fabio para CEI")
