"""
Blockchain API client.

Provides helper functions to fetch blockchain data from public APIs.
"""

import requests

BASE_URL = "https://blockchain.info"

def get_latest_block() -> dict:
    """Return the latest block summary."""
    response = requests.get(f"{BASE_URL}/latestblock", timeout=10)
    response.raise_for_status()
    return response.json()

def get_block(block_hash: str) -> dict:
    """Return full details for a block identified by *block_hash*."""
    response = requests.get(
        f"{BASE_URL}/rawblock/{block_hash}", timeout=10
    )
    response.raise_for_status()
    return response.json()

def get_difficulty_history(n_points: int = 100) -> list[dict]:
    """Return the last *n_points* difficulty values as a list of dicts."""
<<<<<<< HEAD
    # Usamos api.blockchain.info para evitar bloqueos HTML
    response = requests.get(
        "https://api.blockchain.info/charts/difficulty",
        params={"timespan": "1year", "format": "json"},
=======
    response = requests.get(
        f"{BASE_URL}/charts/difficulty",
        params={"timespan": "1year", "format": "json", "sampled": "true"},
>>>>>>> f3b4319fb47d612cb695c57d62b0a384126b27bb
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("values", [])[-n_points:]

if __name__ == "__main__":
    # 1. Obtenemos el resumen del último bloque
    print("Conectando a la API de blockchain.info...")
    latest_summary = get_latest_block()
    block_hash = latest_summary.get("hash")

    # 2. Obtenemos los detalles completos del bloque usando su hash
    full_block = get_block(block_hash)

    # 3. Imprimimos los campos requeridos para el Hito 2
    print("\n--- DATOS DEL ÚLTIMO BLOQUE DE BITCOIN ---")
    print(f"Altura (Height): {full_block.get('height')}")
    print(f"Hash: {full_block.get('hash')}")
    print(f"Número de transacciones: {full_block.get('n_tx')}")
    print(f"Nonce: {full_block.get('nonce')}")
    print(f"Bits (Target): {full_block.get('bits')}")

    # Importante 1: Conectar los datos con la teoría
    # Observaciones:
    # 1. El hash del bloque comienza con una gran cantidad de ceros a la izquierda, 
    #    lo que demuestra visualmente el esfuerzo del Proof of Work.
    # 2. El campo 'bits' codifica el 'target threshold' (umbral objetivo) que 
    #    hemos estudiado en los apuntes de la asignatura.