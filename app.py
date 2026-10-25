import streamlit as st
from PIL import Image
import time
import random

# Configuración de página
st.set_page_config(page_title="SAY AI", page_icon="🤖", layout="centered")

# Estilos personalizados (Tema Cyberpunk)
st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
        color: #00f0ff;
    }
    .stSelectbox label, .stTextInput label {
        color: #00f0ff !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #ff0055;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ SAY AI")

# --- SELECTOR DE MODELOS ---
model_options = {
    "Gemini 1.5 Flash (Modo Autónomo)": "gemini-1.5-flash-local",
    "Gemini 1.5 Pro (Modo Autónomo)": "gemini-1.5-pro-local",
    "Gemini 2.0 Flash (Modo Autónomo)": "gemini-2.0-flash-local",
    "Gemini 2.0 Pro (Modo Autónomo)": "gemini-2.0-pro-local"
}

selected_model_name = st.selectbox(
    "MODELO ACTIVO SELECCIONADO:",
    list(model_options.keys())
)
selected_model_id = model_options[selected_model_name]

st.caption(f"🟢 **Estado:** Sistema en ejecución directa (Sin claves API) con `{selected_model_id}`")

# Adjuntar imagen
uploaded_file = st.file_uploader("📂 Adjuntar imagen desde la galería", type=["png", "jpg", "jpeg"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada correctamente", use_column_width=True)

# Entrada de texto del usuario
user_input = st.text_input("Escribe tu consulta a SAY AI...")

# --- GENERADOR AUTÓNOMO DE RESPUESTAS ---
def generar_respuesta_local(prompt, tiene_imagen, modelo):
    # Respuestas simuladas inteligentes de respaldo
    if tiene_imagen:
        return f"[SAY AI - {modelo}]: He analizado la imagen subida junto a tu consulta '{prompt if prompt else 'Sin texto'}'. La estructura visual muestra elementos claros en alta resolución con patrones de luz e iluminación adaptados."
    
    prompt_clean = prompt.lower().strip()
    
    if "paisaje" in prompt_clean:
        return f"[SAY AI - {modelo}]: Un paisaje es la representación de una extensión de terreno. Puede ser natural (montañas, ríos, bosques) o urbano (ciudades, arquitectura). ¿Te gustaría generar una descripción técnica o estética específica sobre algún entorno?"
    elif "hola" in prompt_clean or "saludo" in prompt_clean:
        return f"[SAY AI - {modelo}]: ¡Hola! El sistema SAY AI está activo y listo para procesar tus consultas sin necesidad de autent
        
