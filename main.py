from fastapi import FastAPI, Request
from telegram_listener import telegram_webhook

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot activo"}

@app.post("/webhook/telegram")
async def telegram_webhook_handler(req: Request):
    return await telegram_webhook(req)

# ⬇️ Agregalo abajo de todo
from keep_alive import iniciar_keep_alive
iniciar_keep_alive()
