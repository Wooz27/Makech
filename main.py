import streamlit as st
from streamlit_option_menu import option_menu
from utils.helpers import reservas_fragment
from components.form import register_form
from components.sidebar import sidebar
from components.qr_gallery import qr_gallery

#main
def main():
    st.set_page_config(
        page_title="Reservas Makech",
        page_icon="assets/favicon.ico",
        layout="centered",
        initial_sidebar_state="auto",
    )
    #componente del sidebar
    sidebar()

    st.title("Reservas Makech")
    st.logo("assets/logo.png", size="large")
    st.markdown("""
<style>
header[data-testid="stHeader"] img {
    height: 150px !important;
    max-height: 150px !important;
    width: auto !important;
    margin-top: 50px !important;
}

section[data-testid="stSidebar"] img {
    height: 150px !important;
    max-height: 150px !important;
    width: auto !important;
    margin-top: 50px !important;
}
</style>
""", unsafe_allow_html=True)


    vista = option_menu(
        menu_title=None,
        options=["Registrar reserva", "Ver reservas", "Ver QRs"],
        icons=["pencil", "table", "qr-code"],
        default_index=0,
        orientation="horizontal",
        key="vista_menu"
        
    )

    if vista == "Registrar reserva":
        register_form()
    elif vista == "Ver reservas":
        reservas_fragment()
    elif vista == "Ver QRs":
        qr_gallery()




if __name__ == "__main__":
    main()
