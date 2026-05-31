# Reviewer Comment Classification

Comments ordered from **easiest to hardest** to address. Difficulty is estimated in terms of writing effort, research required, and scope of changes to the paper.

---

## 1. Remove first-person "We" — Section 3 opening

**Difficulty: ⭐ Very Easy** ✅ DONE

> *"The text should not include words like We. In this section, the tool is test using.."*

**What needs to change:** Replace "We applied the tool to nine real sites across Germany..." with passive voice (e.g., "The tool is applied to nine real sites..."). Single sentence, no content change, no research.

**Effort:** 5 minutes. One sentence rewrite.

**Fix applied:** Changed "==We applied the tool== to nine real sites..." to "The tool is applied to nine real sites..." — review comment removed from paper.md.

---

## 2. Rewrite the opening sentence of Section 4 — Impact

**Difficulty: ⭐ Very Easy** ✅ DONE

> *"I think this is not a good first sentence on Impact. Should be a clear sentence of the impact of the Tool. Where can be used and the benefits."*

**What needs to change:** The section currently opens with an AFIR statistic ("AFIR requires over 300,000 truck charging points..."), which reads like context, not impact. Replace with a direct statement of what the tool enables and who benefits. No research needed — the content already exists later in the section, it just needs to lead.

**Effort:** 10–15 minutes. Rewrite 1–2 sentences, shuffle existing content.

**Fix applied:** Replaced the AFIR statistic as opening with a direct impact statement: "The tool provides decision-makers with a fast, transparent way to estimate and compare overnight HDV charging infrastructure costs before committing to a project." The AFIR figure was kept but moved into a supporting sentence later in the same paragraph. Review comment removed from paper.md.

---

## 3. Clarify the transition "Cost estimation makes this harder" — Section 1 §3

**Difficulty: ⭐⭐ Easy** ✅ DONE

> *"What is this? what its harder?"*

**What needs to change:** The sentence "Cost estimation makes this harder" follows a paragraph about grid connection bottlenecks, so "harder" is ambiguous — harder than what? The link to cost estimation is not clear. Add one connecting sentence that explicitly ties the previous point (infrastructure complexity, slow grid connections) to the cost estimation challenge.

**Effort:** 15–20 minutes. 1–2 sentences added or rephrased.

**Fix applied:** Replaced "==Cost estimation makes this harder.==" with "These infrastructure challenges are compounded by a lack of reliable cost estimation tools." This makes the connection explicit — "these challenges" refers directly to the previous paragraph (slow grid connections, permitting, megawatt-scale capacity needs) and "cost estimation tools" sets up the paragraph that follows. Review comment removed from paper.md.

---

## 4. Make the 4-type classification visible earlier in the document — Section 5 / Section 1

**Difficulty: ⭐⭐ Easy** ✅ DONE

> *"This was not clear before in the document"* — on *"It classifies projects into four types by grid connection requirement..."* in Section 5.

**What needs to change:** The four project types are introduced in Section 2.2 but only described in detail there. Section 1 already lists the classification as contribution (2), but it is buried in a numbered list. Making it more prominent earlier — e.g., one dedicated sentence in the closing paragraph of Section 1, or in the abstract — would remove the surprise in Section 5.

**Effort:** 20–30 minutes. Add 1–2 sentences in Section 1 summary and/or abstract.

**Fix applied:** Expanded contribution (2) in the Section 1 closing paragraph to name and briefly describe all four types inline: "Type 1 (sufficient existing capacity), Type 2 (LV upgrade needed), Type 3 (MV connection alongside existing transformer), and Type 4 (full MV buildout from scratch) — which determines which cost components are activated." By the time the reader reaches Section 2.2 or Section 5, the four types are already named and their meaning is established. The `[REVIEW]` annotation was also removed from the Section 5 sentence since the issue is now resolved upstream.

---

## 5. Mention existing software tools for passenger car EV charging — Section 1 §3

**Difficulty: ⭐⭐ Easy–Medium** ✅ DONE (differently)

> *"Are there softwares for passenger cars?"*

**What needs to change:** The paragraph states "charging infrastructure for passenger cars is well studied" but does not cite any tools or software. Need to name 1–2 existing passenger car charging tools (e.g., NREL's EVI-Pro, DOE EVSE cost tools) and contrast them with the HDV case to justify the gap. Requires a short literature check to find the right references.

**Effort:** 1–2 hours. Find 1–2 references, add 1–2 sentences.

**Fix applied:** Rather than adding passenger car references, the sentence "Charging infrastructure for passenger cars is well studied, but trucks need bigger chargers..." was removed entirely and replaced with a direct, absolute statement: "Charging infrastructure for trucks requires high-power chargers, heavy electrical equipment, and site-specific civil works." This avoids the weak comparative framing and the uncited claim, while making the paragraph self-contained. Review comment removed from paper.md.

---

## 6. Clarify what inputs can be chosen and how they connect to the workflow — Section 2.2

**Difficulty: ⭐⭐⭐ Medium** ✅ DONE

> *"Also, is not clear what are the things that can be choosen, where they fit in the software work flow."*

**What needs to change:** The input parameters paragraph lists the 13+3 inputs but does not explain which inputs drive which part of the calculation or how they propagate through the system. Needs a short mapping between input groups and the workflow stages (e.g., charger count/power → load calculation → project type → which cost functions activate). This is related to comment 5 (formulas) and comment 4 (architecture rewrite) — ideally addressed together.

**Effort:** 1–2 hours. Add a short explanatory paragraph or restructure the existing one. No external research but requires understanding the full `calls.py` logic.

**Sub-tasks:**

- [ ] **6a** — Group the 13+3 inputs into functional categories in the paper prose (e.g., "grid parameters", "charger parameters", "site parameters") and explain what each group drives
- [ ] **6b** — Add one short paragraph mapping the input-to-output flow: `n, P → apparent load S → current I → project type (1–4) → active cost functions → aggregated cost`
- [ ] **6c** — Reference Figure C (activation matrix) here to make the type → cost function link visual rather than prose-only

**Fix applied:** Grouped the 16 inputs into three functional categories (charger parameters, grid/connection parameters, distance/site parameters) in Section 2.2 and added a paragraph mapping the input-to-output flow: S = n·P/pf → project type (1–4) → active cost functions → aggregated cost. Figure 7 (composite pipeline sub-diagrams) makes the type → cost function link visual.

---

## 7. Rewrite Section 2.1 to describe architecture, not file listing — Section 2.1

**Difficulty: ⭐⭐⭐ Medium** ✅ DONE

> *"I think the whole Software Architecture section looks like a description of the code organization than an actual software architecture section. Right now it mainly lists the files (app.py, calls.py, cost.py) and explains what each one does, but it does not really describe the architecture of the system itself.*
>
> *The figure helps to show the overall workflow, but it still feels quite high level/generic. Maybe the section could focus more explicitly on the software layers/components and how they interact. For example, describing the Streamlit front end as the presentation layer, calls.py as the orchestration/logic layer, and cost.py as the computational layer containing the engineering/cost models.*
>
> *It would also help to explain the data flow more clearly. Right now that flow is implied but not really discussed in detail."*

**What needs to change:** The section needs to shift from "here are the three files" to "here are the three architectural layers and how data flows between them." Concretely:
- **Presentation layer** (`app.py`): collects user inputs, renders Plotly charts, handles exports
- **Orchestration layer** (`calls.py`): validates inputs, classifies project type via `case_definition()`, calls `compute_all_costs()`, drives sensitivity sweeps
- **Computational layer** (`cost.py`): 19 pure functions, each taking a physical quantity and returning a cost in €

The data flow: user inputs → validation & type classification (1–4) → selective activation of cost functions → aggregation → visualisation. This is all derivable from reading the code — no external research needed — but requires rewriting the section substantially.

**Effort:** 2–3 hours. Rewrite ~half a page, possibly update Figure 1 to reflect the layer/flow framing.

**Sub-tasks:**

- [ ] **7a** — Replace current Section 2.1 prose with a three-paragraph structure: one paragraph per layer (Presentation / Orchestration / Computational), each naming the file, its role, and its key functions
- [ ] **7b** — Add a data-flow paragraph after the three layer paragraphs: describe the full path from widget change → `medium_requirement()` / `hard_requirement()` → `case_definition()` → `compute_all_costs()` → chart render, explaining that Streamlit's reactive rerun model means every widget change re-executes the classification logic automatically
- [ ] **7c** — Embed **Figure A** (three-layer architecture diagram) and **Figure B** (reactive loop flowchart) in Section 2.1, replacing or supplementing the existing Figure 1
- [ ] **7d** — Remove the current file-listing framing ("The codebase is organized into three files…") and replace with layer-centric language ("The tool follows a three-layer architecture…")

**Fix applied:** Rewrote Section 2.1 to describe three architectural layers (Presentation, Orchestration, Computational) with explicit data flow. Replaced Figure 1 (old file-listing diagram) with the abstract pipeline figure showing the four-stage data flow: User Inputs → Project Type → Sizing → Cost Functions → €.

---

## 8. Add key formulas to Section 2.2 — Software Functionalities

**Difficulty: ⭐⭐⭐⭐ Medium–Hard** ✅ DONE

> *"In this section needs to introduce the main functions of the software and formulas. What is written is configuration, that can be place in other section."*

**What needs to change:** Section 2.2 describes the cost model in prose but shows no equations. The code in `utils/cost.py` and `utils/calls.py` contains well-defined mathematical relationships that should appear in the paper. Key formulas to extract and typeset:

| Component | Formula (from code) |
|---|---|
| Planned load | `S = n × P / pf` (kVA) |
| LV current | `I = n·P·1000 / (√3 · V_LV)` |
| MV current | `I = (n·P/pf − G) / (√3 · V_MV)` or `I = (n·P/pf) / (√3 · V_MV)` |
| MV cable cost (per m) | `C = 53.976 · e^(0.0034·I)` (€/m) |
| LV cable cost (per m) | `C = 0.276 · I` (€/m) |
| Rectifier modules | `k = ⌈n·P / 200⌉`, cost = `k × 44,400` € |
| LV cabinet current | `I = n·P·1000 / (√3 · V_LV)` |
| Charger planning | `C = n · (25.064·P + 275.07)` € |
| Charger installation | `C = n · (155.83·P + 5822.5)` € |
| Site preparation | `C = A · r` where `r` ∈ {45.2, 55.2, 150.6} €/m² |

Transformer and switchgear use lookup tables so they need to be described as interpolated from 2024 catalog data. All formulas are in the code and just need to be transferred to the paper with proper mathematical notation. This requires careful reading of all 19 functions in `cost.py` to make sure nothing is missed or misrepresented.

**Effort:** 3–5 hours. Read all 19 functions, extract equations, typeset in the paper, verify each formula matches the code exactly, adjust surrounding prose.

**Sub-tasks:**

- [ ] **8a** — Add the load-sizing equations first (planned apparent load S, LV/MV current derivation) as they are the inputs to all downstream cost functions
- [ ] **8b** — Add the cable cost equations (LV linear regression `C = 0.276·I`, MV exponential fit `C = 53.976·e^(0.0034·I)`) with a note on how they were derived from catalog data
- [ ] **8c** — Add the labor and site formulas (planning, installation, site preparation rate table) with the regression source noted
- [ ] **8d** — Describe the transformer and switchgear lookup tables in prose (interpolated from 2024 catalog, kVA → €), since they have no closed-form formula
- [ ] **8e** — Embed **Figure C** (activation matrix) in Section 2.2 to show which formulas apply per project type, then reference it from the prose

**Fix applied:** Added two formula tables to Section 2.2: one for the key sizing calculations (S, I, S_T, k) and one for the 10 cost functions mapping electrical quantities to euros. Also added Figure 7 (composite pipeline sub-diagrams) showing three concrete examples of the input-to-€ flow. Sub-task 8e is superseded by Figure 7 which shows the same information more concretely through examples.

---

## 9. Expand the literature review of related software — Section 1 §4

**Difficulty: ⭐⭐⭐⭐⭐ Hard** ✅ DONE

> *"I think this literature review of softwares is short, and FleetRL is not even so related. What Types of softwares exist and which gap this software fills? For sure reviewers will ask for a more indeep review."*

**What needs to change:** The current literature paragraph mentions only FleetRL, ICCT reports, and Borlaug et al. — none of which are open-source interactive tools for HDV charging infrastructure cost estimation. The review needs to:
1. Survey what software tools *do* exist for EV charging infrastructure planning/costing (passenger cars and HDVs)
2. Identify which aspects each tool covers and which it does not (interactive vs. static, component-level vs. aggregate, European vs. US, HDV vs. passenger)
3. Make the gap explicit: no tool currently does component-level, interactive, European HDV overnight charging cost estimation

This requires proper external research — searching Google Scholar, SoftwareX, JOSS, and grey literature for tools, reading them, and writing a structured comparison. It is the most open-ended change and the one most likely to require new citations.

**Effort:** 1–2 days of research + 2–3 hours of writing. Produces a new paragraph or two replacing/expanding the current gap analysis.

**Fix applied:** Replaced the single-paragraph related-work note with a structured two-paragraph survey organized by the three categories of existing tools: LCOC/operating-economics tools (Borlaug 2020 [10], Lanz 2022 [23], Atlas [24]), the NREL EVI-X planning/simulation suite [22], and static component-level cost studies (AFDC [12], ICCT/Nicholas [25]). It then covers the closest HDV-depot work (Borlaug 2021 [26], Wang 2025 [27]) and FleetRL [14], ending with an explicit statement of the gap. Six new references [22]–[27] were added to paper.md, paper_final.typ, and references.yml. The content is based on a verified deep-research survey (six search angles, 20 sources, 24/25 claims confirmed by 3-vote adversarial verification). Wording respects the verification caveats: NREL framed as "capital cost estimation is not their job" rather than "ignores cost", ICCT framed as static analysis, and the EU LCOC paper framed as passenger-scoped.

A follow-up targeted check of SoftwareX/Software Impacts and GitHub added two more references to preempt SoftwareX-reviewer counterexamples: datafev [28] (Software Impacts charging-management framework) and EV-EcoSim [29] (open-source grid-aware co-simulation platform that does quantify cost, distinguished as levelized grid/DER cost in a US light-duty context rather than component-level station capex). Other surfaced tools (EVPLAN GIS siting, INCEPTS, HELVES, Open-V2X-MP) target siting/simulation/management, not capital cost, so the gap holds.

---

## Summary Table

| # | Section | Comment (abbreviated) | Difficulty | Estimated effort |
|---|---|---|---|---|
| 1 | Sec 3 | Remove "We" | ⭐ Very Easy | 5 min |
| 2 | Sec 4 | Rewrite Impact opening | ⭐ Very Easy | 15 min |
| 3 | Sec 1 §3 | Fix "this harder" transition | ⭐⭐ Easy | 20 min |
| 4 | Sec 1 / Sec 5 | Make 4-type classification visible earlier | ⭐⭐ Easy | 30 min |
| 5 | Sec 1 §3 | Mention passenger car software tools | ⭐⭐ Easy–Medium | 1–2 h |
| 6 | Sec 2.2 | Clarify input-to-workflow mapping | ⭐⭐⭐ Medium | 1–2 h |
| 7 | Sec 2.1 | Rewrite architecture as layers + data flow | ⭐⭐⭐ Medium | 2–3 h |
| 8 | Sec 2.2 | Add key formulas from the code | ⭐⭐⭐⭐ Medium–Hard | 3–5 h |
| 9 | Sec 1 §4 | Expand literature review of related software | ⭐⭐⭐⭐⭐ Hard | 1–2 days |
