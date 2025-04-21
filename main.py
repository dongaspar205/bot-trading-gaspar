# Lógica principal del bot de trading (FastAPI backend)
from fastapi import FastAPI
from telegram_listener import telegram_webhook  # 👈 importamos el webhook
from fastapi.requests import Request

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot activo"}

# 🔥 Montamos el webhook manualmente
@app.post("/webhook/telegram")
async def telegram_webhook_handler(req: Request):
    return await telegram_webhook(req)
