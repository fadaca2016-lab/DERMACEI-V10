import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA PROFESIONAL CEI
st.set_page_config(page_title="Derma CEI v11.9", layout="centered")

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

# Encabezado con Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        # Usamos el logo que subiste
        logo = Image.open("logo 2.jpg")
        st.image(logo, use_container_width=True)
    except:
        st.markdown("<h1>CEI</h1>", unsafe_allow_html=True)

st.markdown("<h1>Centro de Estética Integral</h1>", unsafe_allow_html=True)

# 2. CONEXIÓN TÉCNICA (Con Búsqueda Web para Precios)
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

# 3. INTERFAZ DUAL
modo = st.sidebar.radio("Seleccionar Misión:", ["Escáner de Piel (Rostro)", "Inspector de Producto (Foto/Barcode)"])

# --- MISIÓN 1: DIAGNÓSTICO DE PIEL ---
if modo == "Escáner de Piel (Rostro)":
    st.markdown("<h2>Misión 1: Diagnóstico de Tejido</h2>", unsafe_allow_html=True)
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
            with st.expander("👁️ Zona de Experto: Ver Protocolo Sugerido"):
                st.info("⚠️ Esta sección requiere autorización de Olga.")
                pw = st.text_input("Clave de experto:", type="password")
                if pw == "Olga123":
                    res_pax = model.generate_content(["Sugiere un protocolo basado en activos (INCI) para esta piel.", img_piel])
                    st.write(res_pax.text)
                elif pw:
                    st.error("Acceso denegado.")

# --- MISIÓN 2: INSPECTOR DE PRODUCTO (LO QUE AGREGAMOS RECIÉN) ---
else:
    st.markdown("<h2>🕵️ Inspector de Producto e INCI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ad1457;'>Enfocá bien el código de barras o la marca</p>", unsafe_allow_html=True)
    
    foto_prod = st.camera_input("Escaneá el producto")
    
    if foto_prod:
        img_prod = Image.open(foto_prod)
        st.image(img_prod, width=300, caption="Producto detectado")
        
        if st.button("🔍 EJECUTAR AUDITORÍA TOTAL"):
            with st.spinner("Decodificando código y buscando precios..."):
                try:
                    prompt_prod = (
                        "Analiza minuciosamente este producto cosmético de la imagen: "
                        "1. LECTURA DE CÓDIGO: Lee el código de barras (EAN/UPC) si es visible. "
                        "2. IDENTIFICACIÓN: Nombre exacto del producto y marca. "
                        "3. ANÁLISIS TÉCNICO: Detalla los principios activos (INCI) y su función. "
                        "4. PRECIO EN ARGENTINA: Busca el precio actual aproximado en el mercado local. "
                        "5. VEREDICTO CEI: ¿Es un producto apto para nivel profesional o uso hogareño?"
                    )
                    response_prod = model.generate_content([prompt_prod, img_prod])
                    st.markdown("---")
                    st.markdown("### 📋 Informe de Auditoría")
                    st.write(response_prod.text)
                except Exception as e:
                    st.error(f"Falla en el rastreo: {e}")

st.markdown("---")
st.caption("v11.9 - Sistema de Inteligencia CEI | Fabio & Olga")
