import qrcode
import base64
from io import BytesIO


def gen_qr(payload):
    nombre = payload.get("name")
    area = payload.get("area")
    table = payload.get("table")
    date = payload.get("date")
    time = payload.get("time")
    person = payload.get("persons")
    event = payload.get("event")
    nots = payload.get("nots")
    kids = payload.get("niños")

    qr = qrcode.make(f"""
    Nombre: {nombre}
    Área: {area}
    Mesa: {table}
    Fecha: {date}
    Hora: {time}
    Adultos: {person}
    Niños: {kids}
    Evento: {event}
    Notas: {nots}
""")
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


