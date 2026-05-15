import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA CEI PREMIUM
st.set_page_config(page_title="Derma CEI v11.8", layout="centered")

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

# Encabezado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        logo = Image.open("logo 2.jpg")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("<h1>CEI</h1>", unsafe_allow_html=True)

# 2. CONEXIÓN TÉCNICA (Búsqueda Web Habilitada)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[{'google_search_retrieval': {}}] 
        )
    else:
        st.warning("⚠️ Falta API KEY en Secrets.")
except Exception as e:
    st.error(f"Error técnico: {e}")

st.markdown("---")

# 3. INTERFAZ
modo = st.sidebar.radio("Misión:", ["Escáner de Piel", "Inspector de Producto (Foto/Barcode)"])

if modo == "Escáner de Piel":
    # ... (Mantenemos el bloque de piel igual para no romper lo que ya aprobó la jefa)
    st.markdown("<h2>Diagnóstico de Piel</h2>", unsafe_allow_html=True)
    foto_piel = st.camera_input("Rostro")
    if foto_piel:
        img_piel = Image.open(foto_piel)
        if st.button("🚀 INICIAR DIAGNÓSTICO"):
            res_piel = model.generate_content(["Analiza biotipo y lesiones.", img_piel])
            st.write(res_piel.text)
            
        with st.expander("👁️ Protocolo Oculto"):
            pw = st.text_input("Clave:", type="password")
            if pw == "Olga123":
                res_pax = model.generate_content(["Protocolo INCI.", img_piel])
                st.write(res_pax.text)

# NUEVA MISIÓN: INSPECTOR CON LECTURA DE CÓDIGO
else:
    st.markdown("<h2>🕵️ Inspector de Producto e INCI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ad1457;'>Sacale al frente, al INCI o al Código de Barras</p>", unsafe_allow_html=True)
    
    foto_prod = st.camera_input("Escaneá el producto")
    
    if foto_prod:
        img_prod = Image.open(foto_prod)
        st.image(img_prod, width=300)
        
        if st.button("🔍 AUDITORÍA TOTAL"):
            with st.spinner("Leyendo código de barras y analizando mercado..."):
                try:
                    prompt_prod = (
                        "Analiza minuciosamente la imagen de este producto cosmético: "
                        "1. CÓDIGO DE BARRAS: Si ves un código de barras o números EAN/UPC, leelos y usalos para identificar el producto exacto. "
                        "2. IDENTIFICACIÓN: Nombre, marca y procedencia. "
                        "3. ANÁLISIS INCI: Desglose de activos y seguridad química. "
                        "4. PRECIO EN ARGENTINA: Buscá el precio actual en Mercado Libre o farmacias locales. "
                        "5. VEREDICTO: ¿Es apto para el uso profesional en el CEI?"
                    )
                    response_prod = model.generate_content([prompt_prod, img_prod])
                    st.markdown("### 📋 Informe de Auditoría")
                    st.write(response_prod.text)
                except Exception as e:
                    st.error(f"Falla en la lectura: {e}")

st.markdown("---")
st.caption("v11.8 - Lector Óptico de Barcode & INCI | Fabio para CEI")
