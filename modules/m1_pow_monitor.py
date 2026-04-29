"""Módulo M1: Proof of Work Monitor."""

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from api.blockchain_client import get_latest_block, get_block

def render() -> None:
    st.header("M1 - Proof of Work Monitor")
    st.write("Monitorización en vivo del estado de la minería de la red Bitcoin.")

    if st.button("Analizar Red (M1)", type="primary"):
        with st.spinner("Descargando datos y calculando matemáticas criptográficas..."):
            try:
                # 0. Obtenemos los datos desde tu API client
                latest_summary = get_latest_block()
                block = get_block(latest_summary.get("hash"))

                # --- PARTE 1: DIFICULTAD Y UMBRAL (BITS) ---
                st.subheader("1. Dificultad y Umbral Objetivo (Target)")
                
                bits_int = block.get('bits')
                # Convertimos el entero a hexadecimal y quitamos el '0x' inicial
                bits_hex = hex(bits_int)[2:] 
                
                # La estructura del campo bits es: 2 primeros caracteres = exponente, 6 siguientes = coeficiente
                exponent = int(bits_hex[:2], 16)
                coefficient = int(bits_hex[2:], 16)
                
                # Cálculo matemático del Target
                target = coefficient * (256 ** (exponent - 3))
                
                # Representación en binario (256 bits) para visualizar el espacio SHA-256
                target_bin = f"{target:0256b}"
                leading_zeros = 256 - len(target_bin.lstrip('0'))
                
                col1, col2 = st.columns(2)
                col1.metric("Campo 'Bits' (Cabecera)", f"0x{bits_hex}")
                col2.metric("Ceros a la izquierda exigidos", leading_zeros)
                
                st.write("**Representación visual del Umbral en el espacio SHA-256:**")
                st.code(target_bin, language="text")

                # --- PARTE 2: HASH RATE ESTIMADO ---
                st.subheader("2. Estimación del Hash Rate")
                
                # Calculamos el Target Máximo original establecido por Satoshi Nakamoto (Bits 0x1d00ffff)
                max_target = 0x00ffff * (256 ** (0x1d - 3))
                difficulty = max_target / target
                
                # Hash Rate = Dificultad * 2^32 / 600
                hash_rate = difficulty * (2**32) / 600
                exahashes = hash_rate / 1e18 # Convertimos a ExaHashes por segundo para que sea legible
                
                col3, col4 = st.columns(2)
                col3.metric("Dificultad de Minería", f"{difficulty:,.2f}")
                col4.metric("Hash Rate Estimado", f"{exahashes:,.2f} EH/s")

             
                # --- PARTE 3: HISTOGRAMA DE TIEMPO ENTRE BLOQUES ---
                st.subheader("3. Distribución del tiempo entre bloques")
                
                # Solución profesional: Usamos mempool.space para evitar los bloqueos de Cloudflare
                headers = {'User-Agent': 'Mozilla/5.0'}
                blocks_response = requests.get("https://mempool.space/api/v1/blocks", headers=headers).json()
                
                # Extraemos los tiempos y los ordenamos cronológicamente (en esta API el campo es 'timestamp')
                times = sorted([b.get('timestamp') for b in blocks_response if isinstance(b, dict) and 'timestamp' in b])
                
                if len(times) > 1:
                    # Calculamos la diferencia de tiempo entre cada bloque y su anterior (en minutos)
                    diffs_seconds = [times[i] - times[i-1] for i in range(1, len(times))]
                    diffs_minutes = [d / 60 for d in diffs_seconds]
                    
                    # Preparamos los datos para graficar con Plotly
                    df_times = pd.DataFrame({"Minutos": diffs_minutes})
                    
                    # Generamos el histograma de distribución
                    fig = px.histogram(
                        df_times, 
                        x="Minutos", 
                        nbins=15, 
                        title="Tiempo entre los últimos bloques (Distribución Estadística)",
                        labels={"Minutos": "Minutos entre bloques"},
                        color_discrete_sequence=['#F7931A'] # Color Bitcoin
                    )
                    # Añadimos la línea de los 10 minutos objetivo
                    fig.add_vline(x=10, line_dash="dash", line_color="white", annotation_text="Target: 10 min")
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info("💡 Teoría: Como se aprecia en la gráfica, el tiempo de llegada de los bloques sigue un proceso de Poisson, formando una distribución exponencial alrededor del objetivo de 10 minutos.")
                else:
                    st.warning("No se pudieron descargar suficientes bloques hoy para generar la gráfica. Inténtalo de nuevo en unos minutos.")

            except Exception as e:
                st.error(f"Error al calcular los datos del M1: {e}")