from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "Hola desde Vercel 🚀"}

@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"msg": f"Hola {nombre}, tu API está funcionando en Vercel!"}
