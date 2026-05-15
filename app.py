import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. ESTÉTICA PROFESIONAL CEI
st.set_page_config(page_title="Derma CEI v12.0", layout="centered")

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

# --- ARREGLO DEL LOGO (BLINDAJE TÉCNICO) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Fabio, acá el código busca el archivo de varias formas por si GitHub le cambió el nombre
    nombres_logo = ["logo 2.jpg", "logo_2.jpg", "logo2.jpg", "LOGO 2.JPG"]
    logo_final = None
    for n in nombres_logo:
        if os.path.exists(n):
            logo_final = n
            break
    
    if logo_final:
        st.image(logo_final, use_container_width=True)
    else:
        # Si no lo encuentra, ponemos un banner elegante para que no quede vacío
        st.markdown("<h2 style='text-align: center; color: #d81b60;'>CEI</h2>", unsafe_allow_html=True)

st.markdown("<h1>Centro de Estética Integral</h1>", unsafe_allow_html=True)

# 2. CONEXIÓN TÉCNICA (Con Búsqueda Web para Precios)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Usamos 1.5 Flash para que el radar de precios sea veloz
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[{'google_search_retrieval': {}}] 
        )
    else:
        st.warning("⚠️ Falta API KEY en los Secrets de Streamlit.")
except Exception as e:
    st.error(f"Error de conexión: {e}")

st.markdown("---")

# 3. INTERFAZ DUAL
modo = st.sidebar.radio("Seleccionar Misión:", ["Escáner de Piel (Rostro)", "Inspector de Producto (Precios/INCI)"])

# --- MISIÓN 1: DIAGNÓSTICO DE PIEL ---
if modo == "Escáner de Piel (Rostro)":
    st.markdown("<h2>Misión 1: Diagnóstico de Tejido</h2>", unsafe_allow_html=True)
    foto_piel = st.camera_input("Capturá el rostro")
    
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

# --- MISIÓN 2: INSPECTOR DE PRODUCTO (CÓDIGO DE BARRAS Y PRECIOS) ---
else:
    st.markdown("<h2>🕵️ Inspector de Producto e INCI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ad1457;'>Enfocá el código de barras o el frente del envase</p>", unsafe_allow_html=True)
    
    foto_prod = st.camera_input("Escaneá el producto")
    
    if foto_prod:
        img_prod = Image.open(foto_prod)
        st.image(img_prod, width=300, caption="Producto detectado")
        
        if st.button("🔍 AUDITORÍA TOTAL (INCI + PRECIO)"):
            with st.spinner("Rastreando código y precios en Argentina..."):
                try:
                    prompt_prod = (
                        "Analiza esta imagen de producto cosmético: "
                        "1. LECTURA ÓPTICA: Identifica código de barras (EAN/UPC) o nombre exacto. "
                        "2. ANÁLISIS INCI: Detalla activos principales y función. "
                        "3. RADAR DE PRECIOS: Busca el precio actual aproximado en pesos argentinos (Mercado Libre/Farmacias). "
                        "4. VEREDICTO: ¿Es apto para uso profesional en el CEI o es de uso masivo?"
                    )
                    response_prod = model.generate_content([prompt_prod, img_prod])
                    st.markdown("---")
                    st.markdown("### 📋 Informe de Auditoría de Mercado")
                    st.write(response_prod.text)
                except Exception as e:
                    st.error(f"Falla en el rastreo: {e}")

st.markdown("---")
st.caption("v12.0 - CEI Intelligence System | Fabio & Olga")
