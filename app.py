import streamlit as st

# Importamos los módulos que tienes en la carpeta 'modules'
from modules import m1_pow_monitor, m2_block_header, m3_difficulty_history, m4_ai_component

# Configuración básica de la página
st.set_page_config(page_title="CryptoChain Analyzer", page_icon="🔗", layout="wide")

# Menú lateral de navegación
st.sidebar.title("Navegación")
seleccion = st.sidebar.radio(
    "Ir a:",
    ["M1: PoW Monitor", "M2: Block Header", "M3: Difficulty History", "M4: AI Component"]
)

# Lógica para mostrar un módulo u otro según lo que elijas en el menú
if seleccion == "M1: PoW Monitor":
    m1_pow_monitor.render()
elif seleccion == "M2: Block Header":
    m2_block_header.render()
elif seleccion == "M3: Difficulty History":
    m3_difficulty_history.render()
elif seleccion == "M4: AI Component":
    m4_ai_component.render()
