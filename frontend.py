import streamlit as st
import requests
import pandas as pd

# 1. Configuración visual del tablero
st.title("🏛️ Tablero de Fiscalización Inteligente DS4PS")
st.markdown("Sistema de Soporte de Decisiones para Asignación de Recursos")

# 2. Interfaz de usuario (El control del Ministro)
estrategia_elegida = st.selectbox(
    "Seleccione Doctrina Política para el operativo", 
    ["impacto", "eficiencia"]
)

# 3. El Botón de Acción
if st.button("Ejecutar Algoritmo de Priorización"):

    # A. Preparamos la llamada a la API (El "Teléfono Rojo")
    url_api = f"http://127.0.0.1:8080/priorizar/{estrategia_elegida}"

    # B. Armamos nuestra credencial de acceso (El Header de seguridad)
    credenciales = {"x-api-key": "ClaveSecreta123"}

    # C. Hacemos la petición GET
    respuesta = requests.get(url_api, headers=credenciales)

    # 4. Procesamiento de la respuesta
    if respuesta.status_code == 200:
        datos = respuesta.json()
        st.success(f"✅ Estrategia aplicada exitosamente: {datos['estrategia_aplicada'].upper()}")

        # Convertimos la lista de zonas a un DataFrame de Pandas para verlo lindo
        df_resultados = pd.DataFrame(datos["ranking_operativos"])

        # Mostramos la tabla interactiva
        st.subheader("Ranking de Prioridad")
        st.dataframe(df_resultados, use_container_width=True)

        # Mostramos un gráfico para visualizar rápido el presupuesto necesario
        st.subheader("Costo Operativo por Zona")
        st.bar_chart(data=df_resultados, x="nombre", y="costo", color="#360d0d")

    else:
        st.error("🚨 Acceso Denegado. Verifique sus credenciales ministeriales.")