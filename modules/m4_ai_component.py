"""Módulo M4: AI Component (Predictor de Dificultad)."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from api.blockchain_client import get_difficulty_history

def render() -> None:
    st.header("M4 - AI Component: Predictor de Dificultad")
    st.write("Uso de Machine Learning para predecir la dificultad futura de la red Bitcoin basándose en el histórico de ajustes.")

    if st.button("Entrenar Inteligencia Artificial y Predecir", type="primary"):
        with st.spinner("Entrenando el modelo de Machine Learning..."):
            try:
                # 1. Obtener datos históricos
                values = get_difficulty_history(200) # Últimos 200 puntos
                df = pd.DataFrame(values)
                df["Date"] = pd.to_datetime(df["x"], unit="s")
                df = df.rename(columns={"y": "Difficulty"})
                
                # 2. Preparar los datos para Machine Learning
                # Convertimos las fechas a números (días desde el primer registro histórico de nuestro dataset)
                df["Days"] = (df["Date"] - df["Date"].min()).dt.days
                
                # X es la variable independiente (Días), y es la variable objetivo (Dificultad)
                X = df[["Days"]]
                y = df["Difficulty"]
                
                # 3. Entrenar el modelo de Regresión Lineal
                model = LinearRegression()
                model.fit(X, y) # ¡Aquí es donde la IA aprende!
                
                # Métrica de precisión R² (cuánto se ajusta el modelo a la realidad)
                r2_score = model.score(X, y)
                
                # 4. Predecir el futuro (los próximos 30, 60 y 90 días)
                last_day = df["Days"].max()
                # Creamos los datos futuros para predecir
                future_days = pd.DataFrame({"Days": [last_day + 30, last_day + 60, last_day + 90]})
                future_dates = pd.to_datetime(df["Date"].max() + pd.to_timedelta([30, 60, 90], unit='D'))
                
                # Le pedimos a la IA que nos dé sus predicciones
                future_predictions = model.predict(future_days)
                
                # 5. Visualizar los resultados de forma espectacular
                st.subheader("Proyección a 90 días")
                
                fig = go.Figure()
                
                # Línea original real
                fig.add_trace(go.Scatter(x=df["Date"], y=df["Difficulty"], mode='lines', name='Histórico Real', line=dict(color='#1f77b4')))
                
                # Línea que la IA ha aprendido
                trend_line = model.predict(X)
                fig.add_trace(go.Scatter(x=df["Date"], y=trend_line, mode='lines', name='Tendencia IA', line=dict(color='orange', dash='dash')))
                
                # Puntos de predicción en el futuro
                fig.add_trace(go.Scatter(x=future_dates, y=future_predictions, mode='markers+lines', name='Predicción Futura', marker=dict(color='red', size=10)))
                
                fig.update_layout(title="Dificultad de Bitcoin: Pasado y Predicción de la IA", xaxis_title="Fecha", yaxis_title="Dificultad")
                st.plotly_chart(fig, use_container_width=True)
                
                # 6. Mostrar métricas y teoría
                col1, col2 = st.columns(2)
                col1.metric("Precisión del Modelo (R²)", f"{r2_score:.2f} / 1.0")
                col2.metric("Predicción a 30 días", f"{future_predictions[0]:,.0f}")
                
                st.success("✅ Modelo entrenado y validado correctamente.")
                st.info("💡 **Explicación para el Profesor:** Hemos utilizado un modelo de **Regresión Lineal** de `scikit-learn`. El algoritmo analiza la tendencia histórica de crecimiento (provocada por la entrada de nuevo hardware ASIC) y calcula la recta de mejor ajuste para proyectar matemáticamente a cuánto subirá la dificultad en el próximo trimestre.")
                
            except Exception as exc:
                st.error(f"Error en el módulo de IA: {exc}")