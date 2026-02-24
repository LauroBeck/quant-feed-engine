# ============================================================
# Bloomberg TV Style Quantum Dashboard — Advanced
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Wedge, Rectangle
from IPython.display import HTML

plt.style.use("dark_background")

# ----------------------------
# Time / state evolution
# ----------------------------

frames = 260
t = np.linspace(0, 10*np.pi, frames)

# Smooth quantum-like oscillations
bull  = 0.55 + 0.30*np.sin(t)
bear  = 0.45 + 0.30*np.sin(t + 2.2)

# Micro volatility spikes
shock = 0.15 + 0.25*np.maximum(0, np.sin(t*3.5))

# Synthetic asset streams
spx  = np.cumsum(np.random.normal(0, 0.15, frames))
ndx  = np.cumsum(np.random.normal(0, 0.20, frames))
dow  = np.cumsum(np.random.normal(0, 0.12, frames))
vix  = np.abs(20 + np.cumsum(np.random.normal(0, 0.3, frames)))

# ----------------------------
# Regime logic
# ----------------------------

def classify(b, br, s):
    if s > 0.55:
        return "VOLATILITY EVENT", "orange"
    elif b > 0.65:
        return "RISK ON", "lime"
    elif br > 0.65:
        return "RISK OFF", "red"
    else:
        return "TRANSITION", "gold"

# ----------------------------
# Gauge drawing helper
# ----------------------------

def draw_gauge(ax, value, label):

    ax.clear()
    ax.set_aspect("equal")
    ax.axis("off")

    theta = 360 * value

    # Background ring
    ax.add_patch(Wedge((0,0), 1.0, 0, 360, width=0.18, alpha=0.15))

    # Active probability arc
    ax.add_patch(Wedge((0,0), 1.0, 90, 90-theta, width=0.18))

    ax.text(0, -0.05, f"{value:.2f}", ha="center", fontsize=12)
    ax.text(0, -0.35, label, ha="center", fontsize=9)

# ----------------------------
# Layout (Bloomberg TV geometry)
# ----------------------------

fig = plt.figure(figsize=(12, 7))
gs = fig.add_gridspec(6, 12)

ax_main   = fig.add_subplot(gs[0:4, 0:7])
ax_assets = fig.add_subplot(gs[0:4, 7:12])
ax_g1     = fig.add_subplot(gs[4:6, 0:2])
ax_g2     = fig.add_subplot(gs[4:6, 2:4])
ax_g3     = fig.add_subplot(gs[4:6, 4:6])
ax_news   = fig.add_subplot(gs[4:6, 6:12])

ax_main.set_xlim(0, frames)
ax_main.set_ylim(-10, 10)
ax_main.set_title("QUANTUM REGIME ENGINE", fontsize=13)

ax_assets.set_xlim(0, frames)
ax_assets.set_ylim(-10, 10)
ax_assets.set_title("MARKET MONITOR", fontsize=11)

ax_news.axis("off")

# Persistent line objects
line_spx, = ax_main.plot([], [], lw=2, label="SPX")
line_ndx, = ax_main.plot([], [], lw=2, label="NDX")

line_dow, = ax_assets.plot([], [], lw=1.5)
line_vix, = ax_assets.plot([], [], lw=1.5)

# Regime box
regime_box = Rectangle((0.02, 0.82), 0.30, 0.12,
                       transform=ax_main.transAxes,
                       fill=True)

ax_main.add_patch(regime_box)

text_regime = ax_main.text(0.04, 0.87, "",
                           transform=ax_main.transAxes,
                           fontsize=11)

# Headlines ticker
headlines = [
    "Macro regime stabilizing across risk assets",
    "Volatility compression detected in index space",
    "Liquidity flows rotating into tech leadership",
    "Cross-asset dispersion widening modestly",
    "Shock probabilities mean-reverting"
]

ticker_text = ax_news.text(0.01, 0.55, "", fontsize=10)

# ----------------------------
# Animation update
# ----------------------------

def update(frame):

    x = np.arange(frame)

    line_spx.set_data(x, spx[:frame])
    line_ndx.set_data(x, ndx[:frame])

    line_dow.set_data(x, dow[:frame])
    line_vix.set_data(x, vix[:frame] - 20)

    regime, color = classify(
        bull[frame-1],
        bear[frame-1],
        shock[frame-1]
    )

    # Flashing effect
    if frame % 20 < 10:
        regime_box.set_facecolor(color)
        regime_box.set_alpha(0.35)
    else:
        regime_box.set_alpha(0.15)

    text_regime.set_text(f"STATE: {regime}")

    # Gauges
    draw_gauge(ax_g1, bull[frame-1], "Bull Prob")
    draw_gauge(ax_g2, bear[frame-1], "Bear Prob")
    draw_gauge(ax_g3, shock[frame-1], "Shock Prob")

    # Scrolling ticker
    idx = (frame // 40) % len(headlines)
    ticker_text.set_text(f"> {headlines[idx]}")

    return (
        line_spx,
        line_ndx,
        line_dow,
        line_vix,
        regime_box,
        text_regime,
        ticker_text
    )

anim = FuncAnimation(fig, update, frames=frames,
                     interval=70, blit=False)

plt.close(fig)

HTML(anim.to_jshtml())
