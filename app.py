import streamlit as st
import google.generativeai as genai
from PIL import Image

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
    "Gemini 1.5 Flash (Rápido)": "gemini-1.5-flash",
    "Gemini 1.5 Pro (Avanzado)": "gemini-1.5-pro",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 2.0 Pro": "gemini-2.0-pro"
}

selected_model_name = st.selectbox(
    "MODELO ACTIVO SELECCIONADO:",
    list(model_options.keys())
)
selected_model_id = model_options[selected_model_name]

# Adjuntar imagen
uploaded_file = st.file_uploader("📂 Adjuntar imagen desde la galería", type=["png", "jpg", "jpeg"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)

# Entrada de texto del usuario
user_input = st.text_input("Escribe tu consulta a SAY AI...")

# Base de conocimientos local ampliada para preguntas frecuentes en caso de no usar API
conocimiento_base = {
    "dios": "En las religiones monoteístas, Dios es considerado el creador y supreme ser del universo, omnipotente, omnipresente y omnisciente. Filosóficamente, suele definirse como el primer motor inmune o la causa primigenia de la existencia.",
    "paisaje": "Un paisaje es una extensión de terreno cuyos elementos visuales reflejan características naturales o la intervención humana (urbano, rural, natural).",
    "hola": "¡Hola! SAY AI está en línea. ¿Sobre qué tema te gustaría obtener información hoy?"
}

if st.button("Enviar"):
    if not user_input and not image:
        st.warning("Por favor escribe una pregunta o adjunta una imagen.")
    else:
        with st.spinner("SAY AI está analizando tu consulta..."):
            respuesta = None
            
            # Intentar usar la API oficial si hay alguna clave configurada en los Secrets
            api_keys = st.secrets.get("GEMINI_API_KEYS", [])
            for key in api_keys:
                if key and not key.startswith("AQ."): # Si es clave válida de AI Studio
                    try:
                        genai.configure(api_key=key)
                        model = genai.GenerativeModel(selected_model_id)
                        if image:
                            res = model.generate_content([user_input, image] if user_input else [image])
                        else:
                            res = model.generate_content(user_input)
                        respuesta = res.text
                        break
                    except:
                        continue
            
            # Si no hay clave válida o falló, usar búsqueda inteligente en la base local o sintetizar
            if not respuesta:
                query_lower = user_input.lower()
                for keyword, desc in conocimiento_base.items():
                    if keyword in query_lower:
                        respuesta = desc
                        break
                
                if not respuesta:
                    respuesta = f"Has consultado sobre: '{user_input}'. Para obtener respuestas de inteligencia artificial generativa en tiempo real para cualquier pregunta compleja, asegúrate de colocar una clave de API de AI Studio válida (que comience por AIzaSy...) en los Secrets de Streamlit. Mientras tanto, el sistema opera con respuestas directas."

        st.success("Respuesta de SAY AI:")
        st.write(respuesta)
    
