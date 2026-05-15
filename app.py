import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. CONFIGURACIÓN TÉCNICA Y ESTÉTICA (Derma CEI v12.6)
st.set_page_config(page_title="Derma CEI v12.6", layout="centered")

# Estilo "Pink CEI"
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

# --- CABECERA: EL LOGO REAL DEL CEI ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Fabio, este link apunta directo a tu logo de la silueta y la flor.
    # Usamos HTML puro para que no haya margen de error en la PC.
    logo_url = "https://storage.googleapis.com/generate-v1-assets-public/c1e2fc8a-2f16-4d2f-9cfc-0b4a22754602/logo%202.jpg"
    st.markdown(f'<img src="{logo_url}" style="width:100%; border-radius: 10px;">', unsafe_allow_html=True)

st.markdown("<h1>Centro de Estética Integral</h1>", unsafe_allow_html=True)

# 2. MOTOR DE IA (Gemini 1.5 Flash con Búsqueda Web)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[{'google_search_retrieval': {}}] 
        )
    else:
        st.warning("⚠️ Che Fabio, te falta la API KEY en los Secrets de Streamlit.")
except Exception as e:
    st.error(f"Error técnico en el motor: {e}")

st.markdown("---")

# 3. INTERFAZ DE USUARIO
modo = st.sidebar.radio("Seleccioná Misión:", ["Escáner de Piel (Rostro)", "Inspector de Producto (Precios/INCI)"])

# --- MISIÓN 1: ESCÁNER DE PIEL ---
if modo == "Escáner de Piel (Rostro)":
    st.markdown("<h2>Misión: Diagnóstico de Tejido</h2>", unsafe_allow_html=True)
    foto_piel = st.camera_input("Capturá el rostro de la paciente")
    
    if foto_piel:
        img_piel = Image.open(foto_piel)
        if st.button("🚀 INICIAR DIAGNÓSTICO"):
            with st.spinner("Analizando para el CEI..."):
                try:
                    prompt_piel = "Actúa como experto del CEI. Analiza esta piel: Biotipo y Lesiones. NO sugieras protocolos."
                    res_piel = model.generate_content([prompt_piel, img_piel])
                    st.markdown("### 📊 Informe Técnico")
                    st.write(res_piel.text)
                except Exception as e:
                    st.error(f"Falla: {e}")
            
            st.markdown("---")
            with st.expander("👁️ Ver Protocolo (Contraseña de Olga)"):
                pw = st.text_input("Clave de experto:", type="password")
                if pw == "Olga123":
                    res_pax = model.generate_content(["Sugiere protocolo basado en activos (INCI) para esta piel.", img_piel])
                    st.write(res_pax.text)
                elif pw:
                    st.error("Acceso denegado.")

# --- MISIÓN 2: INSPECTOR DE PRODUCTO ---
else:
    st.markdown("<h2>Misión: Inspector de Producto</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ad1457;'>Enfocá marca, código de barras o etiqueta INCI</p>", unsafe_allow_html=True)
    
    foto_prod = st.camera_input("Escaneá el producto")
    
    if foto_prod:
        img_prod = Image.open(foto_prod)
        if st.button("🔍 EJECUTAR AUDITORÍA TOTAL"):
            with st.spinner("Rastreando activos y precios en Argentina..."):
                try:
                    prompt_prod = (
                        "Analiza este producto cosmético: "
                        "1. Marca y producto exacto. "
                        "2. Lectura de código de barras (si se ve). "
                        "3. Análisis de activos INCI. "
                        "4. Precio actual aproximado en pesos argentinos. "
                        "5. Veredicto: ¿Es profesional o de uso masivo?"
                    )
                    response_prod = model.generate_content([prompt_prod, img_prod])
                    st.markdown("---")
                    st.markdown("### 📋 Informe de Auditoría")
                    st.write(response_prod.text)
                except Exception as e:
                    st.error(f"Falla en el rastreo: {e}")

st.markdown("---")
st.caption("v12.6 - Sistema de Inteligencia CEI | Fabio & Olga")
