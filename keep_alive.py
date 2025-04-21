import threading
import time
import requests

def ping():
    while True:
        try:
            print("🔁 Ping automático a Render")
            requests.get("https://bot-trading-gaspar.onrender.com/")
        except Exception as e:
            print(f"⚠️ Error en ping: {e}")
        time.sleep(280)  # cada 4 minutos y 40 segundos

def iniciar_keep_alive():
    thread = threading.Thread(target=ping)
    thread.daemon = True
    thread.start()
