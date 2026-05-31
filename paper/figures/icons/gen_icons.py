"""Generate small function-type icons for the pipeline diagram."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

W, H = 1.4, 1.1   # inches
DPI  = 90          # → ~126 x 99 px


def save(name, color):
    plt.tight_layout(pad=0.1)
    plt.savefig(f"{name}.png", dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()


# ── 1. LINEAR  (ax + b)  ───────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
# axes
ax.annotate('', xy=(0.95, 0.08), xytext=(0.05, 0.08),
            arrowprops=dict(arrowstyle='->', color='#888', lw=1.2))
ax.annotate('', xy=(0.12, 0.92), xytext=(0.12, 0.08),
            arrowprops=dict(arrowstyle='->', color='#888', lw=1.2))
# line
x = np.array([0.15, 0.88])
y = 0.15 + 0.75 * (x - 0.15) / (0.88 - 0.15)
ax.plot(x, y, color='#283593', lw=2.5)
save('icons/linear', '#283593')

# ── 2. LOOKUP TABLE (LUT) ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
rows = [('x', 'y'), ('x₁', 'y₁'), ('x₂', 'y₂'), ('⋮', '⋮')]
cols = [0.20, 0.55, 0.80]
row_h = 0.82 / len(rows)
for i, (xi, yi) in enumerate(rows):
    yc = 0.9 - i * row_h
    fc = '#FFF8E1' if i == 0 else 'white'
    rect = mpatches.FancyBboxPatch((0.08, yc - row_h * 0.85),
                                   0.38, row_h * 0.82,
                                   boxstyle="square,pad=0.01",
                                   facecolor=fc, edgecolor='#F57F17', lw=0.8)
    ax.add_patch(rect)
    rect2 = mpatches.FancyBboxPatch((0.54, yc - row_h * 0.85),
                                    0.38, row_h * 0.82,
                                    boxstyle="square,pad=0.01",
                                    facecolor=fc, edgecolor='#F57F17', lw=0.8)
    ax.add_patch(rect2)
    ax.text(0.27, yc - row_h * 0.42, xi, ha='center', va='center',
            fontsize=7, color='#333', fontweight='bold' if i == 0 else 'normal')
    ax.text(0.73, yc - row_h * 0.42, yi, ha='center', va='center',
            fontsize=7, color='#333', fontweight='bold' if i == 0 else 'normal')
    if i > 0:
        ax.annotate('', xy=(0.54, yc - row_h * 0.42), xytext=(0.46, yc - row_h * 0.42),
                    arrowprops=dict(arrowstyle='->', color='#F57F17', lw=1))
save('icons/lut', '#F57F17')

# ── 3. EXPONENTIAL  (A·e^(bx)) ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.annotate('', xy=(0.95, 0.08), xytext=(0.05, 0.08),
            arrowprops=dict(arrowstyle='->', color='#888', lw=1.2))
ax.annotate('', xy=(0.12, 0.92), xytext=(0.12, 0.08),
            arrowprops=dict(arrowstyle='->', color='#888', lw=1.2))
x = np.linspace(0.15, 0.88, 100)
raw = np.exp(3.5 * (x - 0.15)) - 1
y = 0.12 + 0.76 * raw / raw[-1]
ax.plot(x, y, color='#880E4F', lw=2.5)
save('icons/exponential', '#880E4F')

# ── 4. CEILING / STEP  (⌈x/k⌉ · c) ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.annotate('', xy=(0.95, 0.08), xytext=(0.05, 0.08),
            arrowprops=dict(arrowstyle='->', color='#888', lw=1.2))
ax.annotate('', xy=(0.12, 0.92), xytext=(0.12, 0.08),
            arrowprops=dict(arrowstyle='->', color='#888', lw=1.2))
steps_x = [0.15, 0.33, 0.33, 0.52, 0.52, 0.70, 0.70, 0.88]
steps_y = [0.18, 0.18, 0.38, 0.38, 0.58, 0.58, 0.78, 0.78]
ax.step(steps_x, steps_y, where='post', color='#6A1B9A', lw=2.5)
ax.plot(steps_x, steps_y, color='#6A1B9A', lw=2.5)
save('icons/ceiling', '#6A1B9A')

# ── 5. WEIGHTED LINEAR  (Σ wᵢxᵢ) ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
inputs = [('x₁', 0.78), ('x₂', 0.55), ('x₃', 0.32)]
for label, yp in inputs:
    ax.text(0.10, yp, label, ha='center', va='center', fontsize=8, color='#00695C')
    ax.annotate('', xy=(0.44, 0.55), xytext=(0.18, yp),
                arrowprops=dict(arrowstyle='->', color='#00695C', lw=1.2))
circle = plt.Circle((0.54, 0.55), 0.10, color='#E0F2F1', ec='#00695C', lw=1.5, zorder=3)
ax.add_patch(circle)
ax.text(0.54, 0.55, 'Σ', ha='center', va='center', fontsize=11,
        color='#00695C', fontweight='bold', zorder=4)
ax.annotate('', xy=(0.90, 0.55), xytext=(0.64, 0.55),
            arrowprops=dict(arrowstyle='->', color='#00695C', lw=1.5))
ax.text(0.94, 0.55, '€', ha='center', va='center', fontsize=9, color='#00695C', fontweight='bold')
save('icons/weighted', '#00695C')

# ── 6. DERIVED / INVERSE  (f⁻¹) ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.annotate('', xy=(0.95, 0.08), xytext=(0.05, 0.08),
            arrowprops=dict(arrowstyle='->', color='#888', lw=1.2))
ax.annotate('', xy=(0.12, 0.92), xytext=(0.12, 0.08),
            arrowprops=dict(arrowstyle='->', color='#888', lw=1.2))
# forward curve (dashed)
x = np.linspace(0.15, 0.88, 100)
raw = np.exp(3.5 * (x - 0.15)) - 1
y_fwd = 0.12 + 0.76 * raw / raw[-1]
ax.plot(x, y_fwd, color='#90A4AE', lw=1.5, linestyle='--', alpha=0.6)
# inverse curve (solid)
y_inv = x  # inverse of monotone fn through same range, simplified as log shape
raw2 = np.log(1 + 6 * (x - 0.15))
raw2 = np.clip(raw2, 0, None)
y_inv2 = 0.12 + 0.76 * raw2 / raw2[-1]
ax.plot(x, y_inv2, color='#546E7A', lw=2.5)
ax.text(0.75, 0.30, 'f⁻¹', fontsize=9, color='#546E7A', fontweight='bold')
save('icons/derived', '#546E7A')

print("All icons saved.")
