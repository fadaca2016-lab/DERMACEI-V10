import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import io

# 1. ESTÉTICA Y CONFIGURACIÓN (Derma CEI v12.8)
st.set_page_config(page_title="Derma CEI v12.8", layout="centered")

# Estilo "Pink CEI" para que Olga esté contenta
st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { 
        background-color: #ff69b4; color: white; 
        border-radius: 20px; width: 100%; border: none; font-weight: bold; height: 3.5em;
    }
    h1, h2 { color: #d81b60; text-align: center; font-family: 'Helvetica', sans-serif; }
    .stRadio > label { color: #ad1457; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- EL LOGO INYECTADO (BASE64) ---
# Fabio: Este bloque es el ADN de tu imagen. No necesita archivos externos.
# Si esto no muestra el logo, me retiro y me pongo a vender esponjas en el subte.
LOGO_DATA = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAEAAQADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZnaGlqc3R1dnd4eXqGhc49ICAnEAAC0QMCARIAAhEBAxEB/8QAPAAAAAABAwMCBAUDAgUDAgYDAAABAgADEQQSITFBEyJRYXEFMoGRoULB8BQjUrHR4fEGYnIVM0NTgpLS/9oADAMBAAIRAxEAPwD2SiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//Z"

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Mostramos el logo directamente desde el código inyectado
    st.markdown(f'<div style="display: flex; justify-content: center;"><img src="{LOGO_DATA}" width="200" style="border-radius: 10px;"></div>', unsafe_allow_html=True)

st.markdown("<h1>Centro de Estética Integral</h1>", unsafe_allow_html=True)

# 2. MOTOR IA (Gemini 1.5 Flash con Búsqueda Web)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[{'google_search_retrieval': {}}] 
        )
    else:
        st.warning("⚠️ Configurá la API KEY en los Secrets de Streamlit.")
except Exception as e:
    st.error(f"Error de conexión: {e}")

st.markdown("---")

# 3. INTERFAZ
modo = st.sidebar.radio("Misión:", ["Escáner de Piel (Rostro)", "Inspector de Producto (Precios/INCI)"])

if modo == "Escáner de Piel (Rostro)":
    st.markdown("<h2>Misión: Diagnóstico de Tejido</h2>", unsafe_allow_html=True)
    foto_piel = st.camera_input("Capturá el rostro")
    if foto_piel:
        img_piel = Image.open(foto_piel)
        if st.button("🚀 INICIAR DIAGNÓSTICO"):
            with st.spinner("Analizando para el CEI..."):
                res_piel = model.generate_content(["Actúa como experto del CEI. Analiza biotipo y lesiones. No sugieras protocolos.", img_piel])
                st.markdown("### 📊 Informe Técnico")
                st.write(res_piel.text)
        
        with st.expander("👁️ Ver Protocolo (Clave Olga)"):
            pw = st.text_input("Contraseña:", type="password")
            if pw == "Olga123":
                res_pax = model.generate_content(["Sugerí protocolo basado en activos INCI para esta piel.", img_piel])
                st.write(res_pax.text)

else:
    st.markdown("<h2>Misión: Inspector de Producto</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ad1457;'>Enfocá marca o código de barras</p>", unsafe_allow_html=True)
    foto_prod = st.camera_input("Escaneá el envase")
    if foto_prod:
        img_prod = Image.open(foto_prod)
        if st.button("🔍 AUDITORÍA TOTAL"):
            with st.spinner("Buscando activos y precios..."):
                prompt_prod = "Analiza marca, código de barras, activos INCI y busca precio actual en Argentina."
                response_prod = model.generate_content([prompt_prod, img_prod])
                st.markdown("### 📋 Informe de Auditoría")
                st.write(response_prod.text)

st.markdown("---")
st.caption("v12.8 - Logo Inyectado (Base64) | Fabio para CEI")
