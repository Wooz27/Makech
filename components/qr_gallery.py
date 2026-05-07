import base64
import streamlit as st
import pandas as pd
from services.n8n_services import n8n
from services.qr_service import gen_qr


def qr_gallery():
    data = n8n()

    st.subheader("QR de reservas")

    with st.spinner("Cargando reservas..."):
        reservas = data.leer_reservas()

    if not reservas:
        st.warning("No hay reservas disponibles o hubo un error al obtenerlas.")
        return

    df = pd.DataFrame(reservas)

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        buscar = st.text_input("Buscar por nombre", placeholder="Ej: Juan Hernandez")
    with col2:
        areas = ["Todas"] + sorted(df["area"].dropna().unique().tolist()) if "area" in df.columns else ["Todas"]
        area_filtro = st.selectbox("Filtrar por área", areas)
    with col3:
        periodo = st.selectbox("Período", ["Hoy", "Esta semana", "Todas"])

    df_filtrado = df.copy()

    # Filtro por período
    if periodo == "Hoy":
        hoy = pd.Timestamp.now().strftime("%Y-%m-%d")
        df_filtrado = df_filtrado[df_filtrado["fecha"] == hoy]
    elif periodo == "Esta semana":
        df_tmp = df_filtrado.copy()
        df_tmp["fecha"] = pd.to_datetime(df_tmp["fecha"], errors="coerce")
        semana = pd.Timestamp.now().isocalendar().week
        anio = pd.Timestamp.now().year
        mask = (
            (df_tmp["fecha"].dt.isocalendar().week == semana) &
            (df_tmp["fecha"].dt.year == anio)
        )
        df_filtrado = df_filtrado[mask.values]

    if buscar:
        df_filtrado = df_filtrado[
            df_filtrado["nombre"].str.contains(buscar, case=False, na=False)
        ]
    if area_filtro != "Todas" and "area" in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado["area"].str.lower() == area_filtro.lower()]

    if df_filtrado.empty:
        st.info("No se encontraron reservas para los filtros seleccionados.")
        return

    st.markdown(f"**{len(df_filtrado)} reserva(s) encontrada(s)**")
    st.divider()

    # Galería: 3 columnas
    cols = st.columns(3)

    for idx, (_, row) in enumerate(df_filtrado.iterrows()):
        col = cols[idx % 3]
        with col:
            nombre = row.get("nombre", "Sin nombre")
            fecha = row.get("fecha", "")
            hora = row.get("hora de entrada", row.get("hora", ""))
            area = row.get("area", "")
            mesa = row.get("mesa", "")
            personas = row.get("adultos", row.get("num_person", ""))
            ninos = row.get("niños", row.get("num_kids", 0))
            evento = row.get("eventos", row.get("evento", ""))
            notas = row.get("notas", row.get("comentarios", ""))

            # Regenerar QR desde los datos de la reserva
            qr_b64 = gen_qr({
                "name": nombre,
                "area": area,
                "table": mesa,
                "date": fecha,
                "time": hora,
                "persons": personas,
                "niños": ninos,
                "event": evento,
                "nots": notas,
            })

            with st.container(border=True):
                st.markdown(f"**{nombre}**")
                st.caption(f"📅 {fecha}  🕐 {hora}")
                st.caption(f"📍 {area.capitalize() if area else '—'}  🪑 Mesa {mesa}")

                st.image(
                    f"data:image/png;base64,{qr_b64}",
                    width='stretch',
                )

                img_bytes = base64.b64decode(qr_b64)
                filename = f"qr_{nombre.replace(' ', '_')}_{fecha}.png"
                st.download_button(
                    label="⬇️ Descargar QR",
                    data=img_bytes,
                    file_name=filename,
                    mime="image/png",
                    key=f"dl_qr_{idx}",
                    use_container_width=True,
                )
