import streamlit as st
import requests
import pandas as pd

# 1. Configuración visual del tablero
st.title("🏛️ Tablero de Fiscalización Inteligente DS4PS")
st.markdown("Sistema de Soporte de Decisiones para Asignación de Recursos")

# 2. Interfaz de usuario
estrategia_elegida = st.selectbox(
    "Seleccione Doctrina Política para el operativo", 
    ["impacto", "eficiencia", "visibilidad"] # Agregada 'visibilidad' que tenés en el backend
)

# 3. El Botón de Acción
if st.button("Ejecutar Algoritmo de Priorización"):

    # A. Llamada a la API
    url_api = f"https://prueba-kzld.onrender.com/priorizar/{estrategia_elegida}"
    credenciales = {"x-api-key": "269c0715f99839b174c991f3a24c4c4c"}

    try:
        respuesta = requests.get(url_api, headers=credenciales)

        # 4. Procesamiento de la respuesta
        if respuesta.status_code == 200:
            datos = respuesta.json()
            ranking = datos.get("ranking_operativos", [])
            
            # --- VALIDACIÓN DE SEGURIDAD: ¿Hay datos? ---
            if ranking:
                st.success(f"✅ Estrategia aplicada: {datos['estrategia_aplicada'].upper()}")
                
                df_resultados = pd.DataFrame(ranking)

                # Mostramos la tabla
                st.subheader("Ranking de Prioridad")
                st.dataframe(df_resultados, use_container_width=True)

                # Mostramos el gráfico
                st.subheader("Costo Operativo por Zona")
                st.bar_chart(data=df_resultados, x="nombre", y="costo", color="#360d0d")
            else:
                st.warning("⚠️ La API respondió correctamente, pero no hay zonas cargadas en la base de datos.")
        
        elif respuesta.status_code == 401:
            st.error("🚨 Acceso Denegado. Verifique sus credenciales.")
        else:
            st.error(f"🚨 Error en el servidor: {respuesta.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("🚨 No se pudo conectar al Backend. ¿Está encendido el servidor en el puerto 8080?")
