from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Importamos nuestros módulos separados (Arquitectura Limpia)
from database import get_db, ZonaDB
from esquemas import Zona
from estrategias import catalogo_estrategias

# ==========================================
# 0. CARGA DE SECRETOS DE ESTADO (.env)
# ==========================================
load_dotenv()
TOKEN_MINISTERIAL = os.getenv("TOKEN_MINISTERIAL")
TOKEN_MINISTERIAL_ZONA_1 = os.getenv("TOKEN_MINISTERIAL_ZONA_1")

if not TOKEN_MINISTERIAL or not TOKEN_MINISTERIAL_ZONA_1:
    raise RuntimeError("🚨 Faltan las credenciales de seguridad en el archivo .env")

# ==========================================
# 1. CONFIGURACIÓN DE LA API
# ==========================================
app = FastAPI(
    title="Sistema Fiscalización V2 (Con Base de Datos)", 
    description="API para la fiscalización con persistencia en SQLite", 
    version="2.0.0"
)

# ==========================================
# 2. CAPA DE SEGURIDAD
# ==========================================
def verificar_permiso(x_api_key: str = Header(...)):
    if x_api_key != TOKEN_MINISTERIAL:
        raise HTTPException(status_code=401, detail="No autorizado.")
    
def verificar_permiso_zona_1(x_api_key: str = Header(...)):
    if x_api_key != TOKEN_MINISTERIAL_ZONA_1:
        raise HTTPException(status_code=401, detail="No autorizado.")

# ==========================================
# 3. ENDPOINTS
# ==========================================
@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido al sistema con persistencia de datos"}

@app.get("/zonas", dependencies=[Depends(verificar_permiso_zona_1)]) 
def obtener_zonas(db: Session = Depends(get_db)):
    # Buscamos todas las zonas directamente en el archivo SQLite
    zonas_db = db.query(ZonaDB).all()
    return {"total_zonas": len(zonas_db), "datos": zonas_db}

@app.post("/zonas")
def crear_zona(nueva_zona: Zona, db: Session = Depends(get_db)):
    # 1. Verificamos que la zona no esté repetida en la base de datos
    zona_existente = db.query(ZonaDB).filter(ZonaDB.nombre == nueva_zona.nombre).first()
    if zona_existente:
        return {"error": "Ya existe una zona con ese nombre. Elija otro."}  
    
    # 2. Guardamos en el disco duro (SQLite)
    nueva_zona_db = ZonaDB(**nueva_zona.model_dump())
    db.add(nueva_zona_db)
    db.commit()
    db.refresh(nueva_zona_db)
    return {"mensaje": "Zona registrada exitosamente en la BD", "zona": nueva_zona_db}

@app.get("/priorizar/{nombre_estrategia}", dependencies=[Depends(verificar_permiso)])
def priorizar_zonas(nombre_estrategia: str, db: Session = Depends(get_db)):
    if nombre_estrategia not in catalogo_estrategias:
        return {"error": "Estrategia política no reconocida."}

    # Obtenemos las zonas de la base de datos
    zonas_db = db.query(ZonaDB).all()

    # Buscamos la fórmula y ordenamos los registros
    formula_elegida = catalogo_estrategias[nombre_estrategia]
    zonas_ordenadas = sorted(zonas_db, key=formula_elegida, reverse=True)

    return {
        "estrategia_aplicada": nombre_estrategia,
        "ranking_operativos": zonas_ordenadas
    }

# ==========================================
# 6. ARRANQUE EN MODO COMPATIBLE (WSGI)
# ==========================================
if __name__ == "__main__":
    import uvicorn
    # Eliminamos el uso de librerías de C/loop asíncronos pesados
    # Usamos un modo que Windows/GitBash puede manejar
    uvicorn.run(app, host="127.0.0.1", port=8080, loop="none")