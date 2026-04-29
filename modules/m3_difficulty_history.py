"""Módulo M3: Difficulty History."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from api.blockchain_client import get_difficulty_history

def render() -> None:
    st.header("M3 - Difficulty History")
    st.write("Evolución de la dificultad en los últimos periodos de ajuste (cada 2016 bloques).")

    if st.button("Cargar Histórico de Dificultad", type="primary", key="m3_load"):
        with st.spinner("Descargando datos históricos y calculando ratios..."):
            try:
                # 1. Descarga de datos
                values = get_difficulty_history(150) # Traemos suficientes puntos
                df = pd.DataFrame(values)
                df["Date"] = pd.to_datetime(df["x"], unit="s")
                df = df.rename(columns={"y": "Difficulty"})
                
                # 2. Matemáticas del Ajuste de Dificultad
                # Detectamos dónde la dificultad ha cambiado respecto al punto anterior
                df["Diff_Change"] = df["Difficulty"].diff()
                
                # Filtramos solo los momentos exactos de ajuste (cada 2016 bloques)
                adjustments = df[df["Diff_Change"] != 0].copy()
                
                # Ratio de tiempo: La fórmula de ajuste es Diff_New = Diff_Old * (Tiempo_Objetivo / Tiempo_Real)
                # Por tanto: Tiempo_Real / Tiempo_Objetivo = Diff_Old / Diff_New
                adjustments["Prev_Diff"] = adjustments["Difficulty"].shift(1)
                adjustments["Ratio (Real/Objetivo)"] = adjustments["Prev_Diff"] / adjustments["Difficulty"]
                
                # 3. Visualización Principal
                fig = px.line(df, x="Date", y="Difficulty", title="Evolución de la Dificultad de Minería")
                
                # Añadimos los marcadores rojos en los momentos exactos de ajuste
                fig.add_trace(go.Scatter(
                    x=adjustments["Date"], 
                    y=adjustments["Difficulty"],
                    mode="markers",
                    name="Ajuste (2016 bloques)",
                    marker=dict(color="red", size=10, symbol="x")
                ))
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 4. Tabla analítica de los ajustes exigida en los requisitos
                st.subheader("Análisis de Ratios en los últimos Ajustes")
                st.info("Un ratio > 1 indica que los bloques se minaron más rápido de lo esperado (menos de 600s de media), provocando una subida de la dificultad.")
                
                # Limpiamos la tabla para mostrar los datos relevantes
                display_df = adjustments.dropna(subset=["Ratio (Real/Objetivo)"])
                display_df = display_df[["Date", "Difficulty", "Ratio (Real/Objetivo)"]].tail(5)
                
                st.dataframe(display_df, use_container_width=True)

            except Exception as exc:
                st.error(f"Error cargando la gráfica: {exc}")