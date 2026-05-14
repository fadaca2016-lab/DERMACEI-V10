import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA CEI
st.set_page_config(page_title="Derma CEI v10", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { 
        background-color: #ff69b4; color: white; 
        border-radius: 20px; width: 100%; border: none; font-weight: bold;
    }
    h1 { color: #d81b60; text-align: center; }
    .stRadio > label { color: #ad1457; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>CEI - Centro de Estética Integral</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ad1457;'>Escáner Profesional v10.2</p>", unsafe_allow_html=True)

# 2. CONEXIÓN (La clave para evitar el error de la imagen 7668fc.png)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Usamos la versión más estable para el diagnóstico de piel
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error en Secrets. Revisá la llave.")

# 3. INTERFAZ
st.markdown("---")
opcion = st.radio("Fuente de imagen:", ["Cámara del móvil", "Subir foto de galería"], horizontal=True)

foto = None
if opcion == "Cámara del móvil":
    foto = st.camera_input("Capturá la zona")
else:
    foto = st.file_uploader("Seleccioná el archivo", type=['jpg', 'png', 'jpeg'])

# 4. ANÁLISIS
if foto:
    img = Image.open(foto)
    if opcion == "Subir foto de galería":
        st.image(img, width=400)
    
    if st.button("🚀 INICIAR DIAGNÓSTICO PROFESIONAL"):
        with st.spinner("Analizando para el CEI..."):
            try:
                prompt = "Actúa como experto cosmetólogo del CEI. Determina Biotipo y lesiones (comedones, pápulas, pústulas)."
                response = model.generate_content([prompt, img])
                st.markdown("### 📊 Informe Técnico")
                st.write(response.text)
            except Exception as e:
                st.error(f"Falla en el motor de IA: {e}")

st.markdown("---")
st.caption("Desarrollado por Fabio para CEI")
