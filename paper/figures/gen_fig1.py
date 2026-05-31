"""Figure 1: data pipeline drawn as architectural swim-lanes.
Three full-height layer bands (Presentation / Orchestration / Computational)
separated by dashed dividers, with the pipeline boxes sitting on top."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

# ── Colors ───────────────────────────────────────────────────────────────
BAND_PRES = "#EAF3FC"; C_PRES = "#1565C0"
BAND_ORCH = "#EAF6EC"; C_ORCH = "#2E7D32"
BAND_COMP = "#F3EFFA"; C_COMP = "#4527A0"
C_SIZ = "#E65100"
GREY = "#546E7A"
DIVIDER = "#90A4AE"

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# ── Layer bands (full height background) ─────────────────────────────────
BAND_TOP, BAND_BOT = 94, 5
def band(x0, x1, fill):
    ax.add_patch(Rectangle((x0, BAND_BOT), x1 - x0, BAND_TOP - BAND_BOT,
                           facecolor=fill, edgecolor="none", zorder=1))

band(2,  25, BAND_PRES)
band(25, 48, BAND_ORCH)
band(48, 85, BAND_COMP)
# output region (right of last divider) is left white

# ── Dashed vertical dividers between layers ──────────────────────────────
for xsep in (25, 48, 85):
    ax.plot([xsep, xsep], [BAND_BOT, BAND_TOP], linestyle=(0, (6, 4)),
            color=DIVIDER, linewidth=1.8, zorder=2)

# ── Layer titles at the top of each band ─────────────────────────────────
def title(xc, main, sub, color):
    ax.text(xc, 90, main, ha="center", va="top", fontsize=17,
            fontweight="bold", color=color, zorder=3)
    ax.text(xc, 84.5, sub, ha="center", va="top", fontsize=13,
            style="italic", color=color, zorder=3)

title(13.5, "Presentation Layer",  "(app.py)",   C_PRES)
title(36.5, "Orchestration Layer", "(calls.py)", C_ORCH)
title(66.5, "Computational Layer", "(cost.py)",  C_COMP)
ax.text(92.5, 90, "Output", ha="center", va="top", fontsize=15.5,
        fontweight="bold", color=GREY, zorder=3)

# ── Boxes ────────────────────────────────────────────────────────────────
CY = 58
BH = 22
def box(cx, w, fill, edge, text, tcolor, h=BH):
    ax.add_patch(FancyBboxPatch((cx - w / 2, CY - h / 2), w, h,
                 boxstyle="round,pad=0,rounding_size=1.6",
                 facecolor=fill, edgecolor=edge, linewidth=2.4, zorder=5))
    ax.text(cx, CY, text, ha="center", va="center", fontsize=14,
            fontweight="bold", color=tcolor, zorder=6)
    return cx - w / 2, cx + w / 2  # left, right edges

USER_L, USER_R = box(13.5, 19, "#BBDEFB", C_PRES, "User Inputs\n(16 parameters)", C_PRES)
PT_L,   PT_R   = box(36.5, 19, "#A5D6A7", C_ORCH, "Project Type\nDefinition\n(Type 1 / 2 / 3 / 4)", C_ORCH)
SIZ_L,  SIZ_R  = box(57,   15, "#FFE0B2", C_SIZ,  "Sizing\nCalculations\n(10 components)", C_SIZ)
CF_L,   CF_R   = box(76,   15, "#D1C4E9", C_COMP, "Cost\nFunctions\n(15 components)", C_COMP)
EUR_L,  EUR_R  = box(92.5, 13, "#C8E6C9", C_ORCH, "Investment\nCost Items\n(€)", C_ORCH)

# ── Arrows ───────────────────────────────────────────────────────────────
def arrow(x1, y1, x2, y2, color, dashed=False, lw=2.4):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                 arrowstyle="-|>", mutation_scale=22, color=color, lw=lw,
                 linestyle="--" if dashed else "-", zorder=4))

def elabel(xc, yc, text, color, fs=11.5):
    ax.text(xc, yc, text, ha="center", va="center", fontsize=fs,
            color=color, zorder=7,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.9))

# Backbone (solid, on the centerline)
arrow(USER_R, CY, PT_L,  CY, C_PRES)
arrow(PT_R,   CY, SIZ_L, CY, C_ORCH, dashed=True)
arrow(SIZ_R,  CY, CF_L,  CY, C_SIZ)
arrow(CF_R,   CY, EUR_L, CY, C_COMP, lw=3.2)

elabel((USER_R + PT_L) / 2,  CY + 10, "n, P, G, pf,\nV_LV, trafo …", GREY)
elabel((PT_R + SIZ_L) / 2,   CY + 10, "Type 1–4\n(activates)", C_ORCH)
elabel((SIZ_R + CF_L) / 2,   CY + 11, "I, S,\nP, V", C_SIZ)
elabel((CF_R + EUR_L) / 2,   CY + 9,  "15 line\nitems", C_COMP)

# Skip edges (dashed Bezier curves dipping below the centerline, each at a
# distinct depth so they stay clearly separated, landing on box bottoms).
BOT = CY - BH / 2  # bottom edge of every box
def skip(x1, x2, depth, color, label, lx, ly):
    xc = (x1 + x2) / 2
    yc = BOT - depth                     # control point below the line
    t = np.linspace(0, 1, 90)
    bx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * xc + t ** 2 * x2
    by = (1 - t) ** 2 * BOT + 2 * (1 - t) * t * yc + t ** 2 * BOT
    ax.plot(bx, by, linestyle=(0, (5, 3)), color=color, lw=2.2, zorder=4)
    ax.annotate("", xy=(x2, BOT), xytext=(bx[-4], by[-4]),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2,
                                mutation_scale=22), zorder=4)
    elabel(lx, ly, label, color)

skip(40, 71, 10, C_ORCH, "Type 1–4 (gates functions)",     56, BOT - 13)
skip(16, 54, 20, C_PRES, "n, P, V_LV, G, pf, distances …", 33, BOT - 24)
skip(11, 80, 32, C_PRES, "dist, area, material, n, P",     46, BOT - 36)

plt.tight_layout(pad=0.5)
plt.savefig("/Users/davide/Documents/uni/ev-charging-cost-estimator/paper/figures/pipeline_abstract.png",
            dpi=200, bbox_inches="tight", facecolor="white")
print("Figure 1 saved.")
