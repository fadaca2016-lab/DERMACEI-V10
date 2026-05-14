import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración estética: Minimalista y Rosa Suave
st.set_page_config(page_title="Derma CEI v10", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { 
        background-color: #ff69b4; color: white; 
        border-radius: 20px; width: 100%; border: none;
    }
    h1 { color: #d81b60; text-align: center; font-family: 'Helvetica', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>CEI - Centro de Estética Integral</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ad1457;'>Escáner de Piel Inteligente v10</p>", unsafe_allow_html=True)

# Conexión con Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Falta configurar la API Key en los Secrets de Streamlit.")

# Entrada: Cámara (ideal para el móvil) o archivo
foto = st.camera_input("Capturá o subí la foto de la paciente")

if foto:
    img = Image.open(foto)
    if st.button("🚀 INICIAR DIAGNÓSTICO PROFESIONAL"):
        with st.spinner("Analizando tejido para el CEI..."):
            try:
                prompt = (
                    "Actúa como un experto cosmetólogo del CEI. "
                    "Analiza la piel en esta imagen y determina: "
                    "1. Biotipo cutáneo. 2. Presencia de comedones, pápulas o pústulas. "
                    "3. Sugerencia de protocolo técnico (ej. electroporación) sin marcas."
                )
                response = model.generate_content([prompt, img])
                st.markdown("### 📊 Resultado del Análisis")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error en el motor de IA: {e}")

st.markdown("---")
st.caption("Desarrollado por Fabio para CEI")
