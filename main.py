from fastapi import FastAPI, Request
from telegram_listener import telegram_webhook
from keep_alive import iniciar_keep_alive
import time

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot activo"}

@app.post("/webhook/telegram")
async def telegram_webhook_handler(req: Request):
    return await telegram_webhook(req)

# 🔁 Activamos keep-alive para evitar que Render cierre el servicio
iniciar_keep_alive()

# ⏳ Bucle infinito para mantener vivo el proceso principal
while True:
    time.sleep(3600)
