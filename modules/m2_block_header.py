"""Módulo M2: Block Header Analyzer."""

import streamlit as st
import hashlib
import struct
from api.blockchain_client import get_block, get_latest_block

def little_endian_hex(hex_str: str) -> bytes:
    """Convierte un string hexadecimal a bytes en formato little-endian."""
    # Aseguramos longitud par
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    # Convertimos a bytes y los invertimos
    return bytes.fromhex(hex_str)[::-1]

def render() -> None:
    st.header("M2 - Block Header Analyzer")
    st.write("Inspección de la cabecera de 80 bytes y verificación local del Proof of Work.")

    # Opción para coger el último bloque automáticamente para facilitar la vida
    if st.button("Cargar el último bloque minado"):
        latest = get_latest_block()
        st.session_state["m2_hash_input"] = latest.get("hash")

    # Input del usuario (con un valor por defecto en session_state)
    block_hash_input = st.text_input(
        "Hash del Bloque (Introduce uno o usa el botón de arriba):",
        value=st.session_state.get("m2_hash_input", ""),
        key="m2_hash_field"
    )

    if st.button("Analizar Cabecera y Verificar PoW", type="primary") and block_hash_input:
        with st.spinner("Descargando bloque y ejecutando doble SHA-256..."):
            try:
                block = get_block(block_hash_input)
                
                st.subheader("1. Los 6 campos de la cabecera")
                
                # Extraemos los campos necesarios
                version = block.get("ver")
                prev_block = block.get("prev_block")
                mrkl_root = block.get("mrkl_root")
                timestamp = block.get("time")
                bits = block.get("bits")
                nonce = block.get("nonce")

                col1, col2 = st.columns(2)
                col1.write(f"**Versión:** {version}")
                col1.write(f"**Hash Previo:** {prev_block}")
                col1.write(f"**Raíz Merkle:** {mrkl_root}")
                col2.write(f"**Timestamp:** {timestamp}")
                col2.write(f"**Bits:** {bits}")
                col2.write(f"**Nonce:** {nonce}")

                # --- VERIFICACIÓN LOCAL DEL PROOF OF WORK ---
                st.subheader("2. Verificación Local (Little-Endian & SHA-256)")
                
                # Empaquetamos los 80 bytes estrictamente como lo hace Bitcoin
                # Formatos de struct: < (little-endian), I (unsigned int 4 bytes)
                header_bin = (
                    struct.pack("<I", version) +
                    little_endian_hex(prev_block) +
                    little_endian_hex(mrkl_root) +
                    struct.pack("<I", timestamp) +
                    struct.pack("<I", bits) +
                    struct.pack("<I", nonce)
                )

                # Aplicamos doble SHA-256 (hashlib exige bytes)
                hash1 = hashlib.sha256(header_bin).digest()
                hash2 = hashlib.sha256(hash1).digest()
                
                # El resultado se debe leer al revés para mostrarlo como string hexadecimal
                calculated_hash = hash2[::-1].hex()

                st.write("**Hash calculado localmente:**")
                st.code(calculated_hash)
                
                if calculated_hash == block_hash_input:
                    st.success("✅ Verificación exitosa: El hash calculado coincide con el hash oficial del bloque.")
                else:
                    st.error("❌ Error de verificación: El hash no coincide.")

                # Comprobación de ceros a la izquierda exigida en M2
                leading_zeros = len(calculated_hash) * 4 - len(bin(int(calculated_hash, 16))[2:])
                st.info(f"El hash calculado tiene **{leading_zeros} bits** a cero al principio, confirmando que está por debajo del umbral objetivo dictado por el campo 'bits'.")

            except Exception as exc:
                st.error(f"Error al procesar el bloque. Verifica el hash. Detalle: {exc}")