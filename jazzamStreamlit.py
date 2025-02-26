# app.py
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Obtener el API key desde la variable de entorno
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    st.error("No se encontró el API key. Por favor, define la variable API_KEY en tu archivo .env.")
else:
    # Configuración de la API
    genai.api_key = API_KEY
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('chat-bison-001')

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

    # Crear dos columnas: 1/4 a la izquierda (imagen) y 3/4 a la derecha (texto y formulario)
    col_img, col_text = st.columns([1, 3])

    with col_img:
        # Contenedor para centrar la imagen verticalmente
        st.markdown('<div class="vertical-center">', unsafe_allow_html=True)
        image = Image.open("coltrane.jpg")  # New image: 1138x924 px
        # Mostrar la imagen en su resolución original; Streamlit se encargará de la reducción
        st.image(image, caption="John Coltrane", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_text:
        # Título centrado y descripción de la app
        st.markdown("<h1 class='center-title'>Jazzam - Asistente Musical Virtual</h1>", unsafe_allow_html=True)
        st.write(
            """
            ¡Hola! Soy **Jazzam**, tu asistente musical virtual. Estoy acá para ayudarte a elegir tu próximo álbum favorito de John Coltrane.
            Ingresá tus artistas o álbumes favoritos y recibirás una recomendación personalizada.
            """
        )

        # Formulario para solicitar inputs al usuario
        with st.form(key="recommendation_form"):
            artist1 = st.text_input("¿Cuál es tu artista o álbum musical favorito?")
            artist2 = st.text_input("¿Tenés otro artista o álbum favorito? (opcional)")
            submit_button = st.form_submit_button(label="Obtener recomendación")

        # Función para generar la recomendación
        def generar_recomendacion(artists: list) -> str:
            # Construir el prompt del usuario
            user_prompt = (
                f"Mis artistas o álbumes favoritos son {', '.join(artists)}. "
                "Recomendame el álbum de John Coltrane que más se asemeje a su estilo musical. "
                "Por favor, da tu respuesta en dos párrafos breves, de igual longitud sin importar si elijo 1 o 2 artistas. "
                "Asegurate de que tu respuesta mantenga un tono cálido, amable y servicial."
            )

            # Definir el contexto e instrucciones para Jazzam
            context_prompt = (
                "Sos un asistente musical virtual llamado 'Jazzam'. Tu conocimiento se basa en la discografía y biografía de John Coltrane. "
                "Cuando recibas los artistas o álbumes favoritos del usuario, elegí el álbum de John Coltrane que más se asemeje al estilo de esos artistas o álbumes, "
                "y proporciona una explicación detallada y cálida para justificar tu elección. "
                "Tu lista de respuestas posibles se debe limitar a los siguientes álbumes de John Coltrane: "
                "(Blue Train - Stardust - Giant Steps - Ballads - My Favorite Things - John Coltrane and Johnny Hartman - A Love Supreme - Meditations - Ascension). "
                "Si el usuario ha ingresado solo un artista, tu respuesta debe constar de dos párrafos; si ha ingresado dos, la respuesta debe ser un solo párrafo extendido. "
                "Asegurate de que tus respuestas sean de longitud apropiada (2 párrafos breves), utilizando una cantidad justa de tokens para ofrecer una explicación completa pero concisa. "
                "Sé siempre amable y servicial, evitando respuestas secas o demasiado directas, y mantené un tono cálido y accesible en todo momento. "
                "Quiero que le des al usuario la bienvenida en una oración corta, y procedas directamente a la respuesta, separada en otro párrafo. "
                "Tu acento o dialecto de respuestas será siempre castellano rioplatense, siendo vos oriundo de Buenos Aires, Argentina. "
            )

            # Combinar el contexto y el prompt del usuario
            full_prompt = f"{context_prompt}\n\nUsuario: {user_prompt}\n\nJazzam:"
            # Llamar a la API de Gemini para generar la respuesta
            response = model.generate_content(full_prompt)
            return response.text.strip()

        # Procesar el formulario y mostrar la recomendación
        if submit_button:
            if not artist1.strip():
                st.error("Necesito al menos un artista o álbum para recomendarte algo. Por favor, ingresá al menos uno.")
            else:
                artists = [artist1.strip()]
                if artist2.strip():
                    artists.append(artist2.strip())

                with st.spinner("Generando recomendación..."):
                    recommendation = generar_recomendacion(artists)

                st.markdown("### Recomendación de Jazzam")
                st.write(recommendation)
                st.success("¡Gracias por utilizar Jazzam! Si querés otra recomendación, modificá tus elecciones y presioná el botón nuevamente.")