# Section 2 Rewrite + Pipeline Figures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite Sections 2.1 and 2.2 of paper.md to address reviewer comments #6, #7, #8 — shifting from file-listing prose to a layer + data-flow description, adding input-to-workflow mapping, adding key formulas, and replacing Figure 1 + Figure 7 slot with pipeline figures.

**Architecture:** The abstract pipeline figure (`pipeline_abstract.png`) replaces Figure 1. A composite of three cost-item sub-diagrams from `figures/pipeline/` becomes the new Figure 7 slot (placed in Section 2.2). Section 2.1 prose is rewritten around the three architectural layers and data flow. Section 2.2 groups inputs by function and adds the key cost formulas.

**Tech Stack:** Markdown (paper.md), Python/matplotlib (composite figure generation), Graphviz dot (already rendered).

---

## Files

| Action | Path | Responsibility |
|---|---|---|
| Modify | `paper/paper.md` lines 60–107 | Rewrite Sections 2.1 and 2.2, update figure captions |
| Create | `paper/figures/gen_composite_figure.py` | Generate composite 3-panel cost item figure |
| Create | `paper/figures/Figure_composite_pipeline.png` | The composite figure (output of above script) |
| Modify | `paper/review.md` | Mark comments #6, #7, #8 as ✅ DONE |

---

## Task 1: Generate the composite cost item figure

**Files:**
- Create: `paper/figures/gen_composite_figure.py`
- Create: `paper/figures/Figure_composite_pipeline.png`

- [ ] **Step 1: Write the generator script**

```python
# paper/figures/gen_composite_figure.py
"""Composite figure: 3 cost item pipeline sub-diagrams as a vertical panel."""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

PIPELINE = "/Users/davide/Documents/uni/ev-charging-cost-estimator/paper/figures/pipeline"

# Chosen examples: simple, medium-complexity, chained
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
```

- [ ] **Step 2: Run the script**

```bash
cd /Users/davide/Documents/uni/ev-charging-cost-estimator/paper/figures
python3 gen_composite_figure.py
```

Expected output: `Composite figure saved.`

- [ ] **Step 3: Verify the figure looks correct**

Open and inspect:
```bash
open /Users/davide/Documents/uni/ev-charging-cost-estimator/paper/figures/Figure_composite_pipeline.png
```

Check: three panels stacked vertically, each showing a clean pipeline from inputs to €, with labels (a), (b), (c).

---

## Task 2: Replace Figure 1 reference with abstract pipeline

**Files:**
- Modify: `paper/paper.md` lines 76–78

- [ ] **Step 1: Replace Figure 1 caption and reference in paper.md**

Find this block (around line 76–78):
```markdown
Figure 1: Software architecture overview.

*Figure 1: Software architecture overview.*
```

Replace with:
```markdown
![Figure 1](figures/pipeline_abstract.png)

*Figure 1: Data pipeline overview. User inputs feed the project type classifier and the electrical sizing layer in parallel. The project type (1–4) gates which sizing calculations are active. Sized electrical quantities (I, S, P, V) feed 15 cost functions, each producing one line item in euros.*
```

---

## Task 3: Rewrite Section 2.1

**Files:**
- Modify: `paper/paper.md` lines 60–78

- [ ] **Step 1: Replace the Section 2.1 content**

Find this entire block (lines 60–78):
```markdown
### 2.1 Software Architecture

> **[REVIEW]** I think the whole Software Architecture section looks like a description of the code organization than an actual software architecture section. Right now it mainly lists the files (app.py, calls.py, cost.py) and explains what each one does, but it does not really describe the architecture of the system itself.
>
> The figure helps to show the overall workflow, but it still feels quite high level/generic. Maybe the section could focus more explicitly on the software layers/components and how they interact. For example, describing the Streamlit front end as the presentation layer, calls.py as the orchestration/logic layer, and cost.py as the computational layer containing the engineering/cost models.
>
> It would also help to explain the data flow more clearly. Right now that flow is implied but not really discussed in detail.

The code is split into three files totaling about 1,800 lines (Figure 1):

- `**app.py`** (~995 lines): the Streamlit front end. Collects inputs, validates them, shows results as Plotly charts, and handles Excel/PDF export.
- `**utils/calls.py**` (~325 lines): the orchestration layer. Checks whether LV or MV upgrades are needed (`medium_requirement`, `hard_requirement`), picks the project type (`case_definition`), runs all 19 cost functions (`compute_all_costs`), and drives the sensitivity sweeps.
- `**utils/cost.py**` (~490 lines): the 19 cost functions themselves. Each takes a physical quantity (apparent power, current, cable length, or area) and returns a cost in 2024 euros, using lookup tables and fitted curves from industrial catalogs and published data.

In practice: the user fills in the input form; `calls.py` validates the inputs, determines the project type (1–4), and calls each relevant cost function with the right sizes; the results land in an itemized table and interactive charts.

Figure 1: Software architecture overview.

*Figure 1: Software architecture overview.*
```

Replace with:
```markdown
### 2.1 Software Architecture

The tool follows a three-layer architecture. The **presentation layer** (`app.py`, ~995 lines) collects the 16 user inputs through a Streamlit widget form, re-renders the interface on every change to enable or disable fields that depend on the current configuration, and displays results as interactive Plotly charts with Excel and PDF export. The **orchestration layer** (`utils/calls.py`, ~325 lines) validates inputs, runs `medium_requirement()` and `hard_requirement()` to check whether the existing grid connection can handle the planned load, calls `case_definition()` to assign one of four project types, and calls `compute_all_costs()` which dispatches to every relevant cost function. The **computational layer** (`utils/cost.py`, ~490 lines) contains 19 pure functions — each takes one or more physical quantities and returns a cost in 2024 euros using lookup tables or fitted curves from industrial catalogs and published studies.

Data flows through four stages, shown in Figure 1. The user's 16 input parameters feed the project type classifier and the electrical sizing calculations in parallel. The project type (1–4) gates which sizing calculations are active and which cost functions return non-zero values. The sized electrical quantities — current I [A], apparent power S [kVA], total power P [kW], and voltage V [kV] — feed 15 cost functions. Each cost function produces one line item in euros. Because Streamlit re-executes the entire script on every widget change, the classification and field-enable logic runs automatically on every interaction without any explicit callback wiring.

![Figure 1](figures/pipeline_abstract.png)

*Figure 1: Data pipeline overview. User inputs feed the project type classifier and the electrical sizing layer in parallel. The project type (1–4) gates which sizing calculations are active. Sized electrical quantities (I, S, P, V) feed 15 cost functions, each producing one line item in euros.*
```

---

## Task 4: Rewrite Section 2.2 — input grouping and workflow mapping

**Files:**
- Modify: `paper/paper.md` lines 80–107

- [ ] **Step 1: Replace the Section 2.2 input parameters block**

Find this block (starting at line 80):
```markdown
**Input parameters.** The user provides 13 numbers and 3 categorical choices: how many chargers, at what power, what voltage levels, the existing grid connection capacity, cable distances, the power factor, and site preparation details (land area, surface material, terrain). The form also asks about LV and MV connection specifics: transformer capacity, distances to the nearest transformer and MV access point, and safety margins. Fields that do not apply to the current configuration are grayed out automatically; for example, MV parameters only appear when the planned load exceeds what the existing connection can supply (Figure 2).

> **[REVIEW]** In this section needs to introduce the main functions of the software and formulas. What is written is configuration, that can be place in other section.
>
> **[REVIEW]** Also, is not clear what are the things that can be choosen, where they fit in the software work flow.
```

Replace with:
```markdown
**Input parameters.** The tool takes 13 numerical and 3 categorical inputs, grouped by their role in the calculation pipeline:

- **Charger parameters** — number of chargers *n*, power per charger *P* [kW], and load power factor *pf* — drive the planned apparent load calculation and appear in nearly every cost function.
- **Grid and connection parameters** — existing grid connection capacity *G* [kVA], LV level *V*_LV [V], MV level *V*_MV [kV], available transformer capacity [kVA], maximum LV connection power [kVA], transformer presence (yes/no), and transformer safety margin [%] — determine the project type and size the MV and LV electrical equipment.
- **Distance and site parameters** — cable distances from the rectifier to the chargers, from the premises to the nearest MV/LV transformer, and to the nearest MV access point [m], plus land area [m²], pavement material, and terrain type — determine cable costs and site preparation cost.

The planned apparent load is computed as S = n·P/pf [kVA]. This is compared against G: if S ≤ G, the existing connection is sufficient (Type 1). Otherwise, the uncovered load S − G is compared against the local LV threshold to determine whether a simple LV upgrade suffices (Type 2) or a new MV connection is needed (Types 3–4). Once the type is known, only the relevant cost components are activated — fields that do not apply are grayed out in the interface automatically (Figure 2).
```

- [ ] **Step 2: Add the key formulas block after Project Type Classification paragraph**

Find this text:
```markdown
**Investment cost model.** The model covers everything from the grid connection point to the charging plug (Figure 4) and computes 15 cost items through 19 functions in three groups.
```

Replace with:
```markdown
**Investment cost model.** The model covers everything from the grid connection point to the charging plug (Figure 4) and computes 15 cost items through 19 functions in three groups. Figure 7 shows three representative examples of how inputs flow through the pipeline to produce a cost in euros — from a simple passthrough (Chargers) to a linear sizing calculation (Transformer) to a chained function (MV Connection Cost, which takes the MV cable material cost as its own input).

The key intermediate calculations that size electrical components are:

| Quantity | Formula |
|---|---|
| Planned apparent load | S = n · P / pf [kVA] |
| LV current | I = n · P · 1000 / (√3 · V_LV) [A] |
| MV current (Type 3) | I = (n · P/pf − G) / (√3 · V_MV) [A] |
| MV current (Type 4) | I = (n · P/pf) / (√3 · V_MV) [A] |
| Transformer rating | S_T = (n · P/pf − G) · (1 + margin/100) [kVA] |
| Rectifier modules | k = ⌈n · P / 200⌉ |

The cost functions that map these quantities to euros are:

| Component | Formula type | Key formula |
|---|---|---|
| LV/DC cables | Linear | C = 0.276 · I · dist [€] |
| MV cables | Exponential | C = 53.976 · e^(0.0034 · I) · dist [€] |
| LV cabinet | Linear | C = 10.319 · I − 900.26 [€] |
| Rectifier | Step | C = k · 44,400 [€] |
| Transformer | Lookup table | S_T [kVA] → catalog price [€] |
| MV switchgear | Weighted linear | C = base + Σ w_i · x_i [€] |
| Surge arresters | Lookup table | V_MV [kV] → catalog price [€] |
| Charger planning | Linear | C = n · (25.064 · P + 275.07) [€] |
| Charger installation | Linear | C = n · (155.83 · P + 5822.5) [€] |
| Site preparation | Lookup table | C = A · r, r ∈ {45.2, 55.2, 150.6} [€/m²] |

```

- [ ] **Step 3: Add sensitivity analysis pipeline paragraph**

Find this block in Section 2.2:
```markdown
**Analysis modes.** Three modes are available. **Cost Breakdown** produces a full itemized table for the exact configuration, exportable to Excel. **Single-Variable Sensitivity** lets the user sweep one or more parameters across a range while holding everything else fixed; the result is a stacked bar chart showing how each component changes. **Two-Parameter Sensitivity** sweeps two parameters at once, displayed as a scatter plot color-coded by the second parameter, with full component breakdowns on hover.
```

Replace with:
```markdown
**Analysis modes.** Three modes are available. **Cost Breakdown** produces a full itemized table for the exact configuration, exportable to Excel. **Single-Variable Sensitivity** sweeps one parameter across a user-defined range while holding everything else fixed. Because the swept parameter passes through the full pipeline on every step, a change in — for example — number of chargers *n* can shift the project type mid-sweep (e.g., from Type 1 to Type 3 once the planned load exceeds the grid connection capacity), which in turn activates a different set of cost components; the resulting stacked bar chart makes these discontinuities visible. **Two-Parameter Sensitivity** sweeps two parameters at once and displays the results as a scatter plot color-coded by the second parameter, with full component breakdowns on hover. In both sensitivity modes, every evaluation re-runs the complete pipeline — project type classification, electrical sizing, and cost computation — so the output reflects the true non-linear response of the cost model to input variation.
```

- [ ] **Step 4: Add the composite figure reference at the end of Section 2.2**

After the **Export and deployment** paragraph, add:

```markdown
![Figure 7](figures/Figure_composite_pipeline.png)

*Figure 7: Three representative cost item pipelines. (a) Chargers: inputs n and P pass directly through a lookup table. (b) Transformer: six inputs drive a linear sizing calculation producing S [kVA], which indexes a catalog lookup table. (c) MV Connection Cost: a chained function that takes the MV cable material cost as input rather than raw electrical quantities.*
```

---

## Task 5: Update review.md — mark #6, #7, #8 as done

**Files:**
- Modify: `paper/review.md`

- [ ] **Step 1: Mark comment #6 as done**

Find:
```markdown
**Difficulty: ⭐⭐⭐ Medium**

> *"Also, is not clear what are the things that can be choosen, where they fit in the software work flow."*
```

Add `✅ DONE` after the difficulty line and add a Fix applied section at the end of comment #6:
```markdown
**Fix applied:** Grouped the 16 inputs into three functional categories (charger parameters, grid/connection parameters, distance/site parameters) in Section 2.2 and added a paragraph mapping the input-to-output flow: S = n·P/pf → project type (1–4) → active cost functions → aggregated cost. Figure 7 (composite pipeline sub-diagrams) makes the type → cost function link visual.
```

- [ ] **Step 2: Mark comment #7 as done**

Find:
```markdown
**Effort:** 2–3 hours. Rewrite ~half a page, possibly update Figure 1 to reflect the layer/flow framing.
```

Add fix description after the effort line:
```markdown
**Fix applied:** Rewrote Section 2.1 to describe three architectural layers (Presentation, Orchestration, Computational) with explicit data flow. Replaced Figure 1 (old file-listing diagram) with the abstract pipeline figure showing the four-stage data flow: User Inputs → Project Type → Sizing → Cost Functions → €.
```

- [ ] **Step 3: Mark comment #8 as done**

Find:
```markdown
**Effort:** 3–5 hours. Read all 19 functions, extract equations, typeset in the paper, verify each formula matches the code exactly, adjust surrounding prose.
```

Add fix description after the effort line:
```markdown
**Fix applied:** Added two formula tables to Section 2.2: one for the key sizing calculations (S, I, S_T, k) and one for the 10 cost functions mapping electrical quantities to euros. Also added Figure 7 (composite pipeline sub-diagrams) showing three concrete examples of the input-to-€ flow. Sub-task 8e (embed Figure C activation matrix) is superseded by Figure 7 which shows the same information more concretely through examples.
```

---

## Self-Review Checklist

- [x] **Spec coverage:** Comments #6 (input grouping + workflow mapping), #7 (architecture rewrite + Figure 1), #8 (formulas + Figure 7) all have tasks.
- [x] **Figure count:** Figure 1 replaced (not added), Figure 7 slot filled (not added) → stays at 6 figures.
- [x] **No placeholders:** All new prose written out in full, formula tables complete.
- [x] **Figure paths correct:** `figures/pipeline_abstract.png` exists; `figures/Figure_composite_pipeline.png` created in Task 1.
- [x] **Section 2.2 formula tables verified:** All formulas match `cost.py` functions read earlier in the session.
- [x] **Figure 7 citation in Section 3 already removed** in previous step — no dangling reference.
