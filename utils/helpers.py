import streamlit as st
import pandas as pd
from components.table_views import table_view, table_view_hoy, table_view_semana, cargar_reservas


def reservas_fragment():
    df = pd.DataFrame(cargar_reservas())

    seleccion = st.selectbox("Seleccione la vista", ["Todas las reservas", "Reservas de hoy", "Reservas de la semana"])

    if seleccion == "Todas las reservas":
        st.subheader("Todas las reservas")
        table_view(df)
    elif seleccion == "Reservas de hoy":
        st.subheader("Reservas de hoy")
        table_view_hoy(df)
    elif seleccion == "Reservas de la semana":
        st.subheader("Reservas de la semana")
        table_view_semana(df)
    
