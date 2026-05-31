"""Composite figure: 3 cost item pipeline sub-diagrams as a vertical panel."""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

PIPELINE = "/Users/davide/Documents/uni/ev-charging-cost-estimator/paper/figures/pipeline"

panels = [
    ("09_chargers.png",      "(a) Chargers — passthrough + lookup table"),
    ("05_transformer.png",   "(b) Transformer — linear sizing + lookup table"),
    ("14_mv_connection.png", "(c) MV Connection Cost — chained cost function"),
]

fig, axes = plt.subplots(3, 1, figsize=(14, 15))
for ax, (fname, title) in zip(axes, panels):
    img = mpimg.imread(f"{PIPELINE}/{fname}")
    ax.imshow(img)
    ax.set_title(title, fontsize=12, fontweight='bold', pad=6, loc='left')
    ax.axis('off')

plt.tight_layout(pad=1.5)
plt.savefig(
    "/Users/davide/Documents/uni/ev-charging-cost-estimator/paper/figures/Figure_composite_pipeline.png",
    dpi=150, bbox_inches='tight', facecolor='white'
)
print("Composite figure saved.")
