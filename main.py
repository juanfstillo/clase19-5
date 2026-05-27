from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel

# ==========================================
# 1. CONFIGURACIÓN DE LA API
# ==========================================
app = FastAPI(
    title="Sistema Fiscalización FSOC", 
    description="API para la fiscalización de actividades económicas", 
    version="1.0.0"
)

# ==========================================
# 2. MODELOS DE DATOS Y BASE DE DATOS SIMULADA
# ==========================================
# Esquema estricto de cómo debe ser una zona válida
class Zona(BaseModel):
    nombre: str
    riesgo: float
    poblacion: int
    costo: float

# Nuestra base de datos simulada (El padrón del Estado)
zonas = [
    # Palermo: Problema gigante, pero carísimo de fiscalizar (Mucha logística)
    {"nombre": "Palermo", "riesgo": 0.9, "poblacion": 100000, "costo": 500},
    
    # Recoleta: Riesgo medio, costo alto
    {"nombre": "Recoleta", "riesgo": 0.5, "poblacion": 40000, "costo": 200},
    
    # San Telmo: Problema chico, pero operativamente regalado (Muy eficiente)
    {"nombre": "San Telmo", "riesgo": 0.6, "poblacion": 15000, "costo": 20},
    
    # Córdoba: Problema grande, costo operativo intermedio (Muy equilibrado)
    {"nombre": "Córdoba", "riesgo": 0.8, "poblacion": 80000, "costo": 150}
]

# ==========================================
# 3. LÓGICA DE NEGOCIO (MOTORES DE DECISIÓN)
# ==========================================
# Estrategia 1: Priorizar reducir el daño al mínimo (Sin importar el costo)
def estrategia_impacto(zona):
    return zona["riesgo"] * zona["poblacion"]

# Estrategia 2: Priorizar reducir el costo al mínimo (Sin importar el daño)
def estrategia_costo(zona):
    return (zona["riesgo"] * zona["poblacion"]) / zona["costo"]

# Catálogo de doctrinas políticas (Patrón Strategy)
catalogo_estrategias = {
    "impacto": estrategia_impacto,
    "eficiencia": estrategia_costo,
}

# ==========================================
# 4. CAPA DE SEGURIDAD (AUTENTICACIÓN)
# ==========================================
TOKEN_MINISTERIAL = "ClaveSecreta123"

TOKEN_MINISTERIAL_ZONA_1 = "123"


# Función que oficia de "auditora" para revisar si el cliente tiene permiso
def verificar_permiso(x_api_key: str = Header(...)):
    if x_api_key != TOKEN_MINISTERIAL:
        raise HTTPException(status_code=401, detail="No autorizado. Token inexistente o inválido.")
    

# Función que oficia de "auditora" para revisar si el cliente tiene permiso
def verificar_permiso_zona_1(x_api_key: str = Header(...)):
    if x_api_key != TOKEN_MINISTERIAL_ZONA_1:
        raise HTTPException(status_code=401, detail="No autorizado. Token inexistente o inválido.")

# ==========================================
# 5. ENDPOINTS (LAS VENTANILLAS DEL MINISTERIO)
# ==========================================

@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido al sistema de fiscalización clase 26-5"}

@app.get("/zonas", dependencies=[Depends(verificar_permiso_zona_1)]) 
def obtener_zonas():
    return {"total_zonas": len(zonas), "datos": zonas}

@app.post("/zonas")
def crear_zona(nueva_zona: Zona):
    # Transformamos el modelo validado a un diccionario de Python y lo guardamos
    if(nueva_zona.nombre in [zona["nombre"] for zona in zonas]):
        return {"error": "Ya existe una zona con ese nombre. Elija otro nombre."}  
    zonas.append(nueva_zona.model_dump())
    return {"mensaje": "Zona registrada exitosamente", "zona": nueva_zona}

# Endpoint para que el Ministro decida el orden de los operativos (Ruta Protegida)
@app.get("/priorizar/{nombre_estrategia}", dependencies=[Depends(verificar_permiso)])
def priorizar_zonas(nombre_estrategia: str):

    # 1. Verificamos que la estrategia exista
    if nombre_estrategia not in catalogo_estrategias:
        return {"error": "Estrategia política no reconocida. Use 'impacto' o 'eficiencia'."}

    # 2. Buscamos la fórmula matemática en nuestro catálogo
    formula_elegida = catalogo_estrategias[nombre_estrategia]

    # 3. Ordenamos las zonas de mayor a menor score usando la fórmula
    zonas_ordenadas = sorted(zonas, key=formula_elegida, reverse=True)

    return {
        "estrategia_aplicada": nombre_estrategia,
        "ranking_operativos": zonas_ordenadas
    }

