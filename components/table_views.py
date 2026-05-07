import streamlit as st  
from services.n8n_services import n8n
import pandas as pd

data = n8n()

df_super_compact= ["fecha", "nombre", "area", "mesa", "hora de entrada", 
                          "eventos","adultos","niños","numero","mail","notas"]

# Nombres legibles para los encabezados de la tabla
COLUMN_CONFIG = {
    "fecha":          st.column_config.TextColumn("Fecha"),
    "nombre":         st.column_config.TextColumn("Nombre"),
    "area":           st.column_config.TextColumn("Área"),
    "mesa":           st.column_config.TextColumn("Mesa"),
    "hora de entrada":st.column_config.TextColumn("Hora"),
    "eventos":        st.column_config.TextColumn("Evento"),
    "adultos":        st.column_config.NumberColumn("Adultos"),
    "niños":          st.column_config.NumberColumn("Niños"),
    "numero":         st.column_config.TextColumn("Teléfono"),
    "mail":           st.column_config.TextColumn("Correo"),
    "notas":          st.column_config.TextColumn("Notas"),
}

def cargar_reservas():
    return data.leer_reservas()

def table_view(df=None):
    if df is None:
        df = pd.DataFrame(cargar_reservas())
    if not df.empty:
        df_filtrado = df[df_super_compact]
        st.dataframe(df_filtrado, hide_index=True, width='stretch', column_config=COLUMN_CONFIG)
    
    elif df.empty:
        st.warning("No hay reservas disponibles o hubo un error al obtenerlas.")

def table_view_hoy(df=None):
    if df is None:
        df = pd.DataFrame(cargar_reservas())
    if not df.empty:
        df_hoy = df[df["fecha"] == pd.Timestamp.now().strftime("%Y-%m-%d")]
        df_filtrado = df_hoy[df_super_compact]
        if df_filtrado.empty:
            st.warning("No hay reservas para hoy.")
        else:
            st.dataframe(df_filtrado, hide_index=True, width='stretch', column_config=COLUMN_CONFIG)

    else:
        st.warning("No hay reservas disponibles o hubo un error al obtenerlas.")

def table_view_semana(df=None):
    if df is None:
        df = pd.DataFrame(cargar_reservas())
    if not df.empty:
        nuevo_df = df.copy()
        nuevo_df["fecha"]= pd.to_datetime(nuevo_df["fecha"], errors="coerce")
        semana_acual = pd.Timestamp.now().isocalendar().week
        anio_actual = pd.Timestamp.now().year

        df_semana = nuevo_df[(nuevo_df["fecha"].dt.isocalendar().week == semana_acual) & 
                       (nuevo_df["fecha"].dt.year == anio_actual)
                       ]
        
        df_filtrado = df_semana[df_super_compact]
        if df_filtrado.empty:
            st.warning("No hay reservas para esta semana.")
        else:
            st.dataframe(df_filtrado, hide_index=True, width='stretch', column_config=COLUMN_CONFIG)
    else:
        st.warning("No hay reservas disponibles o hubo un error al obtenerlas.")