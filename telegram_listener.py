from fastapi import Request
from ejecucion_mexcbot import interpretar_senal, ejecutar_trade

async def telegram_webhook(req: Request):
    try:
        body = await req.json()
        message = body.get("message", {})
        chat_id = str(message.get("chat", {}).get("id"))
        text = message.get("text", "")

        if "#Señal Cripto" in text:
            print(f"📩 Señal detectada:\n{text}")
            datos = interpretar_senal(text)
            if datos:
                resultado = ejecutar_trade(**datos)
                print(f"✅ Resultado: {resultado['mensaje']}")
            else:
                print("⚠️ No se pudo interpretar la señal.")

            return {"status": "ok", "message": "Señal procesada"}

        return {"status": "ok", "message": "Mensaje ignorado"}

    except Exception as e:
        print(f"❌ Error en webhook: {e}")
        return {"status": "error", "message": str(e)}
