import base64
import os
import time

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def _obtener_configuracion():
    api_url = os.getenv("EVO_API_URL", "").rstrip("/")
    api_key = os.getenv("EVO_API_KEY", "")
    instance = os.getenv("EVO_INSTANCE", "")

    faltantes = [
        nombre
        for nombre, valor in (
            ("EVO_API_URL", api_url),
            ("EVO_API_KEY", api_key),
            ("EVO_INSTANCE", instance),
        )
        if not valor
    ]
    if faltantes:
        raise ValueError(
            "Faltan variables de entorno: " + ", ".join(faltantes)
        )

    return api_url, api_key, instance


def _obtener_estado(api_url, instance, headers):
    response = requests.get(
        f"{api_url}/instance/connectionState/{instance}",
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("instance", {}).get("state")


def whatsapp_conectado():
    try:
        api_url, api_key, instance = _obtener_configuracion()
        estado = _obtener_estado(api_url, instance, {"apikey": api_key})
        return estado == "open"
    except (requests.RequestException, ValueError):
        return False


def _mostrar_qr(api_url, instance, headers, qr_box):
    response = requests.get(
        f"{api_url}/instance/connect/{instance}",
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()

    qr_base64 = response.json().get("base64")
    if qr_base64:
        image = base64.b64decode(qr_base64.split(",")[-1])
        qr_box.image(
            image,
            caption="Escanea con WhatsApp > Dispositivos vinculados",
            width=300,
        )


def conectar():
    st.title("Conectar WhatsApp")

    try:
        api_url, api_key, instance = _obtener_configuracion()
    except ValueError as error:
        st.error(str(error))
        return

    headers = {"apikey": api_key}

    if st.button("Generar QR"):
        # crea la instancia si no existe (ignora el error si ya existe)
        try:
            requests.post(
                f"{api_url}/instance/create",
                headers=headers,
                timeout=10,
                json={
                    "instanceName": instance,
                    "qrcode": True,
                    "integration": "WHATSAPP-BAILEYS",
                },
            )

            qr_box = st.empty()
            for _ in range(30):
                if _obtener_estado(api_url, instance, headers) == "open":
                    qr_box.success("¡WhatsApp conectado!")
                    break
                _mostrar_qr(api_url, instance, headers, qr_box)
                time.sleep(4)
            else:
                st.warning("El QR expiró, genera uno nuevo.")
        except (requests.RequestException, ValueError) as error:
            st.error(f"No se pudo conectar con Evolution API: {error}")