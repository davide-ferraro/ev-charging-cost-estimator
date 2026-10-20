# Round 5 — Official SoftwareX Reviewer Comments + Software Test Report (Oct 2026)

First round from the journal's own reviewers after the 2 Aug 2026 submission. Raw inputs in
`review/round5/`: `reviewer_comments_raw.md` (verbatim, typos preserved),
`EV Charging Cost Software_TestFeedbacks.docx` + `test_screenshots/` (software test report, 4 bugs).

**Targets:** `paper/paper_final.typ`, `paper/references.yml`, figure generator
`paper/figures/gen_pipeline_items.py`, and the code `utils/calls.py`, `utils/cost.py`, `app.py`.
Reviewer figure numbers refer to the compiled PDF: "Figure 4" = `<fig5>` label
(`fig5_pipeline_examples.png`, three cost-item pipelines (a)(b)(c)).

Reference numbers as printed in the submitted PDF: [6] ICCT 2022 `icct_costs`, [8] McKinsey/Broer
`mckinsey_charging`, [11] Burton NREL 2020 `burton_ev`, [17] `expert_interviews`,
[22] `nrel_evix`.

One task per reviewer item. Status ☐ TODO / ✅ DONE.

**Writing-style rule for every prose edit (Davide, 2026-10-20):** match the existing text of
`paper_final.typ` exactly in register and rhythm. Before writing, reread the paragraph before and
after the insertion point. No em dashes, no AI vocabulary (comprehensive, robust, leverage,
seamless, crucial, pivotal, delve, foster, "it is worth noting"), no significance inflation, no
three-item rhetorical lists, no sentence that summarizes what was just said. Plain declarative
sentences, concrete numbers, the same terminology already used (project type, cost function,
planned load, grid connection capacity). Show before/after to Davide for every sentence added.

---

## A. Reviewer 2 (Sept 18)

### A1. Simultaneity factor of charging processes — MAJOR
**Difficulty: ⭐⭐⭐⭐** ✅ DONE · _tool + paper §2.2 + §1 + §5_
> *"There is no consideration of the simultaneity of charging processes. [...] In my view, there should be a simultaneity factor taken into account in the cost structure."*

**What needs to change:** Today planned load = n × P / PF everywhere (`case_definition`,
`medium_requirement`, `hard_requirement`, transformer, switchgear, cables, rectifier sizing).
No way to express managed/smart charging reducing the coincident peak.
**Proposed solution (preferred):** add one user input *Simultaneity factor* (0.1–1.0, default 1.0,
help text explaining managed charging), multiply the coincident load n·P·f in project-type
classification and in every grid-side sizing step (transformer, switchgear, MV/LV cables,
connection fees). Charger-side items (chargers, planning, installation, rectifier-to-charger
cables) stay per plug. Document it in §2.2 (inputs table + sizing paragraph), one sentence in §1
motivation, and cite 1–2 depot energy-management papers (Borlaug 2021 [26] is already there).
Add to sensitivity-analysis parameter list so the reviewer's point (cost reduction from
management) can be demonstrated; optionally one sentence of results in §3.
**Alternative:** rebuttal only (overnight depot = worst-case simultaneous charging by design)
and future work. Weaker; reviewer marked it major.
**Effort:** 3–5 h code + tests, 1–2 h paper.
**Fix applied:** Code: new input "Simultaneity factor" (0.1–1.0, step 0.05, default 1.0, tooltip) in `app.py`; `case_definition`, `medium_requirement`, `hard_requirement` and the grid-side cost functions (LV/MV distribution cables, transformer, switchgear) use coincident power P·f; charger-side items unchanged; added to both sensitivity ranges. 3 tests (default reproduces old results exactly; 0.5 turns a Type 3 into Type 1; grid-side-only scaling). Commit c9d9f72. Paper: §1 contribution paragraph (one sentence), §1 after Burton [11] (managed charging sentence citing [26]), §2.2 inputs "14 numerical", charger parameters sentence, planned-load paragraph (S = f·n·P/pf, default/worst case, what is and is not scaled), project-type paragraph, Table 2 rows rewritten in terms of S. Approved by Davide before applying.

### A2. No page numbering
**Difficulty: ⭐** ✅ DONE · _global_
> *"there is not page numbering"*
**Proposed solution:** `#set page(numbering: "1")` in the Typst preamble.
**Fix applied:** `numbering: "1"` added to `#set page`.

### A3. Figure 4 not readable (shared with B5)
**Difficulty: ⭐⭐⭐** ✅ DONE · see B5.

---

## B. Second reviewer ("Reviewer Comments, CHARGE-IT")

### B1. Why "overnight"? Can the station be used daytime / en-route?
**Difficulty: ⭐⭐** ✅ DONE · _§1 or §2.2_
> *"additional explanation around the emphasis on overnight charging [...] is that the case? A sentence addressing this question or further emphasizing the decision-making around sizing [...] would be useful."*
**Proposed solution:** 2–3 sentences: the hardware costed is not restricted to night use; the
overnight framing drives the design assumptions (long dwell → 20–100 kW per plug, all vehicles
parked and plugged simultaneously, which is why the default simultaneity is 1.0; see A1). Ties
to European HDV duty cycles and the 9 h rest period (EU 561/2006). Mention MCS/en-route as out
of scope (already partly in Conclusions).
**Fix applied:** Via B5. §1 contribution paragraph: three sentences (hardware not tied to time of day; overnight = design case, rest period ≥ 9 h under Regulation (EC) 561/2006, 20–100 kW per plug, 10–350 kW range, MCS out of scope). New reference [30] `eu_driving_time`. Approved by Davide.

### B2. Reference HOMER and XENDEE as complex commercial alternatives
**Difficulty: ⭐⭐** ✅ DONE · _§1 related-software paragraph_
> *"reference one additional set of similarly intentioned but much more complex tools: HOMER and XENDEE [...] emphasize the value of the CHARGE-IT tool in terms of being no cost, accessible, and easy-to-use"*
**Proposed solution:** one or two sentences + 2 new `references.yml` entries (HOMER Pro / HOMER
Grid, XENDEE). Word budget is fine (≈3330/4000).
**Fix applied:** Two sentences added in §1 after the EV-EcoSim sentence; new refs HOMER Pro (UL Solutions) and XENDEE. Approved by Davide.

### B3. Modularity also matters to fleet operators (cost functions updatable) — say it earlier
**Difficulty: ⭐⭐** ✅ DONE · _§1 contribution paragraph or §2.1_
> *"if Cost Functions can be updated as costs change, that helps maintain the tool's relevance over time. If this is something that is in fact feasible, the authors should mention it higher up"*
**Proposed solution:** It is feasible: all price tables are plain dicts in `cost.py`. Add a
sentence in §1/§2.1, and make it true in practice: move price tables into one clearly named
place (or at least document "how to update prices" in README/docs). Keep §4 Impact sentence.
**Fix applied:** One sentence at the end of the §2.1 architecture paragraph (prices live in lookup tables and fitted coefficients in cost.py, replaceable without touching the rest). §4 researcher paragraph kept. Approved by Davide.

### B4. Citation numbering not in order of appearance
**Difficulty: ⭐⭐** ✅ DONE · _bibliography_
> *"the citation numbers do not correspond to their order of appearance in the text"*
**Proposed solution:** check the `#bibliography(style: ...)` call; switch to a numeric style
that orders by first citation (e.g. Typst `ieee` or Elsevier numeric), verify the list order
after compile.
**Fix applied:** Citations are literal [n] with a hand-written list. Scripted renumbering by first appearance over prose and caption lines only (table cells untouched); list reordered; verified sequential 1–31.

### B5. Figures 4(b) and 4(c) hard to read — split User Inputs into two columns
**Difficulty: ⭐⭐⭐** ✅ DONE · _`gen_pipeline_items.py` → `fig5_pipeline_examples.png`_
> *"Figures 4(b) and 4(c) are quite difficult to read and could possibly benefit from having the 'User Inputs' split into two columns (so that the other components and text could be larger)"*
Also Reviewer 2: *"figure 4 is not well readable"*.
**Proposed solution:** regenerate (b) and (c) with inputs in two columns, larger font, and
export at higher resolution / as vector (PDF or SVG) instead of PNG. Re-check at print size.
**Fix applied:** `gen_pipeline_items.py`: inputs in two columns (invisible pairing edges), orthogonal edges, node font 15, cluster labels 16, redundant panel title removed, ranksep 0.9; PDF output. Paper figure now a Typst grid of three vector panels (a)(b)(c). Simultaneity input added to the grid-side panels and formulas written in terms of S.

### B6. Citation [6] (ICCT 2022) not findable — add link
**Difficulty: ⭐** ✅ DONE
**Proposed solution:** URL exists in yml but is not printed; fix style/entry so the URL and
report title print. Verify the ICCT link still resolves.
**Fix applied:** Entry corrected: the ICCT document at that URL is the white paper "Charging solutions for battery-electric trucks" (Rajon Bernard, Tankou, Cui, Ragon, Dec 2022); URL printed. Verified from the PDF cover.

### B7. Citation [8] (McKinsey, Broer et al.) dated 2023, should be 2024 — add link
**Difficulty: ⭐** ✅ DONE
**Proposed solution:** verify publication date on mckinsey.com, correct `date`, make sure URL
prints.
**Fix applied:** Verified on McKinsey mirror: authors A. Herlt, E. Hildebrandt, H. Becker; published 19 Sep 2024. Entry and yml corrected, URL printed.

### B8. Citation [11] (Burton et al., NREL 2020) not findable
**Difficulty: ⭐** ✅ DONE
**Proposed solution:** verify `docs.nrel.gov/docs/fy20osti/75269.pdf` (may have moved with the
lab rename, see B9); correct title/authors/report number and print the URL.
**Fix applied:** Found to be a mis-citation inherited from the thesis: NREL 75269 is Elgqvist & Pohl, NREL/PR-6A20-75269 (Nov 2019), light-duty, REopt; no Burton, nothing on trucks. Davide chose: drop it and reattribute the sentence to Borlaug et al. 2021 (Nature Energy), claim verified against abstract and NREL summary (80% of 36 substations need no upgrade, smart charging spares another 10%).

### B9. "nrel" → "nlr" (lab renamed National Laboratory of the Rockies)
**Difficulty: ⭐** ✅ DONE · _[11], [22], any nrel.gov URL_
**Proposed solution:** update author/institution names and URLs to the new domain where the
documents have moved; keep old URL only if the new one does not resolve.
**Fix applied:** Lab renamed National Laboratory of the Rockies on 1 Dec 2025; nrel.gov no longer resolves, nlr.gov does. EVI-X entry now "National Laboratory of the Rockies (formerly NREL)" with nlr.gov URL. No other nrel links remain after B8.

### B10. Citation [17] (Synthesis of Expert Interviews) not findable — source of the cost functions
**Difficulty: ⭐⭐⭐** ✅ DONE · _MUST FIX before publication_
> *"I could not find citation [17], although this is quite important to demonstrate the source of the cost functions, which are the crux of the tool – so this needs to be updated before the paper is published."*
**Proposed solution (needs decision):** the interview synthesis is unpublished thesis material.
Options: (a) cite the public KTH thesis (DIVA, TRITA-ITM-EX 2025:525) where the synthesis and
all price tables are documented; (b) publish a `docs/cost_data_sources.md` in the repo listing
every price table with its source (interviews, Csanyi, ICCT, catalogues) and cite that via the
Zenodo DOI; (c) both. Recommend (c).
**Fix applied:** Replaced by the public KTH thesis record (D. Ferraro, TRITA-ITM-EX 2025:525, DIVA URL), which documents the interview synthesis and every price table. yml key `ferraro_thesis`.

---

## C. Software test report (4 bugs, `round5/EV Charging Cost Software_TestFeedbacks.docx`)

### C1. Sensitivity on Number of chargers crashes: `float + NoneType`
**Difficulty: ⭐⭐** ✅ DONE · `utils/cost.py:get_upper_price`, `calls.py:226`
**Root cause (probable):** `get_upper_price` returns `None` when the sized value exceeds the
largest catalogue key (transformer > 10 MVA, or charger/switchgear tables) and the sweep goes
far enough. Confirm by reproducing with default values.
**Proposed solution:** never return `None`: either extrapolate per-kVA from the top bracket or
raise a clear validation error that the UI shows ("configuration exceeds catalogue range"),
and cap the sweep range in the UI. Add regression test.
**Fix applied:** Reproduced: with default inputs the sweep reaches Type 3/4 at 90–95 chargers, uncovered load > 10,000 kVA, `get_upper_price` returned None. `transformer_cost_function` now splits loads above the largest catalogue size (10 MVA) across ceil(S/10000) identical units and sums their prices. Test `test_sweep_number_of_chargers_never_returns_none` + `test_transformer_above_catalogue_is_split_into_units`.

### C2. App freezes for 1 × 350 kW at 200 V (high current)
**Difficulty: ⭐⭐** ✅ DONE · `utils/cost.py:cables_rectifier_to_chargers_cost_function` (~L160)
**Root cause (CONFIRMED by reading the code):** in the `> MAX_CURRENT` branch
`rest_of_current = single_cable_nominal_current - MAX_CURRENT` resets instead of decrementing,
so any per-cable current above 860 A loops forever. Here current ≈ 1620 A.
**Proposed solution:** `rest_of_current -= MAX_CURRENT` (same fix already applied in
`lv_cabinet_cost_function`); audit the other three `while rest_of_current` loops. Test.
**Fix applied:** Replaced the three `rest_of_current=single_cable_nominal_current-MAX_CURRENT` resets (rectifier-to-chargers, LV distribution, MV distribution loops) with `rest_of_current -= MAX_CURRENT`. Test `test_high_current_cable_sizing_terminates` (1 × 350 kW at 200 V).

### C3. GUI says MV not required but costs include MV equipment (3 × 100 kW, grid 200, trafo 100 kVA)
**Difficulty: ⭐⭐⭐** ✅ DONE · `calls.py:case_definition` vs `hard_requirement`
**Root cause (CONFIRMED):** `hard_requirement` tests `close_trafo_power >= uncovered_load`
(100 ≥ 100 → no MV) while `case_definition` tests `grid_capacity >= treshold` (100 ≥ 200 →
false → Type 3). The two use different conditions for Type 2.
**Proposed solution:** decide which rule is the intended Type 2 definition (paper §2.2 and
Figure 2 flowchart say: uncovered load ≤ LV threshold AND nearby transformer has enough spare
capacity for it). Align `case_definition` to `grid_capacity >= spare_load`, and have the GUI
call the same function so they cannot diverge again. Check the paper flowchart text matches.
**Fix applied:** `case_definition` Type 2 condition changed from `grid_capacity>=treshold` to `grid_capacity>=spare_load`, matching `hard_requirement`. Tests: tester's exact case now Type 2 with zero MV costs; exhaustive agreement test GUI vs engine over 1–39 chargers × grid × nearby capacity × transformer presence. **Paper follow-up:** §2.2 L107 describes Type 2 by LV threshold only; add the nearby-transformer spare-capacity condition so the prose matches the code (fold into A1/B1 edits).

### C4. Transformer safety margin has no effect
**Difficulty: ⭐** ✅ DONE · `utils/cost.py:348-352`
**Root cause (CONFIRMED):** operator precedence: `(...)*1+(safety_margin/100)` adds 0.2 kVA
instead of multiplying by 1.2. Should be `(...)*(1+safety_margin/100)`.
**Proposed solution:** fix, add test (20% vs 50% must change bracket for 4 × 100 kW case:
100 kVA uncovered → 120 vs 150 kVA → €6,805 vs €6,805? check: both ≤150 → same bracket!
Use a test case that crosses a bracket). Note: case-study numbers in paper §3 may shift if
those cases are Type 3/4; must recompute Table 3 / Figures 5–6 after the fix.
**Fix applied:** `*1+(safety_margin/100)` → `*(1+safety_margin/100)` in both Type 3 and Type 4 branches. Test: 4 × 100 kW, 200 kVA uncovered: 0% → €8,679, 20% → €9,497, 50% → €10,315. Same bug exists in legacy `TOOL/utils/cost.py` (not fixed, legacy).

---

## D. Cross-cutting / housekeeping
- D1 ✅ DECIDED (keep figures, state the fix and its <1% effect in the response letter) **Impact of C3/C4 on published numbers:** Figures 5–6 (fig6_cost_per_plug, fig7_case_studies) are thesis PDFs computed with the old code. C4 raises transformer size by the margin (20% default) for every Type 3/4 case, typically one catalogue bracket (+€800 to €3,000 per site, well under 1% of totals). C3 only matters when the nearby transformer's spare capacity lies between the uncovered load and the LV threshold. Full case inputs (distances, LV level, margin) are only in thesis radar plots, not in text. Needs decision: recompute with Davide's thesis input files, or keep figures and state the bracket shift in the response letter.
- D1-old ☐ Recompute all nine case studies after C3/C4 (and A1 if default = 1.0 results must be
  unchanged except for bug fixes). Regenerate Figures 5 and 6 and Table 3 if numbers move.
- D2 ✅ partly: version v1.1.0 in metadata table, README and new `CITATION.cff`; `docs/USER_GUIDE.md` written and linked from the metadata table and README. **Zenodo DOI still needs Davide** (log in at zenodo.org with GitHub, enable the repo, create release v1.1.0 on GitHub; then put the DOI in the metadata table / README).
- D3 ✅ draft: `review/round5/response_letter.md` in Carolina's format (comment, reply, quoted revised text). Reviewer numbering assumed: unnumbered review = Reviewer 1, simultaneity review = Reviewer 2; confirm against the decision letter. Annotated PDF not produced (journal wants the letter); can be generated with `review/annotate.py` if Jagruti wants it.
- D4 ✅ (C1–C4, D6) `tests/test_costs.py`, 8 tests pass; committed locally (not pushed) (`venv/bin/python -m pytest tests -q`). A1 tests to add.
- D6 ✅ (Davide OK 2026-10-20, fixed + test) Observed, not reported by anyone: in `cost_breakdown_sensitivity_calculation` the "Total" omits planning, MV connection and LV connection costs, whereas the Cost Breakdown total includes them. Fix only with Davide's OK (changes sensitivity totals).
- D7 ✅ DONE (redrawn with Graphviz, `figures/classification_flowchart.dot`; old PDF kept in review/round5/) **Flowchart (Figure 2, `fig3_classification_flowchart.pdf`) still shows the old Type 2 test "Grid Capacity >= Threshold"; after C3 it must read "Grid Capacity >= Spare" and the load box must include f. No source file (thesis PDF): redraw (Graphviz, same look as the pipeline figures).**
- D8 ✅ DONE (gen_fig1.py → 17 parameters, regenerated) **Figure 1 (`gen_fig1.py`) says "User Inputs (16 parameters)" → 17 after A1. Regenerate.**
- D5 ✅ 3580 body words (Sections 1–5, figures/tables excluded), 6 figures, 16 pages compiled.

## Decisions made up front (resolved with Davide 2026-10-20)
| # | Question | Decision |
|---|----------|----------|
| Q1 | Simultaneity factor | **Implement in the tool** as a new input (default 1.0) + paper updates (§1, §2.2, sensitivity list). |
| Q2 | Source of test report / revision status | **Jagruti's own test** (not journal-assigned). Journal decision: **minor revision**. Bugs C1–C4 get fixed and mentioned briefly in the response as improvements, not as reviewer items. |
| Q3 | Citation [17] replacement | **Cite the KTH thesis only** (DIVA record, TRITA-ITM-EX 2025:525). |
| Q4 | Type 2 rule | **Nearby transformer spare capacity >= uncovered load** (align `case_definition` to `hard_requirement`). |
| Q5 | Release housekeeping | **Yes to all three**: bump to v1.1.0, Zenodo DOI after fixes, docs page to replace the "To be added" link. |
| Q6 | Jagruti's action points | Not yet received; work from reviews + test report, fold hers in when they arrive. |
| Q7 | Deadline | **About two weeks.** Priority order: C bugs → A1 simultaneity → citations (B4, B6–B10) → figure (B5) → text (B1–B3, A2) → docs/Zenodo (D2) → response letter (D3). |
