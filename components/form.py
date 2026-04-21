import streamlit as st 
import datetime as dt
from services.qr_service import gen_qr
from services.n8n_services import n8n
from components.table_views import cargar_reservas

def register_form():
    n8n_service = n8n()

    table_total = {
        "Terraza": [str (i)for i in range (1,11)],
        "Comedor": [str (i)for i in range (1,9)],
        "Palapa": [str (i)for i in range (1,9)],
        "Galeria": [str (i)for i in range (1,3)],
        "Jardin": [str (i)for i in range (1,16)]
    }


    area = st.selectbox("Seleccione el area", list(table_total.keys()))

    event = st.selectbox("Tipo de evento (opcional)", options=["Cumpleaños", "Compromisos", "Aniversario", "Boda", "Bautizos", "Otro"])
    custom_event = ""
    if event == "Otro":
        custom_event = st.text_input("Especifique el tipo de evento")
        event = custom_event

    with st.form(
        key="reservation_form",
        clear_on_submit=True
    ):
        st.subheader("Registrar nueva reserva")
        name = st.text_input("Nombre del cliente")
        table = st.multiselect("Seleccione la mesa", options=table_total[area])
        date = st.date_input("fecha de la reserva")
        time = st.time_input("Hora de la reserva")
        mail = st.text_input("Correo electronico")
        phone = st.text_input("Numero de telefono")
        persons = st.number_input("Numero de adultos", min_value=1, step=1)
        kids = st.number_input("Numero de niños", min_value=0, step=1)
        nots = st.text_area("Notas adicionales")

        submit = st.form_submit_button("Registrar reserva")

        errors = []

        if submit:
            if not name:
                errors.append("El nombre del cliente es requerido.")
            if not table:
                errors.append("Debe seleccionar al menos una mesa.")
            if not mail and not phone:
                errors.append("Se requiere al menos un método de contacto")
            if date < dt.date.today():
                errors.append("La fecha de la reserva no puede ser en el pasado.")
            if event == "Otro" and not custom_event.strip():
                errors.append("Debe especificar el tipo de evento cuando selecciona 'Otro'.")

            event_value = custom_event.strip() if event == "Otro" else event

            if errors:
                st.error("Por favor corrija los siguientes errores:")
                for error in errors:
                    st.error(error)
            
            else:
                qr = gen_qr({
                    "name": name,
                    "area": area.lower(),
                    "table": table,
                    "date": date.strftime("%Y-%m-%d"),
                    "time": time.strftime("%H:%M"),
                    "persons": int(persons),
                    "niños":kids,
                    "event": event_value,
                    "nots": nots,
                })

                payload = {
                    "name": name,
                    "date": date.strftime("%Y-%m-%d"),
                    "time": time.strftime("%I:%M %p"),
                    "table": table,
                    "mail": mail,
                    "qr": qr,
                    "numero": phone,
                    "area": area.lower(),
                    "evento": event_value,
                    "num_person": persons,
                    "num_kids": kids,
                    "comentarios": nots,
                    "personal": st.session_state.get("personal_selection", ""),
                    "time_militar": time.strftime("%H:%M")
                }

                with st.spinner("Registrando reserva..."):
                    resultado = n8n_service.enviar_reserva(payload)
                    if resultado is None:
                        st.error("No se pudo enviar la reserva a n8n.")
                    else:
                        code= resultado["status"]
                        msg = resultado ["message"] or "Sin mensaje de respuesta"

                        if code == 200:
                            st.success(f"Reserva registrada exitosamente: {msg}")
                        elif code == 201:
                            st.warning(f"Reserva creada pero con advertencias: {msg}")
                        elif code == 400:
                            st.error(f"Error en la solicitud: {msg}")
                        elif code == 409:
                            st.error(f"Conflicto al registrar la reserva: {msg}")
                        else:
                            st.error(f"Error desconocido: {msg}")
                
