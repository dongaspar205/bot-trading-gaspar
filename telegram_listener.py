from fastapi import Request
import os

async def telegram_webhook(req: Request):
    body = await req.json()
    message = body.get("message", {})
    chat_id = str(message.get("chat", {}).get("id"))
    text = message.get("text", "")

    if "#Señal Cripto" in text:
        print(f"📩 Señal detectada:\n{text}")

        # ACA deberías agregar la lógica para:
        # 1. Parsear los campos (cripto, tipo, entrada, SL, TP1/2/3, riesgo)
        # 2. Guardar esa señal en memoria o base de datos
        # 3. Iniciar un proceso de monitoreo de precio

        return {"status": "ok", "message": "Señal procesada"}

    return {"status": "ok", "message": "Mensaje ignorado"}
