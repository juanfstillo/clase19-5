from pydantic import BaseModel

class Zona(BaseModel):
    nombre: str
    riesgo: float
    poblacion: int
    costo: float