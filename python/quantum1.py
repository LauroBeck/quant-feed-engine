# ============================================================
# Colab-Safe Animated Quantum Dashboard
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

plt.style.use("dark_background")

# ----------------------------
# Synthetic quantum-like signals
# ----------------------------

frames = 200
t = np.linspace(0, 6*np.pi, frames)

bull  = 0.5 + 0.4*np.sin(t)
bear  = 0.5 + 0.4*np.sin(t + 2.1)
shock = 0.3 + 0.25*np.sin(t * 3.2)

# ----------------------------
# Figure layout
# ----------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 6))

titles = [
    "Momentum (Bull)",
    "Bear Pressure",
    "Vol Shock",
    "Regime State"
]

for ax, title in zip(axs.flat, titles):
    ax.set_title(title, fontsize=12)
    ax.set_xlim(0, frames)
    ax.set_ylim(0, 1)
    ax.grid(color="gray", alpha=0.2)

# Create persistent line objects (CRITICAL)
line_bull,  = axs[0,0].plot([], [], lw=2)
line_bear,  = axs[0,1].plot([], [], lw=2)
line_shock, = axs[1,0].plot([], [], lw=2)

text_state = axs[1,1].text(
    0.5, 0.5, "",
    ha='center', va='center',
    fontsize=16,
    transform=axs[1,1].transAxes
)

axs[1,1].set_xticks([])
axs[1,1].set_yticks([])

# ----------------------------
# Regime logic
# ----------------------------

def classify_regime(b, br, s):
    if b > 0.65:
        return "GREEN / RISK-ON"
    elif br > 0.65:
        return "RED / RISK-OFF"
    elif s > 0.55:
        return "VOLATILITY EVENT"
    else:
        return "NEUTRAL / TRANSITION"

# ----------------------------
# Animation update
# ----------------------------

def update(frame):

    x = np.arange(frame)

    line_bull.set_data(x, bull[:frame])
    line_bear.set_data(x, bear[:frame])
    line_shock.set_data(x, shock[:frame])

    state = classify_regime(
        bull[frame-1],
        bear[frame-1],
        shock[frame-1]
    )

    text_state.set_text(state)

    return line_bull, line_bear, line_shock, text_state

# ----------------------------
# IMPORTANT: keep reference!
# ----------------------------

anim = FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=50,
    blit=True
)

plt.close(fig)

HTML(anim.to_jshtml())
