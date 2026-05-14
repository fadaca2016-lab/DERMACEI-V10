import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURACIÓN ESTÉTICA (Minimalismo Rosa CEI)
st.set_page_config(page_title="Derma CEI v10", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #fff0f5; /* Rosa suave */
    }
    .stButton>button {
        background-color: #ff69b4;
        color: white;
        border-radius: 20px;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    h1 {
        color: #d81b60;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
    }
    .stRadio > label {
        color: #ad1457;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO
st.markdown("<h1>CEI - Centro de Estética Integral</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ad1457;'>Escáner de Piel Profesional v10</p>", unsafe_allow_html=True)

# 3. CONEXIÓN TÉCNICA CON EL CEREBRO (IA)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error: Revisá la API Key en los Secrets de Streamlit.")

# 4. INTERFAZ HÍBRIDA (Cámara o Archivo)
st.markdown("---")
opcion = st.radio("¿Cómo querés cargar la imagen?", ["Cámara del móvil", "Subir foto de galería"], horizontal=True)

foto = None
if opcion == "Cámara del móvil":
    foto = st.camera_input("Capturá la zona a analizar")
else:
    foto = st.file_uploader("Seleccioná la imagen (110kb es ideal)", type=['jpg', 'png', 'jpeg'])

# 5. PROCESAMIENTO Y ANÁLISIS
if foto:
    img = Image.open(foto)
    
    # Si es archivo, mostramos una previa (la cámara ya tiene la suya)
    if opcion == "Subir foto de galería":
        st.image(img, width=400, caption="Imagen cargada correctamente")
    
    if st.button("🚀 INICIAR DIAGNÓSTICO PROFESIONAL"):
        with st.spinner("Analizando tejido para el CEI..."):
            try:
                # Prompt con enfoque técnico del CEI
                prompt = (
                    "Actúa como un experto cosmetólogo del CEI. "
                    "Analiza minuciosamente la piel en esta imagen y determina: "
                    "1. Biotipo cutáneo (Eudérmica, Grasa, Seca, Mixta). "
                    "2. Mapa de lesiones (Comedones, pápulas, pústulas). "
                    "3. Sugerencia de protocolo técnico (ej. electroporación, mesoterapia virtual) sin mencionar marcas comerciales."
                )
                
                response = model.generate_content([prompt, img])
                
                st.markdown("---")
                st.markdown("### 📊 Informe Técnico del CEI")
                st.write(response.text)
                st.success("Análisis finalizado con éxito.")
                
            except Exception as e:
                st.error(f"El motor técnico falló: {e}")

# PIE DE PÁGINA
st.markdown("---")
st.caption("Sistema de Diagnóstico Digital | Desarrollado por Fabio para CEI")
