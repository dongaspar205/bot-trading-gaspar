import time
import hmac
import hashlib
import requests
import os

BASE_URL = "https://api.mexc.com"

# Obtener precio actual desde el spot para referencia
def obtener_precio_actual(simbolo):
    url = f"{BASE_URL}/api/v3/ticker/price?symbol={simbolo.replace('/', '')}"
    r = requests.get(url)
    return float(r.json().get("price", 0))

# Interpretar la señal textual desde Telegram
def interpretar_senal(texto):
    try:
        lineas = texto.splitlines()
        tipo = "LONG" if "LONG" in lineas[0] else "SHORT"
        cripto = lineas[1].split(":")[1].strip()
        entrada_line = lineas[2].split(":")[1].strip()
        entrada = float(entrada_line) if entrada_line else None
        sl = float(lineas[3].split(":")[1].strip())
        tp1 = float(lineas[4].split(":")[1].split("(")[0].strip())
        tp2 = float(lineas[5].split(":")[1].split("(")[0].strip())
        tp3 = float(lineas[6].split(":")[1].split("(")[0].strip())
        riesgo = lineas[7].split(":")[1].strip()

        return {
            "cripto": cripto,
            "tipo": tipo,
            "entrada": entrada,
            "sl": sl,
            "tp1": tp1,
            "tp2": tp2,
            "tp3": tp3,
            "riesgo": riesgo
        }
    except Exception as e:
        print(f"❌ Error interpretando señal: {e}")
        return None

# Ejecutar trade en MEXC
def ejecutar_trade(cripto, tipo, entrada, sl, tp1, tp2, tp3, riesgo):
    try:
        MEXC_API_KEY = os.getenv("MEXC_API_KEY")
        MEXC_API_SECRET = os.getenv("MEXC_API_SECRET")

        print(f"🔐 Claves detectadas:")
        print(f"MEXC_API_KEY: {MEXC_API_KEY}")
        print(f"MEXC_API_SECRET: {MEXC_API_SECRET}")

        if not MEXC_API_KEY or not MEXC_API_SECRET:
            raise ValueError("⚠️ Las variables de entorno no están disponibles.")

        simbolo = cripto.replace("/", "")
        precio = obtener_precio_actual(cripto)
        monto = {"Bajo": 150, "Medio": 100, "Alto": 50}.get(riesgo, 100)
        cantidad = round(monto / precio, 4)

        side = "SELL" if tipo == "SHORT" else "BUY"
        positionSide = "SHORT" if tipo == "SHORT" else "LONG"
        order_type = "MARKET" if entrada is None else "LIMIT"
        order_price = entrada if entrada else precio
        ts = int(time.time() * 1000)

        params = {
            "symbol": simbolo,
            "price": order_price,
            "vol": cantidad,
            "leverage": 3,
            "side": side,
            "type": order_type,
            "open_type": "CROSSED",
            "position_id": 0,
            "external_oid": f"oid_{ts}",
            "stop_loss_price": sl,
            "take_profit_price": tp1,
            "timestamp": ts
        }

        # Firmar
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        signature = hmac.new(MEXC_API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        full_query = query_string + f"&sign={signature}"

        headers = {
            "ApiKey": MEXC_API_KEY,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post("https://contract.mexc.com/api/v1/private/order/submit",
                                 headers=headers,
                                 data=full_query)

        print(f"📤 Respuesta de MEXC: {response.status_code} {response.text}")

        if response.status_code == 200:
            return {"status": "ok", "mensaje": f"Trade ejecutado en MEXC para {cripto}"}
        else:
            return {"status": "error", "mensaje": response.text}

    except Exception as e:
        print(f"❌ Error ejecutando orden en MEXC: {e}")
        return {"status": "error", "mensaje": str(e)}
