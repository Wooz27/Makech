import requests
import os
from dotenv import load_dotenv

load_dotenv()

class n8n:    
    def __init__(self):
        self.url = os.getenv("N8N_WEBHOOK_URL_GET")
        self.post_url = os.getenv("N8N_WEBHOOK_URL_POST")

    
    def leer_reservas(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al leer las reservas: {e}")
            return []

    def enviar_reserva(self, new_payload):
            try:
                 response = requests.post(self.post_url, json=new_payload, timeout=120)
            except requests.exceptions.RequestException as e:
                print(f"Error al enviar la reserva: {e}")
                return None
            
            return {
                 "status": response.status_code,
                 "message": response.text.strip(),
                 "ok": response.ok
            }
        


