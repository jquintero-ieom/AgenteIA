### IMPORTAR LAS LIBRERIAS NECESARIAS PARA EL CHAT

import streamlit as st
import google.generativeai as genai
from thefuzz import process
import os

###ESTILOS PARA EL CHATBOT
st.markdown("""
 <style>
    .stApp { background-color: #f4f7f9; }
    [data-testid="column"] {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .stChatMessage { border-radius: 10px; border: 1px solid #e0e0e0; }
    .stButton>button {
        background-color: #a71e2d !important;
        color: white !important;
        border-radius: 10px;
        width: 100%;
    }
    h1, h2, h3 { color: #0c2340; }
    </style>

""",unsafe_allow_html=True)


### CONFIGURAR EL ENTORNO GRAFICO DEL CHATBOT
st.set_page_config(
    page_title="MUNDIALITO - Asistente IA para el grupo G66",
    page_icon="🤓",
    layout="wide"
)

###LOGICA DEL CHATBOT - LAS REGLAS

CONOCIMIENTO_ESTATICO = {
    "hola":"¡Hola! Soy tu asistente CREDIUNIÓN. ¿Cómo puedo ayudarte?",
    "informacion":"Nuestros servicios están al alcance de todos",
    "personal":"CREDIUNIÓN cuenta con una planta de personal altamente capacitado y con excelente sentido de pertenencia",
    "horarios":"Atendemos de lunes a viernes en horario de oficina",
    "contacto": "Puedes contactarnos a través de nuestra línea telefónica 018000-XXX-XXX o al correo info@crediunion.com",
    "ubicacion": "Nuestras oficinas principales están en la Calle 112 # 10-50, Bogotá.",
    "chao":"Fue un placer ayudarte"
}

INFO_CREDITOS = {
    "libranzas":"Tenemos convenios con tu empresa para créditos por libranza, llena el formular para consultar tu estado financiero",
    "consumo":"Ofrecemos créditos de libre inversión",
    "finaciacion":"Financiamos tus proyecto de construcción y/o estudios",
    "hipotecario": "Ofrecemos créditos hipotecarios para la compra de vivienda nueva o usada.",
    "vehiculo": "Financiamos la compra de tu vehículo con las mejores tasas."
}

###DIVIDIMOS EL ESPACIO EN EL SITIO WEB PARA ORGANIZAR EL CONTENIDO DEL CHATBOT
colConfiguracion, colChat = st.columns([1,2],gap="large")

###CONTENIDO DE LAS COLUMNAS - CONFIGURACIÓN DE LAS CREDENCIALES
with colConfiguracion:
    st.image("logo.jpg")
    st.subheader("Ajustes ⚙️")
    clave_api = st.text_input("Introduce la clave de API",type="password")

###COLUMNA 2 - ESPACIO DEL CHAT PARA INTERACCION CON EL CLIENTE O USUARIO
with colChat:
    st.title("CHATBOT - MUNDIALITO 🤓")

    if "messages"not in st.session_state:
        st.session_state["messages"] = []

    ###HISTORIAL DEL CHAT
    chat_container = st.container(height=500, border=True)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    ###ENTRADA DEL USUARIO
    if prompt:=st.chat_input("Escribe tu pregunta aqui."):
        st.session_state.messages.append({"role":"user","content":prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
    ###RESPUESTA DEL CHATBOT
        opciones =list(CONOCIMIENTO_ESTATICO.keys())+list(INFO_CREDITOS.keys())
        mejor_llave,puntaje=process.extractOne(prompt.lower(),opciones)

        with chat_container:
            with st.chat_message("assistant"):
                if puntaje>70:
                    respuesta=CONOCIMIENTO_ESTATICO.get(mejor_llave) or INFO_CREDITOS.get(mejor_llave)
                else:
                    try:
                        genai.configure(api_key="AIzaSyBl4khdoHVr0sQPKWdw9IYWz4Q_9RNbQO0")
                        model=genai.GenerativeModel("gemini-2.5-flash")
                        response=model.generate_content(prompt)
                        respuesta = response.text
                    except Exception as e:
                        respuesta=f"Error G66: {e}"

                st.markdown(respuesta)
                st.session_state.messages.append({"role":"assistant","content":respuesta})
