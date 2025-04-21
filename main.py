from fastapi import FastAPI, Request
from telegram_listener import telegram_webhook
from keep_alive import iniciar_keep_alive
import threading

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot activo"}

@app.post("/webhook/telegram")
async def telegram_webhook_handler(req: Request):
    print("📡 Llamada recibida en /webhook/telegram")  # 🔍 Línea de test
    return await telegram_webhook(req)

# 🔁 Ejecutamos keep-alive en segundo plano
def iniciar_bot():
    iniciar_keep_alive()

threading.Thread(target=iniciar_bot, daemon=True).start()
