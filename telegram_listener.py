from fastapi import Request
import os
from ejecucion_mexcbot import interpretar_senal, ejecutar_trade  # ✅ Importamos

async def telegram_webhook(req: Request):
    body = await req.json()
    message = body.get("message", {})
    chat_id = str(message.get("chat", {}).get("id"))
    text = message.get("text", "")

    if "#Señal Cripto" in text:
        print(f"📩 Señal detectada:\n{text}")
        datos = interpretar_senal(text)
        if datos:
            ejecutar_trade(**datos)

        return {"status": "ok", "message": "Señal procesada"}

    return {"status": "ok", "message": "Mensaje ignorado"}
