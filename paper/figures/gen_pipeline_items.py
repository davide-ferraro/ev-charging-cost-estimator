"""Generate one pipeline sub-diagram per cost item."""
import subprocess, os, textwrap

ICONS = "/Users/davide/Documents/uni/ev-charging-cost-estimator/paper/figures/icons"
OUT   = "/Users/davide/Documents/uni/ev-charging-cost-estimator/paper/figures/pipeline"
os.makedirs(OUT, exist_ok=True)

# ── Node catalogues ────────────────────────────────────────────────────────
ALL_INPUTS = {
    'I1':  "Number of chargers (n)",
    'I2':  "Power per charger (P) [kW]",
    'I3':  "LV level (V_LV) [V]",
    'I4':  "Grid connection capacity (G) [kVA]",
    'I5':  "Distance rectifier→chargers [m]",
    'I6':  "Load Power Factor (pf)",
    'I7':  "Max LV connection power [kVA]",
    'I8':  "Available MV/LV transformer capacity [kVA]",
    'I9':  "Distance to MV/LV transformer [m]",
    'I10': "MV level (V_MV) [kV]",
    'I11': "Transformer safety margin [%]",
    'I12': "Distance to MV access point [m]",
    'I13': "Land area [m²]",
    'I14': "Transformer present on premises?",
    'I15': "Pavement material",
    'I16': "Land type",
}
PT_INPUTS = ['I1','I2','I4','I6','I7','I8','I14']

SIZING_INFO = {
    'S1':  ("LV Cabinet",             "linear",      "I = n·P/(√3·V_LV)"),
    'S2':  ("DC Cables",              "linear",      "I = n·P/(V·V_LV)"),
    'S3':  ("LV Distribution Cables", "linear",      "I = (n·P/pf−G)/(√3·V_LV)"),
    'S4':  ("MV Cables",              "linear",      "I = (n·P/pf−G)/(√3·V_MV)"),
    'S5':  ("Transformer",            "linear",      "S = (n·P/pf−G)·(1+m)"),
    'S6':  ("MV Switchgear",          "linear",      "I = (n·P/pf−G)/(√3·V_MV)"),
    'S7':  ("Surge Arresters",        "passthrough", "passes V_MV [kV]"),
    'S8':  ("Grounding Resistors",    "passthrough", "passes V_MV [kV]"),
    'S9':  ("Rectifier",              "ceiling",     "k = ⌈n·P / 200⌉"),
    'S10': ("Chargers",               "passthrough", "passes P [kW]"),
}
CF_INFO = {
    'CF1':  ("Charger Cost",             "lut",         "P [kW] → €",             "#FFF8E1","#F57F17"),
    'CF2':  ("Rectifier Cost",           "ceiling",     "⌈n·P/200⌉ → €",         "#F3E5F5","#6A1B9A"),
    'CF3':  ("LV Cabinet Cost",          "linear",      "I [A] → €",              "#E8EAF6","#283593"),
    'CF4':  ("DC Cables Cost",           "linear",      "I [A], dist → €",        "#E8EAF6","#283593"),
    'CF5':  ("LV Cables Cost",           "linear",      "I [A], dist → €",        "#E8EAF6","#283593"),
    'CF6':  ("MV Cables Cost",           "exponential", "I [A], dist → €",        "#FCE4EC","#880E4F"),
    'CF7':  ("Transformer Cost",         "lut",         "S [kVA] → €",            "#FFF8E1","#F57F17"),
    'CF8':  ("Switchgear Cost",          "weighted",    "I [A], V [kV] → €",      "#E0F2F1","#00695C"),
    'CF9':  ("Surge Arresters Cost",     "lut",         "V [kV] → €",             "#FFF8E1","#F57F17"),
    'CF10': ("Grounding Resistors Cost", "lut",         "V [kV] → €",             "#FFF8E1","#F57F17"),
    'CF11': ("Planning Cost",            "linear",      "n, P → €",               "#E8EAF6","#283593"),
    'CF12': ("Installation Cost",        "linear",      "n, P, Type → €",         "#E8EAF6","#283593"),
    'CF13': ("LV Connection Cost",       "linear",      "LV cable cost → €",      "#E8EAF6","#283593"),
    'CF14': ("MV Connection Cost",       "derived",     "MV cable cost, dist → €","#ECEFF1","#546E7A"),
    'CF15': ("Site Preparation Cost",    "lut",         "area, material → €",     "#FFF8E1","#F57F17"),
}

# ── Cost item definitions ──────────────────────────────────────────────────
# Each entry: (filename, output_label, sizing_id, sizing_out_label, sizing_out_color,
#              cf_id, inputs_to_sizing, extra_inputs_to_cf, use_pt, chained_cf)
# inputs_to_sizing = inputs that go to the sizing box
# extra_inputs_to_cf = inputs that go DIRECTLY to the CF (distances, etc.)
# use_pt = True/False
ITEMS = [
    ("01_lv_cabinet",         "LV cabinet",
     'S1', "I [A]", "#1565C0",
     'CF3', ['I1','I2','I3'], [], False, None),

    ("02_cables_lvdc",        "Cables LVDC (Rectifier-Chargers)",
     'S2', "I [A]", "#1565C0",
     'CF4', ['I1','I2','I3','I5'], ['I5'], False, None),

    ("03_cables_lvac",        "Cables LVAC (Distribution-Site)",
     'S3', "I [A]", "#1565C0",
     'CF5', ['I1','I2','I3','I4','I6','I9'], ['I9'], True, None),

    ("04_cables_mvac",        "Cables MVAC (Distribution-Site)",
     'S4', "I [A]", "#1565C0",
     'CF6', ['I1','I2','I4','I6','I10','I12'], ['I12'], True, None),

    ("05_transformer",        "Transformer",
     'S5', "S [kVA]", "#E65100",
     'CF7', ['I1','I2','I4','I6','I11'], [], True, None),

    ("06_switchgear",         "Switchgear",
     'S6', "I [A], V [kV]", "#1565C0",
     'CF8', ['I1','I2','I4','I6','I10'], ['I10'], True, None),

    ("07_surge_arresters",    "Surge Arresters",
     'S7', "V [kV]", "#6A1B9A",
     'CF9', ['I10'], [], True, None),

    ("08_grounding_resistors","Grounding Resistors",
     'S8', "V [kV]", "#6A1B9A",
     'CF10', ['I10'], [], True, None),

    ("09_chargers",           "Chargers",
     'S10', "P [kW]", "#2E7D32",
     'CF1', ['I1','I2'], [], False, None),

    ("10_rectifier",          "Rectifier",
     'S9', "P [kW]", "#2E7D32",
     'CF2', ['I1','I2'], [], False, None),

    ("11_planning",           "Planning",
     None, None, None,
     'CF11', [], ['I1','I2'], False, None),

    ("12_installation",       "Installation",
     None, None, None,
     'CF12', [], ['I1','I2'], True, None),

    ("13_lv_connection",      "LV connection cost",
     'S3', "I [A]", "#1565C0",
     'CF5', ['I1','I2','I3','I4','I6','I9'], ['I9'], True, 'CF13'),

    ("14_mv_connection",      "MV connection cost",
     'S4', "I [A]", "#1565C0",
     'CF6', ['I1','I2','I4','I6','I10','I12'], ['I12'], True, 'CF14'),

    ("15_site_preparation",   "Site preparation",
     None, None, None,
     'CF15', [], ['I13','I15','I16'], False, None),
]

# ── DOT builders ───────────────────────────────────────────────────────────
def input_node(iid):
    return (f'    {iid} [label="{ALL_INPUTS[iid]}", '
            f'fillcolor="#BBDEFB", color="#1565C0"]\n')

def sizing_node(sid):
    lbl, icon, formula = SIZING_INFO[sid]
    return (f'    {sid} [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">'
            f'<TR><TD><IMG SRC="{ICONS}/{icon}.png"/></TD></TR>'
            f'<TR><TD ALIGN="CENTER"><B>{lbl}</B></TD></TR>'
            f'<TR><TD ALIGN="CENTER">{formula}</TD></TR>'
            f'</TABLE>>, shape=box, fillcolor="#FFE0B2", color="#E65100"]\n')

def cf_node(cfid):
    lbl, icon, formula, fc, c = CF_INFO[cfid]
    return (f'    {cfid} [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">'
            f'<TR><TD><IMG SRC="{ICONS}/{icon}.png"/></TD></TR>'
            f'<TR><TD ALIGN="CENTER"><B>{lbl}</B></TD></TR>'
            f'<TR><TD ALIGN="CENTER">{formula}</TD></TR>'
            f'</TABLE>>, shape=box, fillcolor="{fc}", color="{c}"]\n')

def eur_node(eurid, label):
    return (f'    {eurid} [label="€  {label}", shape=box, '
            f'fillcolor="#E8F5E9", color="#2E7D32", '
            f'fontname="Helvetica Bold", fontsize=11]\n')

def gen_dot(fname, out_label, sid, s_out_lbl, s_out_col,
            cfid, inputs_to_s, extra_to_cf, use_pt, chained):
    """Build and return the full dot source for one cost item."""

    # collect all input nodes to show
    all_shown_inputs = set(inputs_to_s) | set(extra_to_cf)
    if use_pt:
        all_shown_inputs |= set(PT_INPUTS)

    # which inputs go to PT (those in PT_INPUTS that are shown)
    pt_inputs = [i for i in PT_INPUTS if i in all_shown_inputs] if use_pt else []

    has_sizing = sid is not None

    lines = []
    lines.append('digraph item {')
    lines.append('    rankdir=LR')
    lines.append('    splines=true')
    lines.append('    nodesep=0.5')
    lines.append('    ranksep=1.8')
    lines.append('    node [shape=box, style=filled, fontname="Helvetica", fontsize=11, margin="0.12,0.08"]')
    lines.append('    edge [fontname="Helvetica", fontsize=10]')
    lines.append('')

    # title
    lines.append(f'    TITLE [shape=none, label="{out_label}", '
                 f'fontname="Helvetica Bold", fontsize=16, fontcolor="#263238"]')
    lines.append('')

    # ── User Inputs cluster
    lines.append('    subgraph cluster_inputs {')
    lines.append('        label="User Inputs"')
    lines.append('        fontname="Helvetica Bold"')
    lines.append('        fontsize=13')
    lines.append('        fontcolor="#1565C0"')
    lines.append('        color="#1565C0"')
    lines.append('        style=rounded')
    lines.append('        bgcolor="#E3F2FD"')
    for iid in sorted(all_shown_inputs):
        lines.append('    ' + input_node(iid).strip())
    lines.append('    }')
    lines.append('')

    # ── Project Type cluster (if needed)
    if use_pt:
        lines.append('    subgraph cluster_pt {')
        lines.append('        label="Project Type"')
        lines.append('        fontname="Helvetica Bold"')
        lines.append('        fontsize=13')
        lines.append('        fontcolor="#2E7D32"')
        lines.append('        color="#2E7D32"')
        lines.append('        style=rounded')
        lines.append('        bgcolor="#E8F5E9"')
        lines.append('        PT [label="Project Type\\nClassification\\n(Type 1/2/3/4)", '
                     'fillcolor="#A5D6A7", color="#2E7D32", fontname="Helvetica Bold", fontsize=10]')
        lines.append('    }')
        lines.append('')

    # ── Electrical Sizing cluster (if needed)
    if has_sizing:
        lines.append('    subgraph cluster_sizing {')
        lines.append('        label="Sizing Calculations"')
        lines.append('        fontname="Helvetica Bold"')
        lines.append('        fontsize=13')
        lines.append('        fontcolor="#E65100"')
        lines.append('        color="#E65100"')
        lines.append('        style=rounded')
        lines.append('        bgcolor="#FFF8E1"')
        lines.append('    ' + sizing_node(sid).strip())
        lines.append('    }')
        lines.append('')

    # ── Cost Functions cluster
    lines.append('    subgraph cluster_cf {')
    lines.append('        label="Cost Functions"')
    lines.append('        fontname="Helvetica Bold"')
    lines.append('        fontsize=13')
    lines.append('        fontcolor="#4527A0"')
    lines.append('        color="#4527A0"')
    lines.append('        style=rounded')
    lines.append('        bgcolor="#EDE7F6"')
    lines.append('    ' + cf_node(cfid).strip())
    if chained:
        lines.append('    ' + cf_node(chained).strip())
    lines.append('    }')
    lines.append('')

    # ── € output node(s)
    lines.append(eur_node('EUR', out_label))
    lines.append('')

    # ── Edges: inputs → PT
    for iid in pt_inputs:
        lines.append(f'    {iid} -> PT [color="#546E7A"]')

    # ── Edges: inputs → sizing
    for iid in inputs_to_s:
        if has_sizing:
            lines.append(f'    {iid} -> {sid} [color="#546E7A"]')

    # ── Edges: PT → sizing (dashed)
    if use_pt and has_sizing:
        lines.append(f'    PT -> {sid} [color="#2E7D32", style=dashed, penwidth=1.5]')

    # ── Edges: sizing → CF (colored by output quantity)
    if has_sizing and s_out_lbl:
        lines.append(f'    {sid} -> {cfid} [label="{s_out_lbl}", '
                     f'color="{s_out_col}", fontcolor="{s_out_col}", penwidth=2]')

    # ── Edges: extra inputs → CF (dashed)
    for iid in extra_to_cf:
        lines.append(f'    {iid} -> {cfid} [color="#546E7A", style=dashed]')

    # ── Edges: PT → CF (dashed, case gates)
    if use_pt:
        lines.append(f'    PT -> {cfid} [color="#2E7D32", style=dashed, penwidth=1.5]')

    # ── Chained CF
    if chained:
        lines.append(f'    {cfid} -> {chained} [label="cost [€]", '
                     f'color="#880E4F", fontcolor="#880E4F", penwidth=2]')
        if use_pt:
            lines.append(f'    PT -> {chained} [color="#2E7D32", style=dashed, penwidth=1.5]')
        # dist_mv also goes to CF14
        if chained == 'CF14' and 'I12' in all_shown_inputs:
            lines.append(f'    I12 -> {chained} [color="#546E7A", style=dashed]')
        lines.append(f'    {chained} -> EUR [color="#2E7D32", penwidth=2]')
    else:
        lines.append(f'    {cfid} -> EUR [color="#2E7D32", penwidth=2]')

    lines.append('}')
    return '\n'.join(lines)

# ── Generate all ───────────────────────────────────────────────────────────
for item in ITEMS:
    fname, out_label, sid, s_out_lbl, s_out_col, cfid, inputs_to_s, extra_to_cf, use_pt, chained = item
    dot_src = gen_dot(fname, out_label, sid, s_out_lbl, s_out_col,
                      cfid, inputs_to_s, extra_to_cf, use_pt, chained)
    dot_path = os.path.join(OUT, f'{fname}.dot')
    png_path = os.path.join(OUT, f'{fname}.png')
    with open(dot_path, 'w') as f:
        f.write(dot_src)
    result = subprocess.run(
        ['dot', '-Tpng', f'-Gdpi=150', dot_path, '-o', png_path],
        capture_output=True, text=True
    )
    status = "✓" if result.returncode == 0 else f"✗ {result.stderr[:80]}"
    print(f"{fname}: {status}")
