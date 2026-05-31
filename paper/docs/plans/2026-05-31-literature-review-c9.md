# Comment #9: Expand Related-Software Literature Review — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the thin related-work paragraph (Section 1) with a structured, cited survey of EV charging infrastructure cost-estimation tools that establishes the gap, addressing reviewer comment #9. Add the six new references to all bibliography locations, clean up stray markers, mark #9 done, and recompile.

**Architecture:** The new review is two prose paragraphs organized by the three tool categories the research found (LCOC/operating-economics tools, NREL EVI-X planning/simulation tools, static component-level cost literature), followed by the HDV-specific closest work and an explicit gap statement. No em dashes, no bullet lists. Findings are from a verified deep-research run (24/25 claims confirmed by 3-vote adversarial verification).

**Tech Stack:** Markdown (`paper.md`), Typst (`paper_final.typ`), Hayagriva YAML (`references.yml`), Graphviz/none.

---

## New references (assigned numbers [22]–[27])

| # | Citation |
|---|---|
| [22] | National Renewable Energy Laboratory, EVI-X Modeling Suite (EVI-Pro, EVI-FAST), NREL, (n.d.). https://www.nrel.gov/transportation/evi-x |
| [23] | L. Lanz, B. Noll, T.S. Schmidt, B. Steffen, Comparing the levelized cost of electric vehicle charging options in Europe, Nature Communications 13 (2022) 5277. https://doi.org/10.1038/s41467-022-32835-7 |
| [24] | Atlas Public Policy, EV Charging Cost Calculator, (n.d.). https://atlaspolicy.com/ev-charging-cost-calculator/ |
| [25] | M. Nicholas, Estimating electric vehicle charging infrastructure costs across major U.S. metropolitan areas, ICCT Working Paper 2019-14, International Council on Clean Transportation (2019). https://theicct.org/publication/estimating-electric-vehicle-charging-infrastructure-costs-across-major-u-s-metropolitan-areas/ |
| [26] | B. Borlaug, M. Muratori, M. Gilleran, D. Woody, W. Muston, T. Canada, et al., Heavy-duty truck electrification and the impacts of depot charging on electricity distribution systems, Nature Energy 6 (2021) 673–682. https://doi.org/10.1038/s41560-021-00855-0 |
| [27] | G. Wang, M. Miller, L. Fulton, The infrastructure cost for depot charging of battery electric trucks, The Electricity Journal (2025). https://www.sciencedirect.com/science/article/abs/pii/S1040619025000351 |

Already cited, reused in the new text: [6] ICCT 2022 truck report, [10] Borlaug 2020 LCOC (Joule), [12] AFDC 2015 EVSE report, [14] FleetRL.

---

## The new related-work text (canonical version, used in both paper.md and paper_final.typ)

Paragraph A:

> Several software tools and models address parts of the EV charging cost problem, but they fall into three groups that each leave the target case uncovered. The first group computes the levelized cost of charging (LCOC), a per-kilowatt-hour operating metric rather than an upfront capital cost. Borlaug et al. [10] built the reference LCOC framework for the United States and released it as the open-source lcoc-ldevs tool, but it targets light-duty vehicles and folds equipment and installation into an amortized input rather than producing a component breakdown. Lanz et al. [23] applied a similar LCOC approach across 30 European countries, yet their model covers passenger transport only and deliberately leaves grid connection costs out. The Atlas Public Policy charging cost calculator [24] works the same way, estimating the electricity cost of a given charging pattern rather than the hardware and connection investment. The second group is the set of planning and simulation tools in the U.S. Department of Energy EVI-X suite [22]. These project charging demand, simulate site energy use, or run financial scenarios, and they are explicit that capital cost estimation is not their job: the financial tool EVI-FAST asks the user to supply equipment and installation costs from vendor quotes rather than deriving them. The third group is the static, component-level cost literature. The AFDC report on non-residential charging equipment [12] and the ICCT metropolitan-area analysis [25] both split installation cost into hardware, labor, permitting, and grid connection, but they are published as fixed tables and figures rather than interactive software, and both describe U.S. passenger charging with data that is now roughly a decade old.

Paragraph B:

> Work specific to heavy-duty depot charging is more recent and still leaves the niche open. Borlaug et al. [26] examined how depot charging stresses the electricity distribution system and released a load-profile generator, but their focus is grid upgrade cost and load shapes rather than a station-level investment breakdown. Wang et al. [27] come closest in intent, building a component-level bottom-up cost model for medium- and heavy-duty depot charging in California, yet they publish it as a methodology and dataset rather than a reusable interactive tool, and the costs are specific to the United States. FleetRL [14], the SoftwareX tool most often mentioned alongside this kind of work, is a reinforcement-learning environment for scheduling fleet charging and minimizing electricity cost; it models charging operation, not the physical infrastructure or its capital cost, so it complements rather than overlaps with the present tool. Across all of these, no open-source, interactive tool estimates component-level investment cost from the medium-voltage grid connection to the charging plug for European heavy-duty overnight charging, which is the gap this software fills.

---

## Task 1: Rewrite the related-work paragraph in paper.md

**Files:** Modify `paper/paper.md` (lines ~48–52)

- [ ] **Step 1: Replace the highlighted paragraph and remove the [REVIEW] note.**

Find this block (the `==…==` wrapped paragraph plus the blank line and the `> **[REVIEW]**` blockquote that follows it):
```
==No open-source tool currently lets a user enter site-specific parameters and get a component-level investment cost breakdown for an HDV charging station. FleetRL [14], published in SoftwareX, is a reinforcement learning environment for fleet charging optimization. It decides when and how much to charge but does not model the physical infrastructure or its cost. ICCT reports [6] give aggregate estimates in static PDFs, not interactive calculators. Borlaug et al. [10] defined the levelized cost of charging (LCOC) framework for the U.S. but did not publish a reusable tool. Nothing covers the full cost chain from the MV grid connection point to the DC charging plug for European HDV overnight charging.==

> **[REVIEW]** I think this literature review of softwares is short, and FleetRL is not even so related. What Types of softwares exist and which gap this software fills? For sure reviewers will ask for a more indeep review.
```

Replace with Paragraph A followed by a blank line and Paragraph B (the canonical text above, no `==` wrappers, no blockquote).

- [ ] **Step 2: Verify** no `[REVIEW]` marker remains in Section 1 and the two new paragraphs read cleanly with citations [10],[12],[22],[23],[24],[25] in A and [14],[26],[27] in B.

---

## Task 2: Remove the stray highlight in the abstract (paper.md)

**Files:** Modify `paper/paper.md` (line ~18)

- [ ] **Step 1:** Replace `==overnight==` with `overnight` (remove the two `==` markers, keep the word). After this, `grep -c "==" paper.md` must return 0.

---

## Task 3: Add references [22]–[27] to the paper.md bibliography

**Files:** Modify `paper/paper.md` (end of Bibliography section, after `[21]`)

- [ ] **Step 1:** After the `[21] HoLa Innovation Cluster …` entry, append the six entries from the "New references" table above, each as a blank-line-separated Markdown paragraph in the same style as the existing entries (number in brackets, authors, title, venue, year, link).

---

## Task 4: Mirror the rewrite in paper_final.typ

**Files:** Modify `paper/paper_final.typ`

- [ ] **Step 1:** Find the related-work paragraph in the Motivation section that begins `No open-source tool currently lets a user enter site-specific parameters` and ends `… for European HDV overnight charging.` Replace it with Paragraph A and Paragraph B (canonical text), as two separate Typst paragraphs (blank line between).

- [ ] **Step 2:** In the `*References*` list at the end of the file, after the `[21]` entry, add the six new entries [22]–[27] in the same plain-text style used there (Typst auto-renders the URLs).

---

## Task 5: Add entries to references.yml

**Files:** Modify `paper/references.yml`

- [ ] **Step 1:** Append six Hayagriva entries (keys: `nrel_evix`, `lanz_eu_lcoc`, `atlas_calculator`, `nicholas_icct_2019`, `borlaug_hdv_2021`, `wang_depot_2025`) with `type`, `title`, `author`, `url`, `date`, and where applicable `parent` (journal), `volume`, `page-range`, `serial-number` (DOI). Match the existing file's structure.

---

## Task 6: Mark comment #9 done in review.md

**Files:** Modify `paper/review.md`

- [ ] **Step 1:** On the `## 9. …` difficulty line, append `✅ DONE`.

- [ ] **Step 2:** At the end of comment #9 (after its existing description), add:
```
**Fix applied:** Replaced the single-paragraph related-work note with a structured two-paragraph survey organized by the three categories of existing tools — LCOC/operating-economics tools (Borlaug 2020 [10], Lanz 2022 [23], Atlas [24]), the NREL EVI-X planning/simulation suite [22], and static component-level cost studies (AFDC [12], ICCT/Nicholas [25]) — then the closest HDV-depot work (Borlaug 2021 [26], Wang 2025 [27]) and FleetRL [14], ending with an explicit statement of the gap. Six new references [22]–[27] added. Based on a verified deep-research survey (24/25 claims confirmed by 3-vote adversarial verification).
```

---

## Task 7: Recompile and verify

- [ ] **Step 1:** Run `cd paper && typst compile paper_final.typ paper_final.pdf`. Expect exit 0, no unresolved-reference warnings.
- [ ] **Step 2:** Run `grep -c "—" paper/paper.md paper/paper_final.typ` (em dashes) and `grep -c "==" paper/paper.md` (highlights). All must be 0.
- [ ] **Step 3:** Run `grep -c "\[REVIEW\]" paper/paper.md`. Must be 0 (all reviewer comments now resolved).

---

## Self-Review Checklist

- [x] **Reviewer's three asks covered:** (1) what types of software exist — three categories named; (2) what each covers and misses — stated per tool; (3) explicit gap — final sentence of Paragraph B.
- [x] **Verification caveats respected:** NREL framed as "capital cost estimation is not their job" (not "ignores cost"); ICCT framed as static analysis, not "no interactive tool"; EU LCOC framed as passenger-scoped, not "explicitly excludes HDVs"; refuted AFDC claim not used.
- [x] **No em dashes, no bullet lists** in the new prose.
- [x] **No placeholders:** full paragraph text and all six citations written out.
- [x] **Reference numbers consistent:** [22]–[27] used identically in text, paper.md bib, and paper_final.typ list; reused [6],[10],[12],[14] already exist.
- [x] **Three bibliography locations kept in sync** (paper.md, paper_final.typ, references.yml).
