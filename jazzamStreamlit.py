import streamlit as st
import openai
from PIL import Image

# Configure OpenAI API using Streamlit secrets
try:
    openai.api_key = st.secrets["openai"]["api_key"]
except Exception as e:
    st.error("Error: No se pudo acceder al API key de OpenAI. Por favor, verifica la configuración de secrets.")
    st.stop()

# Rest of your UI code remains the same
st.markdown(
    """
    <style>
    .center-title {
        text-align: center;
    }
    .vertical-center {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Create two columns: 1/4 left (image) and 3/4 right (text and form)
col_img, col_text = st.columns([1, 3])

with col_img:
    st.markdown('<div class="vertical-center">', unsafe_allow_html=True)
    image = Image.open("coltrane.jpg")
    st.image(image, caption="John Coltrane", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_text:
    st.markdown("<h1 class='center-title'>Jazzam - Asistente Musical Virtual</h1>", unsafe_allow_html=True)
    st.write(
        """
        ¡Hola! Soy **Jazzam**, tu asistente musical virtual. Estoy acá para ayudarte a elegir tu próximo álbum favorito de John Coltrane.
        Ingresá tus artistas o álbumes favoritos y recibirás una recomendación personalizada.
        """
    )

    with st.form(key="recommendation_form"):
        artist1 = st.text_input("¿Cuál es tu artista o álbum musical favorito?")
        artist2 = st.text_input("¿Tenés otro artista o álbum favorito? (opcional)")
        submit_button = st.form_submit_button(label="Obtener recomendación")

    def generar_recomendacion(artists: list) -> str:
        try:
            user_prompt = (
                f"Mis artistas o álbumes favoritos son {', '.join(artists)}. "
                "Recomendame el álbum de John Coltrane que más se asemeje a su estilo musical. "
                "Por favor, da tu respuesta en dos párrafos breves, de igual longitud sin importar si elijo 1 o 2 artistas. "
                "Asegurate de que tu respuesta mantenga un tono cálido, amable y servicial."
            )

            context_prompt = (
                "Sos un asistente musical virtual llamado 'Jazzam'... "  # Your existing context
            )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": context_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"Error al generar la recomendación: {str(e)}")
            return None

    if submit_button:
        if not artist1.strip():
            st.error("Necesito al menos un artista o álbum para recomendarte algo. Por favor, ingresá al menos uno.")
        else:
            artists = [artist1.strip()]
            if artist2.strip():
                artists.append(artist2.strip())

            with st.spinner("Generando recomendación..."):
                recommendation = generar_recomendacion(artists)
                if recommendation:
                    st.markdown("### Recomendación de Jazzam")
                    st.write(recommendation)
                    st.success("¡Gracias por utilizar Jazzam! Si querés otra recomendación, modificá tus elecciones y presioná el botón nuevamente.")
