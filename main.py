# Lógica principal del bot de trading (FastAPI backend)
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot activo"}
