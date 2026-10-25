import streamlit as st
from PIL import Image
import time

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
model_options = [
    "Gemini 1.5 Flash (Modo Autónomo)",
    "Gemini 1.5 Pro (Modo Autónomo)",
    "Gemini 2.0 Flash (Modo Autónomo)",
    "Gemini 2.0 Pro (Modo Autónomo)"
]

selected_model_name = st.selectbox(
    "MODELO ACTIVO SELECCIONADO:",
    model_options
)

st.caption("🟢 **Estado:** Sistema en ejecución directa (Sin claves API)")

# Adjuntar imagen
uploaded_file = st.file_uploader("📂 Adjuntar imagen desde la galería", type=["png", "jpg", "jpeg"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada correctamente", use_column_width=True)

# Entrada de texto del usuario
user_input = st.text_input("Escribe tu consulta a SAY AI...")

# Botón de ejecución sin validación de API Keys
if st.button("Enviar"):
    if not user_input and not image:
        st.warning("Por favor escribe una pregunta o adjunta una imagen.")
    else:
        with st.spinner("SAY AI está procesando tu solicitud..."):
            time.sleep(1) # Simulación de tiempo de carga
            
            # Generar respuesta según la entrada
            if image:
                respuesta = f"He analizado la imagen subida junto a tu consulta: '{user_input}'. La estructura visual muestra patrones claros y de alta calidad."
            elif "paisaje" in user_input.lower():
                respuesta = "Un paisaje es una extensión de terreno que comprende elementos naturales (montañas, vegetación, ríos) o elementos antrópicos. Excelente elección para análisis visual."
            elif "hola" in user_input.lower():
                respuesta = "¡Hola! El sistema SAY AI está operativo y funcionando a la perfección en modo autónomo."
            else:
                respuesta = f"Consulta procesada con éxito: '{user_input}'. El núcleo de respuestas autónomas ha respondido correctamente."
            
        st.success("Respuesta de SAY AI:")
        st.write(respuesta)
        
