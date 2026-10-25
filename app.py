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
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ SAY AI")

# --- SELECTOR DE MODELOS DE GEMINI ---
model_options = {
    "Gemini 1.5 Flash (Rápido)": "gemini-1.5-flash",
    "Gemini 1.5 Pro (Avanzado)": "gemini-1.5-pro",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 2.0 Pro": "gemini-2.0-pro",
    "Gemini 2.5 Flash": "gemini-2.5-flash"
}

selected_model_name = st.selectbox(
    "MODELO ACTIVO SELECCIONADO:",
    list(model_options.keys())
)
selected_model_id = model_options[selected_model_name]

st.caption(f"🟢 **Estado:** Conectado a `{selected_model_id}`")

# Adjuntar imagen
uploaded_file = st.file_uploader("📂 Adjuntar imagen desde la galería", type=["png", "jpg", "jpeg"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)

# Entrada de texto del usuario
user_input = st.text_input("Escribe tu consulta a SAY AI...")

# --- OBTENER Y CONFIGURAR API KEY ---
api_keys = st.secrets.get("GEMINI_API_KEYS", [])

if not api_keys:
    st.warning("⚠️ No se encontró ninguna API Key configurada en los Secrets.")
else:
    if st.button("Enviar"):
        if not user_input and not image:
            st.warning("Por favor escribe una pregunta o adjunta una imagen.")
        else:
            success = False
            # Intentar con las claves disponibles
            for key in api_keys:
                try:
                    genai.configure(api_key=key)
                    model = genai.GenerativeModel(selected_model_id)
                    
                    with st.spinner("SAY AI está pensando..."):
                        if image:
                            response = model.generate_content([user_input, image] if user_input else [image])
                        else:
                            response = model.generate_content(user_input)
                            
                    st.success("Respuesta de SAY AI:")
                    st.write(response.text)
                    success = True
                    break
                except Exception as e:
                    continue
            
            if not success:
                st.error("❌ Ocurrió un error al procesar la solicitud. Verifica la validez de tus API Keys.")
                
