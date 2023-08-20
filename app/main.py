from fastapi import FastAPI

from app.domain import inicializa_navegador, obtener_datos

app = FastAPI()

@app.get('/')
async def health_check():
    return {"mensaje": "Hola Mundo"}

@app.get('/tablero')
async def tablero():
    navegador = await inicializa_navegador()
    datos = await obtener_datos(navegador)
    return datos

