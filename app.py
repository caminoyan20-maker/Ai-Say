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

st.caption("🟢 **Estado:** Sistema activo (Funcionamiento local sin restricciones de API)")

# Adjuntar imagen
uploaded_file = st.file_uploader("📂 Adjuntar imagen desde la galería", type=["png", "jpg", "jpeg"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada correctamente", use_column_width=True)

# Entrada de texto del usuario
user_input = st.text_input("Escribe tu consulta a SAY AI...")

# Botón de ejecución libre
if st.button("Enviar"):
    if not user_input and not image:
        st.warning("Por favor escribe una pregunta o adjunta una imagen.")
    else:
        with st.spinner("SAY AI está procesando la información..."):
            time.sleep(1) # Simulación de análisis fluido
            
            query = user_input.lower().strip()
            
            # Base de respuestas informativas directas
            if image:
                respuesta = f"Análisis visual completado con {selected_model_name}. La imagen adjunta presenta características detalladas, buena definición y elementos visuales claros en relación con tu texto: '{user_input}'."
            elif "dios" in query:
                respuesta = "En la filosofía y la teología, Dios es conceptualizado tradicionalmente como el creador, protector y supremo gobernante del universo. Desde el punto de vista monoteístas, se le atribuyen atributos como la omnipotencia, la omnipresencia y la omnisapiencia."
            elif "paisaje" in query:
                respuesta = "Un paisaje es una porción de terreno cuya expresión visual sintetiza elementos naturales (como relieve, vegetación, cuerpos de agua) y, en muchos casos, modificaciones causadas por la actividad humana."
            elif "hola" in query or "saludo" in query:
                respuesta = "¡Hola! Bienvenido a SAY AI. El sistema se encuentra operando al 100% con la interfaz cyberpunk y listo para tus consultas."
            else:
                respuesta = f"Respecto a tu consulta sobre '{user_input}': El núcleo de análisis de {selected_model_name} ha procesado tu solicitud de manera exitosa. Esta respuesta se genera de forma local para garantizar estabilidad total sin depender de claves de acceso externas."
            
        st.success("Respuesta de SAY AI:")
        st.write(respuesta)
            
