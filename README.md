# 🏛️ Sistema de Fiscalización Inteligente DS4PS (V2 - Persistencia SQLite)

Proyecto desarrollado con **FastAPI** y **Streamlit** para simular un sistema de soporte de decisiones orientado a la fiscalización de actividades económicas.

Esta versión actualiza el sistema para incluir persistencia de datos mediante **SQLite**, separando responsabilidades en múltiples archivos y permitiendo priorizar zonas operativas utilizando distintas estrategias de decisión ("impacto", "eficiencia" o "visibilidad") mediante una API REST y una interfaz web interactiva.

---

# 📌 Tecnologías utilizadas

- Python 3.10+
- FastAPI
- Uvicorn (Modo WSGI compatible)
- Streamlit
- Pandas
- Requests
- Pydantic
- SQLAlchemy (ORM para la base de datos)
- python-dotenv (Manejo de variables de entorno)

---

# 📂 Estructura del proyecto

.
├── main.py # Backend FastAPI y ruteo
├── frontend.py # Frontend Streamlit (Dashboard)
├── database.py # Configuración de conexión SQLite y modelo ORM
├── esquemas.py # Modelos de validación de datos (Pydantic)
├── estrategias.py # Lógica de cálculo de prioridad (Patrón Strategy)
├── .env.example # Plantilla para variables de entorno de seguridad
├── ministerio.db # Archivo físico de la base de datos local (SQLite)
└── README.md
