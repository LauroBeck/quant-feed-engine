# ============================================================
# Bloomberg-TV Style Quantum Dashboard
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

plt.style.use("dark_background")

# ----------------------------
# Synthetic quantum market signals
# ----------------------------

frames = 240
t = np.linspace(0, 8*np.pi, frames)

bull  = 0.55 + 0.35*np.sin(t)
bear  = 0.45 + 0.35*np.sin(t + 2.4)
shock = 0.25 + 0.30*np.maximum(0, np.sin(t*2.8))

# ----------------------------
# Regime classifier
# ----------------------------

def classify_regime(b, br, s):
    if s > 0.60:
        return "VOLATILITY EVENT"
    elif b > 0.65:
        return "RISK-ON"
    elif br > 0.65:
        return "RISK-OFF"
    else:
        return "TRANSITION"

# ----------------------------
# Figure Layout (Bloomberg-like)
# ----------------------------

fig = plt.figure(figsize=(12, 7))
gs = fig.add_gridspec(6, 10)

ax_main   = fig.add_subplot(gs[0:4, 0:7])   # Dominant panel
ax_side1  = fig.add_subplot(gs[0:2, 7:10])  # Right monitor
ax_side2  = fig.add_subplot(gs[2:4, 7:10])  # Right monitor
ax_bottom = fig.add_subplot(gs[4:6, 0:10])  # News/state band

for ax in [ax_main, ax_side1, ax_side2]:
    ax.set_xlim(0, frames)
    ax.set_ylim(0, 1)
    ax.grid(alpha=0.15)

ax_bottom.axis("off")

ax_main.set_title("QUANTUM REGIME ENGINE", fontsize=14, pad=10)
ax_side1.set_title("Momentum Monitor", fontsize=10)
ax_side2.set_title("Stress / Shock", fontsize=10)

# Persistent line objects (critical)
line_bull,  = ax_main.plot([], [], lw=2)
line_bear,  = ax_main.plot([], [], lw=2)
line_side1, = ax_side1.plot([], [], lw=2)
line_side2, = ax_side2.plot([], [], lw=2)

text_regime = ax_main.text(
    0.02, 0.92, "",
    transform=ax_main.transAxes,
    fontsize=12
)

text_news = ax_bottom.text(
    0.01, 0.7, "",
    fontsize=11,
    family="monospace"
)

text_deploy = ax_bottom.text(
    0.01, 0.25, "",
    fontsize=10,
    family="monospace"
)

# ----------------------------
# Deployment logic
# ----------------------------

def deployment_vector(regime):
    if regime == "RISK-ON":
        return "Deploy: SPX 1.00 | NDX 1.20 | DOW 0.70 | Hedge 0.10"
    elif regime == "RISK-OFF":
        return "Deploy: SPX 0.20 | NDX 0.10 | DOW 0.30 | Hedge 0.80"
    elif regime == "VOLATILITY EVENT":
        return "Deploy: Shock Mode → Hedge 1.00 | Reduce Beta"
    else:
        return "Deploy: Neutral → Balanced Allocation"

# ----------------------------
# Animation update
# ----------------------------

def update(frame):

    x = np.arange(frame)

    line_bull.set_data(x, bull[:frame])
    line_bear.set_data(x, bear[:frame])

    line_side1.set_data(x, bull[:frame])
    line_side2.set_data(x, shock[:frame])

    regime = classify_regime(
        bull[frame-1],
        bear[frame-1],
        shock[frame-1]
    )

    text_regime.set_text(f"STATE: {regime}")

    text_news.set_text(
        f"Signals → Bull {bull[frame-1]:.2f} | "
        f"Bear {bear[frame-1]:.2f} | "
        f"Shock {shock[frame-1]:.2f}"
    )

    text_deploy.set_text(deployment_vector(regime))

    return (
        line_bull,
        line_bear,
        line_side1,
        line_side2,
        text_regime,
        text_news,
        text_deploy
    )

anim = FuncAnimation(fig, update, frames=frames, interval=60, blit=True)

plt.close(fig)

HTML(anim.to_jshtml())
