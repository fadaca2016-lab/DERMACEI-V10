import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA PROFESIONAL CEI
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

# 2. CONEXIÓN TÉCNICA (Ajustada para Fabio)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Usamos el nombre base para máxima compatibilidad
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.warning("⚠️ Configurá la nueva API KEY en los Secrets de Streamlit.")
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

# 4. ANÁLISIS TÉCNICO
if foto:
    img = Image.open(foto)
    if opcion == "Subir foto de galería":
        st.image(img, width=400, caption="Imagen cargada correctamente")
    
    if st.button("🚀 INICIAR DIAGNÓSTICO PROFESIONAL"):
        with st.spinner("Analizando tejido con tecnología Gemini..."):
            try:
                # El prompt con el enfoque del CEI (Principios activos > Marcas)
                prompt = (
                    "Actúa como un experto cosmetólogo del CEI. "
                    "Analiza minuciosamente la piel en esta imagen y determina: "
                    "1. Biotipo cutáneo (Eudérmica, Grasa, Seca, Mixta). "
                    "2. Mapa de lesiones (Comedones, pápulas, pústulas). "
                    "3. Sugerencia de protocolo técnico (ej. electroporación) sin mencionar marcas comerciales."
                )
                
                response = model.generate_content([prompt, img])
                
                st.markdown("---")
                st.markdown("### 📊 Informe Técnico del CEI")
                st.write(response.text)
                st.success("Análisis finalizado con éxito.")
                
            except Exception as e:
                st.error(f"Falla en el motor de IA: {e}")
                st.info("Fabio, revisá que la API KEY sea la que generaste recién para Gemini Flash.")

st.markdown("---")
st.caption("Desarrollado por Fabio para CEI")
