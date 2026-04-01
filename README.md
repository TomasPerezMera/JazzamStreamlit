# Jazzam - Recomendaciones de Música con IA

#### **Jazzam** es una aplicación web ligera que genera recomendaciones personalizadas de álbumes de jazz mediante inteligencia artificial. Fue diseñada para su integración y uso en el E-Commerce "El Rincón de Coltrane" (https://github.com/TomasPerezMera/ColtraNext).

#### La aplicación toma uno o dos artistas o álbumes proporcionados por el usuario y sugiere un álbum de John Coltrane con un estilo similar, ofreciendo una explicación concisa y contextual.

#### Este proyecto está diseñado como un prototipo de portafolio que muestra la integración de la IA, la ingeniería de prompts y las prácticas modernas de front-end.

## Link directo: https://jazzamchat.streamlit.app/

## Tecnologías

- Python
- Streamlit – UI y lógica Frontend
- Google Gemini API – Generación de Texto con IA
- Prompt Engineering – prompts estructurados para guiar comportamiento del modelo
- Session State Management – para persistencia de UI y flujo de interacciones

## IA e Ingeniería de Prompts

La aplicación utiliza un prompt cuidadosamente diseñado para:

- Limitar los resultados a un conjunto predefinido de álbumes
- Garantizar una estructura de respuesta coherente (2 párrafos)
- Aplicar el tono y la localización (español rioplatense)
- Mantener la relevancia entre la entrada del usuario y la recomendación

Esto demuestra el uso práctico de técnicas de ingeniería de prompts para controlar el comportamiento de los modelos de lenguaje grandes (LLM) en una aplicación real.

## Preview

![UI Preview](/JazzamPreview.jpg)

## Setup

Para ejecutar la app localmente:

1. Instalar dependencias

- pip install streamlit google-generativeai

2. Crear un archivo .streamlit/secrets.toml para almacenar la API Key

- [gemini] api_key = "YOUR_API_KEY"

3. Ejecutar la Aplicación

- streamlit run app.py
