// ============================================================================
// Paper: Investment Cost Estimation Tool for Overnight Charging
//        Infrastructure of Heavy-Duty Vehicles in Europe
// Format: SoftwareX (Elsevier) — Original software publication
// ============================================================================

// --- Page setup ---
#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
)
#set text(font: "New Computer Modern", size: 10pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.1")

// --- Title ---
#align(center)[
  #text(size: 14pt, weight: "bold")[
    Investment Cost Estimation Tool for Overnight Charging Infrastructure of Heavy-Duty Vehicles in Europe
  ]

  #v(1em)

  #text(size: 11pt)[Davide Ferraro, Jagruti Thakur#super[\*]]

  #v(0.5em)

  #text(size: 9pt, style: "italic")[
    KTH Royal Institute of Technology, Stockholm, 11428, Sweden
  ]

  #v(0.3em)

  #text(size: 8.5pt)[
    #super[\*] Corresponding author. _E-mail address:_ jrthakur\@kth.se (Jagruti Thakur).
  ]
]

#v(1em)

// --- Article Info & Abstract side by side ---
#grid(
  columns: (1fr, 2.5fr),
  column-gutter: 1.5em,
  [
    #text(size: 8.5pt, weight: "bold")[A R T I C L E #h(0.5em) I N F O]

    #v(0.6em)

    #text(size: 8.5pt)[
      _Keywords:_ \
      Heavy-duty vehicles \
      Depot charging \
      Investment cost modeling \
      Charging infrastructure \
      Grid connection \
      Techno-economic analysis \
      Decision-support tool
    ]
  ],
  [
    #text(size: 8.5pt, weight: "bold")[A B S T R A C T]

    #v(0.6em)

    #text(size: 9pt)[
      The deployment of overnight charging infrastructure for battery-electric heavy-duty vehicles (HDVs) is critical for decarbonizing European freight transport, yet decision-makers lack transparent, component-level cost estimation tools. This paper introduces an open-source, web-based investment cost calculator for overnight depot and public parking charging stations. The tool takes site-specific electrical parameters as input (number and power of chargers, grid connection type, voltage levels, cable distances, and site conditions) and automatically determines the project type (one of four categories based on grid connection requirements). It then sizes every electrical component from the grid connection point to the charging plug and computes itemized costs using real-world pricing data. The tool supports three analysis modes: cost breakdown, single-variable sensitivity, and two-parameter sensitivity analysis, enabling users to explore how different design choices affect total investment cost. Applied to nine case studies across Germany, Italy, and the United Kingdom, the tool produces investment costs ranging from €20,000 to €80,000 per charging plug, depending on grid connection type, charger power level, and deployment scale.
    ]
  ],
)

#v(1em)

// --- Code Metadata Table ---
#text(size: 9pt, weight: "bold")[Code metadata]
#v(0.4em)

#set text(size: 8.5pt)

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  [Current code version], [v1.0.0],
  [Permanent link to code/repository used for this code version], [https://github.com/davide-ferraro/ev-charging-cost-estimator],
  [Legal Code License], [MIT],
  [Code versioning system used], [git],
  [Software code languages, tools, and services used], [Python, Streamlit, Plotly, Pandas, NumPy, OpenPyXL],
  [Compilation requirements, operating environments & dependencies], [Python ≥ 3.10],
  [If available, link to developer documentation/manual], [https://kth.diva-portal.org/smash/record.jsf?pid=diva2%3A2007635],
  [Support email for questions], [davideferraro275\@gmail.com],
)

#set text(size: 10pt)

#v(1.5em)

// ============================================================================
// SECTION 1 — MOTIVATION AND SIGNIFICANCE
// ============================================================================

= Motivation and Significance

Battery-electric trucks are entering the European market at a pace that the charging infrastructure has not kept up with. Heavy-duty vehicles (HDVs) account for over a quarter of EU road transport greenhouse gas emissions and roughly 6% of total EU emissions, despite being a small share of the fleet @eu_hdv. The EU's "Fit for 55" package now mandates CO#sub[2] reductions of 45% by 2030, 65% by 2035, and 90% by 2040 for new HDVs @eu_hdv. Since electric trucks produce no tailpipe CO#sub[2], they count as zero-emission under these rules, which is a direct incentive for manufacturers and fleet operators to go electric @climate_change_connection. Battery costs have fallen enough that electric trucks now work across most freight segments @iea_gev_2023 @acea_masterplan, and McKinsey expects most e-truck operators to prefer overnight depot charging for its predictable schedules and cheap off-peak electricity @mckinsey_overnight.

The problem is on the infrastructure side. A single long-haul truck battery can hold 300--800 kWh, and a depot charging multiple trucks at once may need several megawatts of grid capacity @acea_masterplan @icct_costs @iea_gev_2023. The Alternative Fuels Infrastructure Regulation (AFIR) requires EU Member States to install at least 3.6 MW of truck charging capacity every 60 km along the core road network by 2030 @afir. Europe had roughly 10,000 public truck charging points in 2023; that number needs to reach 300,000 by the end of the decade, at an estimated cost of €7 billion @mckinsey_charging. Most existing depots cannot supply this kind of power, and getting a grid connection upgraded is slow, expensive, and tangled in permitting, sometimes taking years @uk_grid_connection.

Cost estimation makes this harder. Charging infrastructure for passenger cars is well studied, but trucks need bigger chargers, heavier electrical equipment, and site-specific civil works. Fleet managers and investors rarely have clear numbers for how costs change across different configurations @borlaug_lcoc. For instance, how much more a depot serving fifty trucks costs compared to one serving five, or what the price difference is between a site that already has a medium-voltage (MV) connection and one that needs a new one built from scratch. Borlaug et al. @borlaug_lcoc found that smaller U.S. depots can often avoid costly grid upgrades, but larger sites typically need high-power connections and new substations. The ICCT notes that transformer sizing, permitting rules, and site characteristics create wide cost variation even within a single country @icct_costs. Burton et al. @burton_ev showed that utilities can cut grid-related costs by sizing components around actual truck usage patterns rather than peak demand. Still, the literature mostly reports cost in broad categories ("equipment," "labor," "grid fees") without breaking it down to individual components like cable cross-sections or switchgear ratings @acea_masterplan @mckinsey_charging. Most studies also focus on North America @borlaug_lcoc @usdoe_evse_costs, where electricity pricing, grid regulations, and equipment standards differ from Europe. Lead time and permitting data is scarce as well @te_depot @uk_grid_connection.

No open-source tool currently lets a user enter site-specific parameters and get a component-level investment cost breakdown for an HDV charging station. FleetRL @cording_fleetrl, published in SoftwareX, is a reinforcement learning environment for fleet charging optimization. It decides when and how much to charge but does not model the physical infrastructure or its cost. ICCT reports @icct_costs give aggregate estimates in static PDFs, not interactive calculators. Borlaug et al. @borlaug_lcoc defined the levelized cost of charging (LCOC) framework for the U.S. but did not publish a reusable tool. Nothing covers the full cost chain from the MV grid connection point to the DC charging plug for European HDV overnight charging.

This paper fills that gap with the first open-source, web-based tool for estimating overnight charging infrastructure investment costs for battery-electric HDVs in Europe. The tool: (1) models 19 individual cost components from the grid connection to the plug; (2) automatically classifies projects into four types based on grid connection requirements; (3) uses real equipment pricing data in 2024 euros from catalogs, suppliers, and published studies; (4) supports cost breakdown, single-variable, and two-parameter sensitivity analyses; and (5) runs as a Streamlit web application that requires no installation and produces interactive charts and downloadable reports. It was developed at KTH Royal Institute of Technology with Scania AB, and validated through interviews with nine industry professionals across Europe.

// ============================================================================
// SECTION 2 — SOFTWARE DESCRIPTION
// ============================================================================

= Software Description

The tool is a Python web application built on Streamlit. Users configure a charging station, run one or more analyses, and get itemized cost results they can export.

== Software Architecture

The code is split into three files totaling about 1,800 lines (@fig_architecture):

- *`app.py`* (~995 lines): the Streamlit front end. Collects inputs, validates them, shows results as Plotly charts, and handles Excel/PDF export.

- *`utils/calls.py`* (~325 lines): the orchestration layer. Checks whether LV or MV upgrades are needed (`medium_requirement`, `hard_requirement`), picks the project type (`case_definition`), runs all 19 cost functions (`compute_all_costs`), and drives the sensitivity sweeps.

- *`utils/cost.py`* (~490 lines): the 19 cost functions themselves. Each takes a physical quantity (apparent power, current, cable length, or area) and returns a cost in 2024 euros, using lookup tables and fitted curves from industrial catalogs and published data.

In practice: the user fills in the input form; `calls.py` validates the inputs, determines the project type (1--4), and calls each relevant cost function with the right sizes; the results land in an itemized table and interactive charts.

#figure(
  image("figures/Figure 1.png", width: 100%),
  caption: [Software architecture overview.],
) <fig_architecture>

== Software Functionalities

*Input parameters.* The user provides 13 numbers and 3 categorical choices: how many chargers, at what power, what voltage levels, the existing grid connection capacity, cable distances, the power factor, and site preparation details (land area, surface material, terrain). The form also asks about LV and MV connection specifics: transformer capacity, distances to the nearest transformer and MV access point, and safety margins. Fields that do not apply to the current configuration are grayed out automatically; for example, MV parameters only appear when the planned load exceeds what the existing connection can supply (@fig_screenshot_input).

#figure(
  image("figures/Figure 3.png", width: 90%),
  caption: [Screenshot of the tool's web interface showing the input parameter form.],
) <fig_screenshot_input>

*Project type classification.* The tool compares the total planned load (chargers $times$ power / power factor) against the existing grid capacity and assigns one of four project types. *Type 1:* the connection already has enough capacity, so only the chargers need to be installed. *Type 2:* a small LV upgrade or new LV connection covers the gap. *Type 3:* a transformer exists on site but cannot handle the load, so a new MV connection is needed alongside it. *Type 4:* the site has only a basic LV connection and needs a full MV buildout from scratch. The type determines which cost components are included and which are zeroed out. @fig_flowchart shows the decision logic.

#figure(
  image("figures/Figure 2.pdf", width: 60%),
  caption: [Flowchart for automatic project type classification.],
) <fig_flowchart>

*Investment cost model.* The model covers everything from the grid connection point to the charging plug (@fig_components) and computes 15 cost items through 19 functions in three groups. *MV/substation equipment:* MVAC cables (exponential fit to current and length), transformer (power-law scaling from apparent power @csanyi_trafo), MV switchgear (score-based on voltage, current, and configuration), surge arresters and grounding resistors (lookup by voltage @ieee_142). *LV equipment:* LVAC cables (linear, Type 2 only), LV switchboard (linear on current), rectifier (222 €/kW in 200 kW modules; absent below 40 kW), LVDC cables (linear on current, distance, and charger count), chargers or DC dispensers (interpolated lookup, 10--350 kW @acea_masterplan). *Labor and site work:* planning and installation (linear on charger count and power @icct_costs @acea_masterplan), MV and LV cable installation (from expert interview data and cable cost @expert_interviews), site preparation (€/m#super[2] by material and terrain). Any component that does not apply to the selected project type returns zero.

#figure(
  image("figures/Figure X.png", width: 95%),
  caption: [General layout of a high-power charging station with centralized conversion.],
) <fig_components>

*Analysis modes.* Three modes are available. *Cost Breakdown* produces a full itemized table for the exact configuration, exportable to Excel. *Single-Variable Sensitivity* lets the user sweep one or more parameters across a range while holding everything else fixed; the result is a stacked bar chart showing how each component changes. *Two-Parameter Sensitivity* sweeps two parameters at once, displayed as a scatter plot color-coded by the second parameter, with full component breakdowns on hover.

*Export and deployment.* Every analysis can be exported to Excel. The tool also generates a PDF report with all inputs, tables, and charts included. It runs locally with `streamlit run app.py` or on a cloud host like Streamlit Community Cloud. No installation is needed beyond Python 3.10 and the packages in `requirements.txt`.

// ============================================================================
// SECTION 3 — ILLUSTRATIVE EXAMPLES
// ============================================================================

= Illustrative Examples

We applied the tool to nine real sites across Germany, Italy, and the United Kingdom, chosen to cover all four project types at different scales. Site selection started from a spatial analysis that cross-referenced truck stop locations @plötz_truckstops with nearby high-power chargers from Open Charge Map @open_charge_map, specifically CCS stations of at least 100 kW within 200 meters of a truck stop. The logic: if high-power chargers already exist nearby, there is likely MV grid capacity in the area. @tab_cases lists the nine cases.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    inset: 6pt,
    align: center,
    stroke: 0.5pt,
    table.header(
      [*Case*], [*Type*], [*Country*], [*Chargers*], [*Power [kW]*], [*Grid [kVA]*], [*Transformer*],
    ),
    [1IT], [1], [Italy],   [3],  [200], [650],  [Yes],
    [3IT], [3], [Italy],   [20], [160], [1800], [Yes],
    [4IT], [4], [Italy],   [10], [200], [200],  [No],
    [1DE], [1], [Germany], [20], [160], [2100], [Yes],
    [2DE], [2], [Germany], [4],  [100], [30],   [No],
    [4DE], [4], [Germany], [40], [20],  [50],   [No],
    [2UK], [2], [UK],      [10], [200], [1800], [Yes],
    [3UK], [3], [UK],      [30], [160], [2100], [Yes],
    [4UK], [4], [UK],      [20], [160], [200],  [No],
  ),
  caption: [Overview of the nine case studies.],
) <tab_cases>

Results span a wide range: roughly €20,000 per plug for large Type 1 sites down to over €80,000 for small Type 4 projects (@fig_cost_per_plug). The pattern is consistent across countries. Specific cost (€/kW) drops as installed power grows. Economies of scale are real, but they hit a floor. For Type 1 projects, chargers, rectifiers, and installation labor make up most of the bill, and specific cost falls from above 1,500 €/kW at 10 kW to below 800 €/kW at 150 kW. Type 4 projects carry the extra burden of a full MV buildout (transformer, switchgear, MV cables, trenching), which does not scale as well; their specific cost drops to about 1,000--1,100 €/kW and then levels off (@fig_sensitivity). The gap between Type 1 and Type 4 at the same power level is roughly 60% MV equipment and 40% additional labor.

#figure(
  image("figures/Figure 5.pdf", width: 85%),
  caption: [Investment cost per plug as a function of deployment scale, for 20 kW and 100 kW chargers.],
) <fig_cost_per_plug>

@fig_case_costs breaks down each case by component. Case 3UK costs the most in absolute terms (30 chargers at 160 kW with a new MV connection), but its per-kW cost is among the lowest because the fixed MV costs are spread over 4.8 MW of capacity. Smaller projects like 2DE and 1IT stay under €500,000 total but pay more per kilowatt.

#figure(
  image("figures/Figure 6.pdf", width: 90%),
  caption: [Investment cost and specific cost (€/kW) for the nine public parking case studies.],
) <fig_case_costs>

#figure(
  image("figures/Figure 7.pdf", width: 75%),
  caption: [Investment cost comparison: Type 1 vs. Type 4 projects for 20 kW and 100 kW chargers as a function of total installed power.],
) <fig_sensitivity>

// ============================================================================
// SECTION 4 — IMPACT
// ============================================================================

= Impact

AFIR requires over 300,000 truck charging points across Europe by 2030, at an estimated €7 billion @afir @mckinsey_charging. That money will be spent site by site, and the range of per-plug costs (€20,000--€80,000) means design choices matter.

Fleet operators can use the tool before committing to a project: compare high-power versus low-power chargers, check whether an LV upgrade is enough or an MV connection is unavoidable, and see which parameters move the total cost most. Policymakers can use the same numbers to design subsidies, set grid connection policies, or decide which TEN-T corridor locations to prioritize.

For researchers, the value is in the open, modular structure. Every cost function can be inspected, modified, or replaced. If MCS connector pricing data becomes available, or if a user wants to plug in local labor rates for a country not covered here, the lookup tables can be edited directly @charin_mcs @hola_mcs. The tool was built with Scania AB and tested against input from nine industry professionals @expert_interviews. It pairs well with FleetRL @cording_fleetrl, which handles the operational side (charging schedules and electricity costs). Together, the two tools cover both the capital and operational parts of the picture.

// ============================================================================
// SECTION 5 — CONCLUSIONS
// ============================================================================

= Conclusions

This paper has introduced an open-source tool that estimates the investment cost of overnight HDV charging infrastructure in Europe, covering 19 cost components from the grid connection to the plug. It classifies projects into four types by grid connection requirement and supports cost breakdown, single-variable, and two-parameter sensitivity analysis through a web interface.

Across nine case studies in Germany, Italy, and the UK, costs range from about €20,000 per plug (large Type 1 sites with existing grid capacity) to over €80,000 (small Type 4 sites needing a full MV buildout). Economies of scale are real but have a floor: MV equipment adds a fixed layer that does not shrink much with more chargers. For Type 1 projects, chargers and installation dominate; for Type 3 and 4, the transformer, switchgear, and MV cabling become the main differentiator.

Next steps include adding electricity cost optimization and levelized cost of charging (LCOC) calculations, lead time estimation by project type, updated pricing for Megawatt Charging System (MCS) connectors as that standard matures, and scaling the methodology to regional deployment planning.

// ============================================================================
// CRediT, Declarations, Acknowledgments
// ============================================================================

#heading(numbering: none)[CRediT Authorship Contribution Statement]

*Davide Ferraro:* Writing -- original draft, Software, Methodology, Investigation, Formal analysis, Data curation, Visualization, Validation. *Jagruti Thakur:* Writing -- review & editing, Supervision, Methodology, Conceptualization, Resources, Project administration.

#heading(numbering: none)[Declaration of Competing Interest]

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

#heading(numbering: none)[Acknowledgments]

The authors thank Antonius Kies (Scania AB) for industrial supervision and guidance, and the nine industry professionals who participated in expert interviews to validate assumptions and provide cost data.

#heading(numbering: none)[Data Availability]

The source code is available at https://github.com/davide-ferraro/ev-charging-cost-estimator. The full methodology and data sources are documented in the accompanying master's thesis report, available at https://kth.diva-portal.org/smash/record.jsf?pid=diva2%3A2007635.

// ============================================================================
// BIBLIOGRAPHY
// ============================================================================

#pagebreak()

#bibliography("references.yml", style: "elsevier-with-titles")
