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
    return await telegram_webhook(req)

# 🧠 Mantener el proceso vivo sin bloquear FastAPI
def iniciar_bot():
    iniciar_keep_alive()
    # Podés agregar más tareas aquí si querés en paralelo

# 🔁 Ejecutamos en segundo plano para que uvicorn no se bloquee
threading.Thread(target=iniciar_bot, daemon=True).start()
