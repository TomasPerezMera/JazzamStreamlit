# app.py
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image  # Import Pillow for image handling

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

    # Crear dos columnas: la izquierda ocupará 3/4 y la derecha 1/4 de la pantalla
    col1, col2 = st.columns([3, 1])

    with col1:
        # Título e introducción de la app
        st.title("Jazzam - Asistente Musical Virtual")
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
                "Asegúrate de que tu respuesta mantenga un tono cálido, amable y servicial."
            )

            # Definir el contexto e instrucciones para Jazzam
            context_prompt = (
                "Eres un asistente musical virtual llamado 'Jazzam'. Tu conocimiento se basa en la discografía y biografía de John Coltrane. "
                "Tu acento o dialecto de respuestas será siempre español rioplatense, de Buenos Aires, Argentina. "
                "Cuando recibas los artistas o álbumes favoritos del usuario, elige el álbum de John Coltrane que más se asemeje al estilo de esos artistas o álbumes, "
                "y proporciona una explicación detallada y cálida para justificar tu elección. "
                "Tu lista de respuestas posibles se debe limitar a los siguientes álbumes de John Coltrane: "
                "(Blue Train - Stardust - Giant Steps - Ballads - My Favorite Things - John Coltrane and Johnny Hartman - A Love Supreme - Meditations - Ascension). "
                "Si el usuario ha ingresado solo un artista, tu respuesta debe constar de dos párrafos; si ha ingresado dos, la respuesta debe ser un solo párrafo extendido. "
                "Asegúrate de que tus respuestas sean de longitud apropiada (2 párrafos breves), utilizando una cantidad justa de tokens para ofrecer una explicación completa pero concisa. "
                "Sé siempre amable y servicial, evitando respuestas secas o demasiado directas, y mantén un tono cálido y accesible en todo momento. "
                "Quiero que le des al usuario la bienvenida en una oración corta, y procedas directamente a la respuesta, separada en otro párrafo. "
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
                st.error("Necesito al menos un artista o álbum para recomendarte algo. Por favor, ingresá al menos uno.")
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
                st.success("¡Gracias por utilizar Jazzam! Si querés otra recomendación, modificá tus elecciones y presioná el botón nuevamente.")

    with col2:
        # Cargar y redimensionar la imagen
        image = Image.open("coltrane.jpg")
        # Redimensionar la imagen a un ancho adecuado para la columna (por ejemplo, 300px)
        # Manteniendo la relación de aspecto original
        desired_width = 300
        original_width, original_height = image.size
        desired_height = int((desired_width / original_width) * original_height)
        image = image.resize((desired_width, desired_height))
        st.image(image, caption="John Coltrane", use_column_width=True)
