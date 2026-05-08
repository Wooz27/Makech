import streamlit as st

def sidebar():
    st.sidebar.title("Hola, quien esta trabajando? 👋")
    with st.sidebar.expander("Personal"):
        personal = st.radio("Selecciona tu usuario", options=["Estefani", "Silvia", "Erik", "Lourdes", "Otro"], key = "personal_selection")
        st.markdown("## Recuerda que tienes que seleccionar tu usuario para que las reservas se asignen correctamente")

        
    