import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA PROFESIONAL CEI (Minimalismo Rosa)
st.set_page_config(page_title="Derma CEI v10", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { 
        background-color: #ff69b4; color: white; 
        border-radius: 20px; width: 100%; border: none; font-weight: bold; height: 3em;
    }
    h1 { color: #d81b60; text-align: center; font-family: 'Helvetica', sans-serif; }
    .stRadio > label { color: #ad1457; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>CEI - Centro de Estética Integral</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ad1457;'>Escáner de Piel Inteligente v10.4</p>", unsafe_allow_html=True)

# 2. CONEXIÓN TÉCNICA (Compatible con Gemini 1.5 y 3.1)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 'gemini-1.5-flash-latest' es la llave maestra para los modelos nuevos
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    else:
        st.warning("⚠️ Fabio, configurá la nueva API KEY en los Secrets de Streamlit.")
except Exception as e:
    st.error(f"Error de configuración: {e}")

# 3. INTERFAZ HÍBRIDA
st.markdown("---")
opcion = st.radio("¿Cómo querés cargar la imagen?", ["Cámara del móvil", "Subir foto de galería"], horizontal=True)

foto = None
if opcion == "Cámara del móvil":
    foto = st.camera_input("Capturá la zona a analizar")
else:
    foto = st.file_uploader("Seleccioná la imagen de la galería", type=['jpg', 'png', 'jpeg'])

# 4. PROCESAMIENTO Y ANÁLISIS DEL CEI
if foto:
    img = Image.open(foto)
    if opcion == "Subir foto de galería":
        st.image(img, width=400, caption="Imagen cargada correctamente")
    
    if st.button("🚀 INICIAR DIAGNÓSTICO PROFESIONAL"):
        with st.spinner("Analizando tejido con tecnología Gemini..."):
            try:
                # Prompt con el enfoque pedagógico de Fabio
                prompt = (
                    "Actúa como un experto cosmetólogo del CEI. "
                    "Analiza minuciosamente la piel en esta imagen y determina: "
                    "1. Biotipo cutáneo (Eudérmica, Grasa, Seca, Mixta). "
                    "2. Mapa de lesiones (Comedones, pápulas, pústulas). "
                    "3. Sugerencia de protocolo técnico sin mencionar marcas comerciales."
                )
                
                response = model.generate_content([prompt, img])
                
                st.markdown("---")
                st.markdown("### 📊 Informe Técnico del CEI")
                st.write(response.text)
                st.success("Análisis finalizado con éxito.")
                
            except Exception as e:
                st.error(f"Falla en el motor de IA: {e}")
                st.info("Asegurate de que la API KEY sea la correcta para el modelo Flash.")

# PIE DE PÁGINA
st.markdown("---")
st.caption("Sistema de Diagnóstico Digital | Desarrollado por Fabio para CEI")
