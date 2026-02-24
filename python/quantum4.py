# ============================================================
# Quantum Bloomberg Macro Engine
# ============================================================

import numpy as np
import yfinance as yf
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# ------------------------------------------------------------
# 1. Market Data (Proxy for Bloomberg Panels)
# ------------------------------------------------------------

tickers = {
    "SPX": "^GSPC",
    "NDX": "^NDX",
    "DOW": "^DJI",
    "VIX": "^VIX"
}

data = yf.download(list(tickers.values()), period="6mo")["Close"]
data.columns = tickers.keys()

returns = np.log(data / data.shift(1))

# ------------------------------------------------------------
# 2. Macro Features (Bloomberg-style abstractions)
# ------------------------------------------------------------

momentum = returns.rolling(20).mean()
volatility = returns.rolling(20).std()

leadership = momentum["NDX"] - momentum["SPX"]
stress = volatility["SPX"]
liquidity = -returns["VIX"].rolling(10).mean()  # inverse fear proxy
trend = momentum["SPX"]

# Normalize to 0–1 range
def normalize(x):
    x = x.iloc[-1]
    return 1 / (1 + np.exp(-5 * x))

trend_strength = normalize(trend)
tech_strength = normalize(leadership)
stress_level = normalize(stress)
liquidity_level = normalize(liquidity)

# ------------------------------------------------------------
# 3. Encode Into Quantum Circuit
# ------------------------------------------------------------

qc = QuantumCircuit(4)

qc.ry(trend_strength * np.pi, 0)     # Q0 Regime
qc.ry(tech_strength * np.pi, 1)      # Q1 Leadership
qc.ry(stress_level * np.pi, 2)       # Q2 Stress
qc.ry(liquidity_level * np.pi, 3)    # Q3 Liquidity

# Entanglement (macro causality)
qc.cx(3, 0)
qc.cx(1, 0)
qc.cx(2, 0)

qc.cz(1, 3)
qc.cz(2, 3)

# ------------------------------------------------------------
# 4. Statevector → Regime Probabilities
# ------------------------------------------------------------

state = Statevector.from_instruction(qc)
probs = state.probabilities()

bull_prob = probs[15]   # |1111>
bear_prob = probs[0]     # |0000>
shock_prob = probs[3]    # example stress state

# ------------------------------------------------------------
# 5. Deployment Readout
# ------------------------------------------------------------

print("\n==============================")
print(" BLOOMBERG-STYLE QUANTUM REGIME")
print("==============================")

print(f"Trend Strength     : {trend_strength:.3f}")
print(f"Tech Leadership    : {tech_strength:.3f}")
print(f"Stress Level       : {stress_level:.3f}")
print(f"Liquidity Regime   : {liquidity_level:.3f}")

print("\nQuantum Probabilities")
print(f"Bull  : {bull_prob:.3f}")
print(f"Bear  : {bear_prob:.3f}")
print(f"Shock : {shock_prob:.3f}")
