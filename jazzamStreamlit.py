import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configurar API Key desde Secrets de Streamlit
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Initializar modelo
model = genai.GenerativeModel("gemini-1.5-flash")

# App UI
st.set_page_config(page_title="Jazzam - Asistente Virtual", page_icon="🎷")

# UI styling
st.markdown(
    """
    <style>
    .main-container {
        display: flex;
        align-items: center;
        height: 80vh;
    }

    .card {
        background-color: #111;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    .center-title {
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .center-sub {
        text-align: center;
        color: #aaa;
        margin-bottom: 1.5rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: 600;
    }

    .fade-in {
    animation: fadeIn 0.6s ease-in;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }

    .result-card {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1.5rem;
        border: 1px solid #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Context
def generar_recomendacion(artists: list) -> str:
    try:
        context = """
Sos Jazzam, un asistente musical de Buenos Aires.

Tu tarea:
- Recibir 1 o 2 artistas o álbumes del usuario
- Recomendar UN álbum de John Coltrane similar en estilo
- Elegir solo entre:
Blue Train, Stardust, Giant Steps, Ballads, My Favorite Things,
John Coltrane and Johnny Hartman, A Love Supreme, Meditations, Ascension

Formato de respuesta:
- 2 párrafos breves
- Primer párrafo: recomendación directa
- Segundo párrafo: justificación

Estilo:
- Español rioplatense (voseo)
- Tono cálido y natural
- Conciso (sin relleno)
"""

        user_prompt = f"""
        Mis artistas o álbumes favoritos son: {', '.join(artists)}.
        Recomendame un álbum de Coltrane similar.
        """

        full_prompt = f"{context}\n\n{user_prompt}"

        response = model.generate_content(
            full_prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 300
            }
        )

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()
        else:
            return "Perdón, no pude generar una recomendación en este momento. Intentá de nuevo!"

    except Exception:
        return "Ocurrió un error al generar la recomendación. Probá nuevamente."

# Inicializamos Historial

if "historial" not in st.session_state:
    st.session_state.historial = []

if "resultado" not in st.session_state:
    st.session_state.resultado = None


# Cuerpo de la App
st.markdown('<div class="main-container card">', unsafe_allow_html=True)

st.markdown('<h1 class="center-title">🎷 Jazzam</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="center-sub">Ingresá uno o dos artistas o álbumes y recibí una recomendación de Coltrane.</p>',
    unsafe_allow_html=True
)

user_input = st.text_input(
"Artistas o álbumes  (separados por coma)",
placeholder="Ej: Miles Davis, Bill Evans",
key="input_artistas"
)

if "historial" not in st.session_state:
    st.session_state.historial = []


artists_list = [a.strip() for a in user_input.split(",") if a.strip()]
is_valid = 0 < len(artists_list) <= 2

if user_input and not is_valid:
    st.warning("Máximo dos artistas/álbumes separados por coma.")

if st.button("Recomendar", disabled=not is_valid):
    if user_input:
        artists = artists_list

        if len(artists) == 0 or len(artists) > 2:
            st.warning("Por favor ingresá uno o dos artistas/álbumes.")
        else:
            with st.spinner("Generando recomendación..."):
                resultado = generar_recomendacion(artists)
                st.session_state.resultado = resultado
                nuevo_item = {
                    "input": artists,
                    "output": resultado
                }
                if not st.session_state.historial or st.session_state.historial[0] != nuevo_item:
                    st.session_state.historial.insert(0, nuevo_item)
                st.session_state.input_artistas = ""


if "resultado" in st.session_state:
    st.markdown('<div class="result-card fade-in">', unsafe_allow_html=True)
    st.markdown("### Recomendación")
    st.write(st.session_state.resultado)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    if "resultado" not in st.session_state and user_input:
        st.warning("Ingresá al menos un artista o álbum.")

st.markdown('</div>', unsafe_allow_html=True)

# Sidebar - Historial e Imagen
with st.sidebar:
    try:
        image = Image.open("coltrane.jpg")
        st.image(image, caption="John Coltrane", use_container_width=True)
    except Exception:
        st.write("Imagen no disponible")
    st.markdown("## Historial")

    if st.session_state.historial:
        for item in st.session_state.historial[:5]:
            st.markdown(f"**Input:** {', '.join(item['input'])}")
            preview = item['output'][:100].rsplit(' ', 1)[0]
            st.markdown(f"_{preview}..._")
            st.markdown("---")
    else:
        st.write("Sin recomendaciones aún.")