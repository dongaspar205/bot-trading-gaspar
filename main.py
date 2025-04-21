# Lógica principal del bot de trading (FastAPI backend)
from fastapi import FastAPI, Request
from telegram_listener import telegram_webhook

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot activo"}

@app.post("/webhook/telegram")
async def webhook_handler(req: Request):
    return await telegram_webhook(req)
