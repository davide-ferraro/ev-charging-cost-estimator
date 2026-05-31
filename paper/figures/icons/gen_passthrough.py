"""Passthrough icon: value passes through unchanged."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

W, H = 1.4, 1.1
DPI  = 90

fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

# Input label
ax.text(0.08, 0.55, 'x', ha='center', va='center', fontsize=13,
        color='#546E7A', fontweight='bold')

# Arrow straight through
ax.annotate('', xy=(0.88, 0.55), xytext=(0.18, 0.55),
            arrowprops=dict(arrowstyle='->', color='#546E7A', lw=2.5))

# "=" sign in the middle
ax.text(0.53, 0.55, '=', ha='center', va='center', fontsize=14,
        color='#546E7A', fontweight='bold')

# Output label
ax.text(0.94, 0.55, 'x', ha='center', va='center', fontsize=13,
        color='#546E7A', fontweight='bold')

plt.tight_layout(pad=0.1)
plt.savefig('passthrough.png', dpi=DPI, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("Passthrough icon saved.")
