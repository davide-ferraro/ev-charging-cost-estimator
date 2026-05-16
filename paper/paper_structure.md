# Paper Structure: Techno-Economic Cost Estimation Tool for Overnight Charging Infrastructure of Heavy-Duty Vehicles in Europe

> **Target format:** SoftwareX "Original software publication" (same as FleetRL paper by Cording & Thakur, 2024)
>
> **Authors:** Davide Ferraro, Jagruti Thakur
>
> **Affiliation:** KTH Royal Institute of Technology, Stockholm, 11428, Sweden

---

## Article Info

**Keywords:**
- Heavy-duty vehicles
- Depot charging
- Techno-economic analysis
- Investment cost modeling
- Charging infrastructure
- Grid connection
- Decision-support tool

---

## Code Metadata Table

| Field | Value |
|-------|-------|
| Current code version | v1.0.0 |
| Permanent link to code/repository | *(GitHub/Zenodo link)* |
| Legal Code License | *(choose: MIT, GPL, etc.)* |
| Code versioning system used | git |
| Software code languages, tools, and services used | Python, Streamlit, Plotly, Pandas, NumPy, OpenPyXL |
| Compilation requirements, operating environments & dependencies | Python >= 3.10, see requirements.txt |
| If available, link to developer documentation/manual | *(link)* |
| Support email for questions | *(email)* |

---

## Abstract (~150-200 words)

The deployment of overnight charging infrastructure for battery-electric heavy-duty vehicles (HDVs) is critical for decarbonizing European freight transport, yet decision-makers lack transparent, component-level cost estimation tools. This paper introduces an open-source, web-based investment cost calculator for overnight depot and public parking charging stations. The tool takes site-specific electrical parameters as input -- number and power of chargers, grid connection type, voltage levels, cable distances, and site conditions -- and automatically determines the project type (one of four categories based on grid connection requirements). It then sizes every electrical component from the grid connection point to the charging plug and computes itemized costs using real-world pricing data. The tool supports three analysis modes: cost breakdown, single-variable sensitivity, and two-parameter sensitivity analysis, enabling users to explore how different design choices affect total investment cost. Applied to nine case studies across Germany, Italy, and the United Kingdom, the tool produces investment costs ranging from EUR 20,000 to EUR 80,000 per charging plug, depending on grid connection type, charger power level, and deployment scale.

---

## 1. Motivation and Significance (~1.5-2 pages)

### 1.1 Context and Problem

- The EU's Fit for 55 package mandates steep CO2 reductions for HDVs (45% by 2030, 90% by 2040), driving rapid adoption of battery-electric trucks.
- The Alternative Fuels Infrastructure Regulation (AFIR) requires high-power charging hubs every 60 km along the TEN-T core network by 2030, implying an estimated EUR 7 billion investment and over 300,000 charging points.
- Infrastructure -- not vehicle technology -- is the primary bottleneck. Overnight depot charging is the dominant use case for commercial fleets (predictable schedules, low-cost off-peak electricity).

### 1.2 The Gap: Lack of Transparent Cost Estimation Tools

- Existing studies estimate infrastructure costs at aggregate level (total CAPEX ranges) without modeling individual electrical components, cable sizing, or grid connection complexity.
- Most cost analyses focus on North American contexts with different electricity pricing structures, grid regulations, and equipment standards.
- No publicly available, open-source tool allows fleet operators, infrastructure planners, or policymakers to input site-specific parameters and obtain detailed, component-level cost breakdowns.
- Lead time estimation -- a critical planning factor -- is almost entirely absent from the academic literature.

### 1.3 Contribution

- This paper presents the first open-source, web-based tool for techno-economic evaluation of overnight HDV charging infrastructure in Europe.
- The tool bridges the gap between high-level cost reports and detailed engineering design by:
  - Modeling 19 individual cost components from the grid connection to the charging plug
  - Automatically classifying projects into four types based on grid connection requirements
  - Incorporating real-world equipment pricing data (transformers, switchgear, cables, chargers, rectifiers)
- The tool is designed for two user groups: (1) fleet operators and infrastructure planners making investment decisions, and (2) researchers studying the economics of HDV charging deployment.

### 1.4 Related Software

- **FleetRL** (Cording & Thakur, 2024): RL environment for optimizing EV fleet charging operations. Focuses on operational charging strategies (when/how much to charge), not infrastructure investment costs. Complementary to this work -- FleetRL addresses operational costs, while this tool addresses capital investment costs.
- No existing open-source tool addresses the full infrastructure investment cost chain from grid connection to plug for HDV overnight charging.

---

## 2. Software Description (~2-3 pages)

### 2.1 Software Architecture

Overview of the tool's modular structure:

```
TOOL_streamlit/
  app.py            -- Streamlit web interface (706 lines)
  utils/
    calls.py        -- Cost calculation orchestration (9 functions)
    cost.py         -- 19 individual cost functions with pricing data
```

- **app.py**: Streamlit-based web GUI with three analysis modes. Handles user input, validation, visualization (Plotly charts), and Excel export.
- **utils/calls.py**: Orchestration layer containing:
  - `medium_requirement()` and `hard_requirement()`: Grid connection requirement validators
  - `case_definition()`: Automatic project type classification (Types 1-4)
  - `compute_all_costs()`: Aggregates all 19 component cost functions
  - Sensitivity analysis functions for single and double parameter sweeps
- **utils/cost.py**: 19 standalone cost functions, each mapping a physical quantity (apparent power, current, cable length, etc.) to a cost in 2024 EUR, using real equipment pricing data from industrial catalogs, e-commerce platforms, and published studies.

**Data flow:** User inputs --> Requirement validation --> Project type determination --> Component sizing (electrical engineering equations) --> Cost functions (pricing data) --> Aggregation --> Visualization & export.

*(Include a figure similar to FleetRL's Fig. 1: graphical overview showing the flow from inputs through calculation to outputs)*

### 2.2 Software Functionalities

#### 2.2.1 Input Parameters

The tool accepts 13 numerical inputs plus 3 categorical selections:
- **Electrical parameters:** Number of chargers, charger power (10-350 kW), low voltage level, grid connection capacity, load power factor
- **Site layout:** Distance between rectifier and chargers, distance to MV/LV transformer, distance to MV access point
- **Grid configuration:** Transformer presence (yes/no), maximum LV connection power, available transformer capacity, medium voltage level, transformer safety margin
- **Site preparation:** Land area, material type (asphalt/concrete), terrain type

#### 2.2.2 Automatic Project Type Classification

Based on the relationship between planned charging load and existing grid capacity, the tool classifies each project into one of four types:
- **Type 1:** Existing grid connection is sufficient (no upgrades needed)
- **Type 2:** Low-voltage connection upgrade required (additional LV connection or upgrade)
- **Type 3:** Existing MV connection present but insufficient; new MV connection required
- **Type 4:** No existing MV connection; new MV connection required from scratch

This classification determines which cost components are included and which lead time estimates apply.

#### 2.2.3 Investment Cost Model

The model calculates 19 cost items organized into three categories:

**Medium Voltage Equipment:** Transformer, MV switchgear, surge arresters, grounding resistors, MVAC cables

**Low Voltage Equipment:** LVAC cables, LV switchboard, rectifier, LVDC cables, chargers/dispensers

**Labor & Site Costs:** Planning, installation, MV connection, LV connection, site preparation

Each component cost is computed as a function of one or more sized physical quantities (e.g., transformer cost = f(apparent power), cable cost = f(current, length, number of parallel systems)). Cost functions are calibrated using real market data.

#### 2.2.4 Analysis Modes

1. **Cost Breakdown:** Full itemized cost table for the configured scenario, with interactive Plotly chart and Excel export
2. **Single-Variable Sensitivity:** Vary one parameter across its range, producing stacked bar charts showing how each cost component evolves
3. **Two-Parameter Sensitivity:** Vary two parameters simultaneously, visualized as a scatter plot with color-coded second parameter

#### 2.2.5 Accessibility and Usability

- Web-based interface (Streamlit) -- no installation required for end users
- Dark-themed, responsive UI with input validation and dynamic field enabling/disabling
- Excel export for all analysis modes
- Input tooltips and contextual help

---

## 3. Illustrative Examples (~2-3 pages)

### 3.1 Case Study Setup

Present a selection of the nine case studies (e.g., 3-4 representative ones) from Germany, Italy, and the UK, covering different project types. For each, briefly state:
- Location context (public parking vs. depot)
- Key input parameters (number of chargers, power level, grid connection capacity, transformer presence)
- Resulting project type classification

*(Include a summary table similar to FleetRL's Table 1)*

### 3.2 Investment Cost Results

- **Cost per plug analysis:** Show how investment cost per plug ranges from EUR 20,000 (Type 1, large deployments) to EUR 80,000 (Type 4, small deployments), demonstrating the tool's ability to capture the wide cost variability.
- **Cost breakdown comparison:** Show the itemized cost breakdown for selected cases, highlighting that chargers, rectifiers, and installation labor typically dominate, while MV equipment adds significant cost for Type 3/4 projects.
- **Sensitivity example:** Demonstrate a sensitivity analysis varying charger power from 20 to 300 kW, showing how specific cost (EUR/kW) decreases with scale for Type 1 but plateaus for Type 4 projects.

*(Include 2-3 figures: cost breakdown bar chart, sensitivity chart, cost per plug range)*

### 3.3 Lead Time Estimates

- Present the lead time ranges for each project type, derived from expert interviews
- Type 1: 5-15 months; Type 2: 6-22 months; Type 3/4: 12-48+ months
- Highlight DNO responsiveness and grid capacity as the dominant sources of variability
- Discuss the practical implications: large-scale deployments requiring new MV connections must be planned years in advance

*(Include 1 figure: lead time Gantt chart or bar chart by project type)*

---

## 4. Impact (~0.5-1 page)

- **For fleet operators and hauliers:** Enables transparent, site-specific investment cost estimation before committing to infrastructure projects. Supports comparison of different deployment strategies (e.g., fewer high-power chargers vs. many low-power chargers, LV-only vs. MV connection). The sensitivity analysis modes help identify which parameters drive costs most.
- **For infrastructure planners and policymakers:** Provides quantitative evidence for planning decisions, subsidy design, and regulatory impact assessment. The lead time estimates (5-15 months for Type 1, up to 4+ years for Type 3/4) highlight the urgency of early grid planning.
- **For researchers:** Offers a reproducible, modifiable investment cost modeling framework. Component-level granularity allows validation against real project data and extension to new equipment types (e.g., MCS connectors) or regional markets.
- **Practical relevance:** The tool was developed in collaboration with Scania AB and validated through expert interviews with nine industry professionals across Europe.
- **Broader context:** As AFIR mandates the deployment of 300,000+ truck charging points by 2030, standardized investment cost estimation tools are essential for coordinating the EUR 7 billion investment effort across member states.

---

## 5. Conclusions (~0.5 page)

- Summarize the tool's capabilities: open-source, web-based, component-level investment cost modeling from grid connection to plug for HDV overnight charging
- Key findings enabled by the tool:
  - Investment cost per plug: EUR 20,000-80,000 depending on grid connection type and scale
  - Economies of scale are significant but bounded by grid connection costs (MV equipment adds a fixed cost layer for Type 3/4 projects)
  - Chargers, rectifiers, and installation labor dominate costs for Type 1 projects; MV equipment becomes the main differentiator for Type 3/4
  - Lead times vary from 5 months to 4+ years, primarily driven by DNO processes
- Future work: integration of operational cost modeling (electricity optimization, LCOC), extension to MCS connector pricing, and regional deployment modeling
- The tool fills a gap in the available software landscape by providing the first open-source, customizable infrastructure investment cost calculator for the emerging HDV charging market in Europe

---

## CRediT Authorship Contribution Statement

**Davide Ferraro:** Writing -- original draft, Software, Methodology, Investigation, Formal analysis, Data curation, Visualization, Validation. **Jagruti Thakur:** Writing -- review & editing, Supervision, Methodology, Conceptualization, Resources, Project administration.

---

## Declaration of Competing Interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

---

## Acknowledgments

The authors thank Antonius Kies (Scania AB) for industrial supervision and guidance, and the nine industry professionals who participated in expert interviews to validate assumptions and provide lead time data.

---

## Data Availability

The source code and sample data are available at *(repository link)*. Data will be made available on request.

---

## References

*(Key references to include -- approx. 20-30, following SoftwareX style)*

1. EU Fit for 55 HDV CO2 standards regulation
2. AFIR regulation
3. ACEA/ChargeUp/T&E European EV Charging Infrastructure Masterplan
4. McKinsey charging infrastructure investment estimates
5. Borlaug et al. (2020) -- Levelized Cost of Charging EVs in the US (Joule)
6. Lanz et al. -- LCOC for the European context
7. Cording & Thakur (2024) -- FleetRL (SoftwareX)
8. ICCT reports on charging infrastructure costs
9. Prysmian Group cable catalog
10. Transport & Environment reports
11. HoLa project (MCS)
12. Streamlit framework
13. Burton et al. -- grid-related cost optimization
14. IEEE Std 142-2007 (grounding)
15. IEC 62196 / CCS2 standard
16. CharIN MCS standard
17. Farady Electric -- MV switchgear pricing
18. ABB -- switchgear guides
19. Siemens -- DC dispenser pricing
20. Wire & Cable Your Way -- cable pricing data
21. *(additional references from thesis bibliography as needed)*

---

## Notes on Adapting to SoftwareX Format

- **Length:** SoftwareX papers are typically 6-8 pages. The sections above are calibrated for this.
- **Focus on software:** Unlike a thesis, the paper should lead with the software and its capabilities, not the background theory. Background goes into Section 1 (Motivation) but should be concise.
- **Figures:** Aim for 4-6 figures total: (1) software architecture diagram, (2) screenshot of the web interface, (3) cost breakdown example, (4) sensitivity analysis example, (5) cost per plug range chart, (6) lead time summary.
- **Equations:** Include only the most important ones (e.g., transformer sizing, cable current calculation, switchgear cost model). Move detailed component equations to supplementary material or reference the thesis.
- **Code metadata table:** Required by SoftwareX -- fill in before submission.
- **Repository:** The code must be in a public repository (GitHub) with a permanent archive (Zenodo DOI) before submission.
