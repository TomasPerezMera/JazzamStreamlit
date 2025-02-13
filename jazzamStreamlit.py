# app.py
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

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
    model = genai.GenerativeModel("gemini-pro")

    # Título e introducción de la app
    st.title("Jazzam - Asistente Musical Virtual")
    st.write(
        """
        ¡Hola! Soy **Jazzam**, tu asistente musical virtual. Estoy aquí para ayudarte a elegir el próximo álbum de John Coltrane
        que se adapte a tus gustos. Ingresa tus artistas o álbumes favoritos y recibirás una recomendación personalizada.
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
            "Recomiéndame el álbum de John Coltrane que más se asemeje a su estilo musical. "
            "Por favor, da tu respuesta en dos párrafos breves, de igual longitud sin importar si elijo 1 o 2 artistas. "
            "Asegúrate de que la respuesta sea aproximadamente un 10% más larga de lo habitual y que mantenga un tono cálido, amable y servicial."
        )

        # Definir el contexto e instrucciones para Jazzam
        context_prompt = (
            "Eres un asistente musical virtual llamado 'Jazzam'. Tu conocimiento se basa en la discografía y biografía de John Coltrane. "
            "Cuando recibas los favoritos del usuario, elige el álbum de John Coltrane que más se asemeje al estilo de esos artistas o álbumes, "
            "y proporciona una explicación detallada y cálida para justificar tu elección. "
            "Si el usuario ha ingresado solo un artista, tu respuesta debe constar de dos párrafos; si ha ingresado dos, la respuesta debe ser un solo párrafo extendido. "
            "Asegúrate de que tus respuestas sean alrededor de un 10% más largas de lo que normalmente serían, utilizando una cantidad apropiada de tokens para ofrecer una explicación completa. "
            "Sé siempre amable y servicial, evitando respuestas secas o demasiado directas, y mantén un tono cálido y accesible en todo momento. "
            "Quiero que le des al usuario la bienvenida en una oración corta, y procedas directamente a la respuesta, separada en otro párrafo. "
            "Tu lista de respuestas posibles se debe limitar a los siguientes álbumes de Coltrane: (Blue Train - Stardust - Giant Steps - Ballads - My Favorite Things - John Coltrane and Johnny Hartman - A Love Supreme - Meditations - Ascension)."
        )

        # Combinar el contexto y el prompt del usuario para formar el prompt completo
        full_prompt = f"{context_prompt}\n\nUsuario: {user_prompt}\n\nJazzam:"

        # Llamar a la API de Gemini para generar la respuesta
        response = model.generate_content(full_prompt)
        return response.text.strip()

    # Procesar el formulario y mostrar la recomendación
    if submit_button:
        # Validar que se haya ingresado al menos un artista o álbum
        if not artist1.strip():
            st.error("Necesito al menos un artista o álbum para recomendarte algo. Por favor, ingresa al menos uno.")
        else:
            # Preparar la lista de artistas
            artists = [artist1.strip()]
            if artist2.strip():
                artists.append(artist2.strip())

            # Mostrar un spinner mientras se genera la recomendación
            with st.spinner("Generando recomendación..."):
                recommendation = generar_recomendacion(artists)

            st.markdown("### Recomendación de Jazzam")
            st.write(recommendation)
            st.success("¡Gracias por utilizar Jazzam! Si deseas otra recomendación, modifica los datos y presiona el botón nuevamente.")