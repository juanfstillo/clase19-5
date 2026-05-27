````md
# 🏛️ Sistema de Fiscalización Inteligente DS4PS

Proyecto desarrollado con **FastAPI** y **Streamlit** para simular un sistema de soporte de decisiones orientado a la fiscalización de actividades económicas.

El sistema permite priorizar zonas operativas utilizando distintas estrategias de decisión ("impacto" o "eficiencia") mediante una API REST y una interfaz web interactiva.

---

# 📌 Tecnologías utilizadas

- Python 3.10+
- FastAPI
- Uvicorn
- Streamlit
- Pandas
- Requests
- Pydantic

---

# 📂 Estructura del proyecto

```bash
.
├── main.py          # Backend FastAPI
├── frontend.py      # Frontend Streamlit
└── README.md
```

---

# ⚙️ Descripción del sistema

El proyecto se divide en dos partes:

## 1. Backend - FastAPI (`main.py`)

La API expone endpoints para:

- Consultar zonas
- Crear nuevas zonas
- Priorizar operativos
- Aplicar estrategias de decisión
- Validar autenticación mediante API Keys

### Estrategias implementadas

| Estrategia | Descripción |
|---|---|
| `impacto` | Prioriza zonas con mayor riesgo e impacto poblacional |
| `eficiencia` | Prioriza zonas con mejor relación impacto/costo |

---

## 2. Frontend - Streamlit (`frontend.py`)

Interfaz gráfica que permite:

- Seleccionar una doctrina política
- Ejecutar el algoritmo de priorización
- Visualizar rankings
- Mostrar gráficos interactivos

---

# 🔐 Seguridad

La API utiliza autenticación mediante headers:

```http
x-api-key
```

## Tokens definidos

### Token ministerial principal

```text
ClaveSecreta123
```

### Token para endpoint `/zonas`

```text
123
```

---

# 🚀 Instalación

## 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd <nombre-del-proyecto>
```

---

## 2. Crear entorno virtual

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Instalar dependencias

```bash
pip install fastapi uvicorn streamlit pandas requests pydantic
```

---

# ▶️ Cómo levantar el proyecto

## Paso 1 — Levantar la API FastAPI

Ejecutar:

```bash
uvicorn main:app --reload
```

La API quedará disponible en:

```text
http://127.0.0.1:8000
```

---

## Paso 2 — Levantar Streamlit

En otra terminal:

```bash
streamlit run frontend.py
```

La interfaz web abrirá automáticamente en:

```text
http://localhost:8501
```

---

# 📡 Endpoints disponibles

## GET `/`

Endpoint raíz.

### Respuesta

```json
{
  "mensaje": "Bienvenido al sistema de fiscalización clase 26-5"
}
```

---

## GET `/zonas`

Obtiene todas las zonas registradas.

### Requiere header

```http
x-api-key: 123
```

---

## POST `/zonas`

Crea una nueva zona.

### Body esperado

```json
{
  "nombre": "Nueva Zona",
  "riesgo": 0.8,
  "poblacion": 50000,
  "costo": 150
}
```

---

## GET `/priorizar/{estrategia}`

Prioriza las zonas según la estrategia seleccionada.

### Estrategias válidas

- `impacto`
- `eficiencia`

### Ejemplo

```bash
GET /priorizar/impacto
```

### Requiere header

```http
x-api-key: ClaveSecreta123
```

---

# 🧠 Conceptos implementados

El proyecto implementa varios conceptos importantes de desarrollo backend:

- APIs REST
- Arquitectura cliente-servidor
- Validación con Pydantic
- Autenticación básica con headers
- Patrón Strategy
- Interfaces gráficas con Streamlit
- Visualización de datos
- Modelado de datos
- Ordenamiento dinámico de información

---

# 📊 Flujo de funcionamiento

```text
Usuario → Streamlit → FastAPI → Motor de Estrategias → Respuesta → Dashboard
```

---

# 🖥️ Captura conceptual del flujo

1. El usuario selecciona una estrategia
2. Streamlit realiza una petición HTTP
3. FastAPI valida credenciales
4. Se ejecuta la estrategia elegida
5. Se ordenan las zonas
6. Se devuelven los resultados
7. Streamlit muestra tablas y gráficos

---

# 📈 Ejemplo de ranking

| Zona | Riesgo | Población | Costo |
|---|---|---|---|
| Palermo | 0.9 | 100000 | 500 |
| Córdoba | 0.8 | 80000 | 150 |
| Recoleta | 0.5 | 40000 | 200 |
| San Telmo | 0.6 | 15000 | 20 |

---

# 👨‍💻 Autor

Proyecto educativo desarrollado para prácticas de:

- FastAPI
- Streamlit
- Arquitectura de APIs
- Sistemas de soporte de decisiones

---
````
