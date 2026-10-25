import streamlit as st
import requests
import json
from PIL import Image
import base64
import io

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
    "Gemini 2.0 Pro": "gemini-2.0-pro"
}

selected_model_name = st.selectbox(
    "MODELO ACTIVO SELECCIONADO:",
    list(model_options.keys())
)
selected_model_id = model_options[selected_model_name]

st.caption(f"🟢 **Estado:** Conectado mediante Token a `{selected_model_id}`")

# Adjuntar imagen
uploaded_file = st.file_uploader("📂 Adjuntar imagen desde la galería", type=["png", "jpg", "jpeg"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)

# Entrada de texto del usuario
user_input = st.text_input("Escribe tu consulta a SAY AI...")

# --- OBTENER Y CONFIGURAR CREDENCIALES ---
api_keys = st.secrets.get("GEMINI_API_KEYS", [])

if not api_keys:
    st.warning("⚠️ No se encontró ninguna credencial configurada en los Secrets.")
else:
    if st.button("Enviar"):
        if not user_input and not image:
            st.warning("Por favor escribe una pregunta o adjunta una imagen.")
        else:
            token = api_keys[0]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{selected_model_id}:generateContent"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Construcción de la carga útil (payload)
            parts = []
            if user_input:
                parts.append({"text": user_input})
            
            if image:
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_str
                    }
                })
            
            payload = {
                "contents": [{
                    "parts": parts
                }]
            }
            
            with st.spinner("SAY AI está procesando tu solicitud..."):
                try:
                    response = requests.post(url, headers=headers, json=payload)
                    
                    if response.status_code == 200:
                        res_json = response.json()
                        candidates = res_json.get("candidates", [])
                        if candidates:
                            content = candidates[0].get("content", {})
                            parts_res = content.get("parts", [])
                            text_output = "".join([p.get("text", "") for p in parts_res])
                            st.success("Respuesta de SAY AI:")
                            st.write(text_output)
                        else:
                            st.error("⚠️ La API respondió pero no se encontraron resultados válidos.")
                    else:
                        st.error(f"❌ Error de autenticación o servidor ({response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"❌ Error al conectar con la API: {e}")
    
