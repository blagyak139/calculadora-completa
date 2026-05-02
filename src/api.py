from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.backend import evaluar, ErrorExpresion

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Peticion(BaseModel):
    dato: str


@app.get("/salud")
def salud():
    return {"estado": "ok"}


@app.post("/sumar")
def sumar(peticion: Peticion):
    try:
        resultado = evaluar(peticion.dato)
        return {"resultado": resultado}
    except ErrorExpresion as e:
        raise HTTPException(status_code=400, detail=str(e))
