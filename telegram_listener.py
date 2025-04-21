
from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.post("/webhook/telegram")
async def telegram_webhook(req: Request):
    body = await req.json()
    message = body.get("message", {})
    chat_id = str(message.get("chat", {}).get("id"))
    text = message.get("text", "")

    if chat_id != ALLOWED_CHAT_ID:
        return {"status": "ignored", "reason": "unauthorized"}

    if "#Señal Cripto" in text:
        print("Señal recibida:", text)
        return {"status": "ok", "message": "Señal procesada"}
    
    return {"status": "ok", "message": "Sin acción"}
