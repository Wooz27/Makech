import streamlit as st
from components.evo_conect import whatsapp_conectado

def sidebar():
    st.sidebar.title("Hola, quien esta trabajando? 👋")
    with st.sidebar.expander("Personal"):
        personal = st.radio("Selecciona tu usuario", options=["Estefani", "Silvia", "Erik", "Lourdes","Marcelino","Daniel", "Otro"], key = "personal_selection")
        st.markdown("## Recuerda que tienes que seleccionar tu usuario para que las reservas se asignen correctamente")

    if whatsapp_conectado():
        st.sidebar.success("WhatsApp conectado")
    else:
        st.sidebar.warning("Falta conectar a whatsapp")


