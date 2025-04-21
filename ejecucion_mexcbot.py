
import time
import hmac
import hashlib
import requests
import os

MEXC_API_KEY = os.getenv("MEXC_API_KEY")
MEXC_API_SECRET = os.getenv("MEXC_API_SECRET")

BASE_URL = "https://api.mexc.com"

headers = {
    "Content-Type": "application/json",
    "ApiKey": MEXC_API_KEY
}

def firmar_cadena(parametros, secret):
    query_string = '&'.join([f"{k}={v}" for k, v in sorted(parametros.items())])
    signature = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return query_string + f"&sign={signature}"

def obtener_precio_actual(simbolo):
    url = f"{BASE_URL}/api/v3/ticker/price?symbol={simbolo.replace('/', '')}"
    r = requests.get(url)
    return float(r.json().get("price", 0))

def ejecutar_trade(cripto, tipo, entrada, sl, tp1, tp2, tp3, riesgo):
    try:
        simbolo = cripto.replace("/", "")
        precio = obtener_precio_actual(cripto)
        monto = {"Bajo": 150, "Medio": 100, "Alto": 50}.get(riesgo, 100)

        # Cálculo de cantidad (Q = USDT / precio actual)
        cantidad = round(monto / precio, 4)

        # Datos comunes
        side = "SELL" if tipo == "SHORT" else "BUY"
        positionSide = "SHORT" if tipo == "SHORT" else "LONG"
        order_type = "MARKET" if entrada is None else "LIMIT"

        # Crear orden
        ts = int(time.time() * 1000)
        data = {
            "symbol": simbolo,
            "price": entrada if entrada else precio,
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

        signed_query = firmar_cadena(data, MEXC_API_SECRET)
        response = requests.post(f"https://contract.mexc.com/api/v1/private/order/submit", 
                                 headers={"ApiKey": MEXC_API_KEY}, 
                                 data=signed_query)

        print(f"🟢 Trade ejecutado: {tipo} {cripto} – Entrada: {entrada or 'Mercado'} – SL: {sl} – TP1: {tp1}")
        return {"status": "ok", "mensaje": f"Trade ejecutado en MEXC para {cripto}"}
    
    except Exception as e:
        print(f"❌ Error ejecutando orden en MEXC: {e}")
        return {"status": "error", "mensaje": str(e)}

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
