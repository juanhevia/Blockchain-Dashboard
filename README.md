# Blockchain Dashboard Project

Use this repository to build your blockchain dashboard project.
Update this README every week.

## Student Information

| Field | Value |
|---|---|
| Student Name | Juan Hevia Losa |
| GitHub Username | @juanhevia |
| Project Title | Blockchain Dashboard Project |
| Chosen AI Approach | [Elige una: Predictor de dificultad / Detector de anomalÃ­as / Estimador de comisiones] |

## Module Tracking

| Module | What it should include | Status |
|---|---|---|
| M1 | Proof of Work Monitor | In progress |
| M2 | Block Header Analyzer | Not started |
| M3 | Difficulty History | Not started |
| M4 | AI Component | Not started |

## Current Progress

## Current Progress

Write 3 to 5 short lines about what you have already done.

- **M1 completado:** Implementado el monitor Proof of Work con cálculo de dificultad, hash rate y gráfica de distribución de tiempos (usando Mempool.space para evitar bloqueos de API).
- **M2 completado:** Analizador de cabeceras funcionando con verificación local del PoW mediante doble SHA-256 y correcta gestión del formato little-endian.
- **M3 completado:** Histórico de dificultad graficado con detección exacta de los eventos de ajuste (cada 2016 bloques) y cálculo de ratios de tiempo real vs objetivo.

## Next Step

Write the next small step you will do before the next class.

- Iniciar el desarrollo del Módulo M4 (AI Integration), preparando los datos para entrenar el modelo de Machine Learning elegido.

## Main Problem or Blocker

Write here if you are stuck with something.

- Tuve problemas con bloqueos anti-bots (Cloudflare) al usar la API de blockchain.info para el M1 y M3, pero lo he resuelto integrando la API de mempool.space y api.blockchain.info.

## Next Step

Write the next small step you will do before the next class.

- Escribir el script en Python (blockchain_client.py) usando la librerÃ­a `requests` para obtener los datos reales del Ãºltimo bloque de Bitcoin.

## Main Problem or Blocker

Write here if you are stuck with something.

- Ninguno por el momento. (O si tienes alguno: Entendiendo quÃ© endpoint de la API necesito usar exactamente).

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py

<!-- student-repo-auditor:teacher-feedback:start -->
## Teacher Feedback

### Kick-off Review

Review time: 2026-04-16 09:59 CEST
Status: Green

Strength:
- Your repository keeps the expected classroom structure.

Improve now:
- The code should connect the API output to theory, especially leading zeros and bits or target.

Next step:
- Add two short code comments that explain leading zeros and the meaning of bits or target.
<!-- student-repo-auditor:teacher-feedback:end -->
