// ============================================================
// SoftwareX paper: Investment Cost Estimation Tool for
// Overnight HDV Charging Infrastructure
// Import figures from typst_pictures/
// ============================================================

#set page(margin: (x: 2.5cm, y: 3cm))
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.1")

// ── Title block ─────────────────────────────────────────────
#align(center)[
  #text(size: 14pt, weight: "bold")[
    Investment Cost Estimation Tool for Overnight Charging \
    Infrastructure of Heavy-Duty Vehicles in Europe
  ]

  #v(0.6em)
  #text(size: 11pt)[Davide Ferraro, Jagruti Thakur, Maria Carolina Gil Ribeiro]

  #text(size: 10pt, style: "italic")[
    KTH Royal Institute of Technology, Stockholm, 11428, Sweden \
    Corresponding author: jrthakur\@kth.se (Jagruti Thakur)
  ]
]

#v(1em)
#line(length: 100%)
#v(0.5em)

// ── Keywords ─────────────────────────────────────────────────
*Keywords:* Heavy-duty vehicles · Depot charging · Investment cost modeling · Charging infrastructure · Grid connection · Techno-economic analysis · Decision-support tool

#v(0.5em)
#line(length: 100%)

// ── Abstract ─────────────────────────────────────────────────
#v(0.5em)
*Abstract*

The deployment of overnight charging infrastructure for battery-electric heavy-duty vehicles (HDVs) is critical for decarbonizing European freight transport, yet decision-makers lack transparent, component-level cost estimation tools. This paper introduces an open-source, web-based investment cost calculator for overnight depot and public parking charging stations. The tool takes site-specific electrical parameters as input (number and power of chargers, grid connection type, voltage levels, cable distances, and site conditions) and automatically determines the project type (one of four categories based on grid connection requirements). It then sizes every electrical component from the grid connection point to the charging plug and computes itemized costs using real-world pricing data. The tool supports three analysis modes: cost breakdown, single-variable sensitivity, and two-parameter sensitivity analysis, enabling users to explore how different design choices affect total investment cost. Applied to nine case studies across Germany, Italy, and the United Kingdom, the tool produces investment costs ranging from €20,000 to €80,000 per charging plug, depending on grid connection type, charger power level, and deployment scale.

#v(0.5em)
#line(length: 100%)

// ── Code Metadata ────────────────────────────────────────────
#v(0.5em)
*Code Metadata*

#figure(
  table(
    columns: (auto, 1fr),
    stroke: 0.5pt,
    fill: (col, row) => if row == 0 { luma(230) } else { white },
    [*Field*], [*Value*],
    [Current code version], [v1.0.0],
    [Permanent link to repository], [https://github.com/davide-ferraro/ev-charging-cost-estimator],
    [Legal Code License], [MIT],
    [Code versioning system], [git],
    [Languages, tools and services], [Python, Streamlit, Plotly, Pandas, NumPy, OpenPyXL],
    [Operating environments and dependencies], [Python ≥ 3.10],
    [Link to developer documentation], [https://kth.diva-portal.org/smash/record.jsf?pid=diva2%3A2007635],
    [Support email], [davideferraro275\@gmail.com],
  )
)

#pagebreak()

// ── 1. Motivation and Significance ───────────────────────────
= Motivation and Significance

Battery-electric trucks are entering the European market at a pace that the charging infrastructure has not kept up with. Heavy-duty vehicles (HDVs) account for over a quarter of EU road transport greenhouse gas emissions and roughly 6% of total EU emissions, despite being a small share of the fleet [1]. The EU's "Fit for 55" package now mandates CO#sub[2] reductions of 45% by 2030, 65% by 2035, and 90% by 2040 for new HDVs [1]. Since electric trucks produce no tailpipe CO#sub[2], they count as zero-emission under these rules, which is a direct incentive for manufacturers and fleet operators to go electric [2]. Battery costs have fallen enough that electric trucks now work across most freight segments [3,4], and McKinsey expects most e-truck operators to prefer overnight depot charging for its predictable schedules and cheap off-peak electricity [5].

The problem is on the infrastructure side. A single long-haul truck battery can hold 300--800 kWh, and a depot charging multiple trucks at once may need several megawatts of grid capacity [3,4,6]. The Alternative Fuels Infrastructure Regulation (AFIR) requires EU Member States to install at least 3.6 MW of truck charging capacity every 60 km along the core road network by 2030 [7]. Europe had roughly 10,000 public truck charging points in 2023; that number needs to reach 300,000 by the end of the decade, at an estimated cost of €7 billion [8]. Most existing depots cannot supply this kind of power, and getting a grid connection upgraded is slow, expensive, and tangled in permitting, sometimes taking years [9].

These infrastructure challenges are compounded by a lack of reliable cost estimation tools. Charging infrastructure for trucks requires high-power chargers, heavy electrical equipment, and site-specific civil works. Fleet managers and investors rarely have clear numbers for how costs change across different configurations [10]. For instance, how much more a depot serving fifty trucks costs compared to one serving five, or what the price difference is between a site that already has a medium-voltage (MV) connection and one that needs a new one built from scratch. Borlaug et al. [10] found that smaller U.S. depots can often avoid costly grid upgrades, but larger sites typically need high-power connections and new substations. The ICCT notes that transformer sizing, permitting rules, and site characteristics create wide cost variation even within a single country [6]. Burton et al. [11] showed that utilities can cut grid-related costs by sizing components around actual truck usage patterns rather than peak demand. Still, the literature mostly reports cost in broad categories ("equipment," "labor," "grid fees") without breaking it down to individual components like cable cross-sections or switchgear ratings [4,8]. Most studies also focus on North America [10,12], where electricity pricing, grid regulations, and equipment standards differ from Europe. Lead time and permitting data is scarce as well [9,13].

Several software tools and models address parts of the EV charging cost problem, but they fall into three groups that each leave the target case uncovered. The first group computes the levelized cost of charging (LCOC), a per-kilowatt-hour operating metric rather than an upfront capital cost. Borlaug et al. [10] built the reference LCOC framework for the United States and released it as the open-source lcoc-ldevs tool, but it targets light-duty vehicles and folds equipment and installation into an amortized input rather than producing a component breakdown. Lanz et al. [23] applied a similar LCOC approach across 30 European countries, yet their model covers passenger transport only and deliberately leaves grid connection costs out. The Atlas Public Policy charging cost calculator [24] works the same way, estimating the electricity cost of a given charging pattern rather than the hardware and connection investment. The second group is the set of planning and simulation tools in the U.S. Department of Energy EVI-X suite [22]. These project charging demand, simulate site energy use, or run financial scenarios, and they are explicit that capital cost estimation is not their job: the financial tool EVI-FAST asks the user to supply equipment and installation costs from vendor quotes rather than deriving them. Open-source interactive tools in the same family take aim at charging operation or grid impacts rather than capital cost: datafev [28] is a Python framework for charging management and scheduling algorithms, and EV-EcoSim [29] is a grid-aware co-simulation and optimization platform that does quantify cost, but as the levelized cost of grid and distributed-energy-resource components in a United States, light-duty context rather than a component-level capital breakdown of the station from the grid connection to the plug. The third group is the static, component-level cost literature. The AFDC report on non-residential charging equipment [12] and the ICCT metropolitan-area analysis [25] both split installation cost into hardware, labor, permitting, and grid connection, but they are published as fixed tables and figures rather than interactive software, and both describe U.S. passenger charging with data that is now roughly a decade old.

Work specific to heavy-duty depot charging is more recent and still leaves the niche open. Borlaug et al. [26] examined how depot charging stresses the electricity distribution system and released a load-profile generator, but their focus is grid upgrade cost and load shapes rather than a station-level investment breakdown. Wang et al. [27] come closest in intent, building a component-level bottom-up cost model for medium- and heavy-duty depot charging in California, yet they publish it as a methodology and dataset rather than a reusable interactive tool, and the costs are specific to the United States. FleetRL [14] is a reinforcement-learning environment for scheduling fleet charging and minimizing electricity cost; it models charging operation, not the physical infrastructure or its capital cost, so it complements rather than overlaps with the present tool. Across all of these, no open-source, interactive tool estimates component-level investment cost from the medium-voltage grid connection to the charging plug for European heavy-duty overnight charging, which is the gap this software fills.

This paper fills that gap with the first open-source, web-based tool for estimating overnight charging infrastructure investment costs for battery-electric HDVs in Europe. The tool models 15 individual cost components from the grid connection to the plug, using real equipment pricing data in 2024 euros from catalogs, suppliers, and published studies. It automatically classifies projects into four types based on grid connection requirements: Type 1 where the existing connection already has sufficient capacity, Type 2 where a small LV upgrade covers the gap, Type 3 where a new MV connection is needed alongside an existing on-site transformer, and Type 4 where a full MV buildout is required from scratch. The type determines which cost components are activated. The tool supports cost breakdown, single-variable, and two-parameter sensitivity analyses, and runs as a Streamlit web application that requires no installation and produces interactive charts and downloadable reports. It was developed at KTH Royal Institute of Technology with Scania AB, with cost assumptions informed by interviews with nine industry professionals across Europe.

// ── 2. Software Description ──────────────────────────────────
= Software Description

The tool is a Python web application built on Streamlit. Users configure a charging station, run one or more analyses, and get itemized cost results they can export.

== Software Architecture

The tool follows a three-layer architecture. The *presentation layer* (`app.py`, ~995 lines) collects the 16 user inputs through a Streamlit widget form, re-renders the interface on every change to enable or disable fields that depend on the current configuration, and displays results as interactive Plotly charts with Excel and PDF export. The *orchestration layer* (`utils/calls.py`, ~325 lines) validates inputs, runs `medium_requirement()` and `hard_requirement()` to check whether the existing grid connection can handle the planned load, calls `case_definition()` to assign one of four project types, and calls `compute_all_costs()` which dispatches to every relevant cost function. The *computational layer* (`utils/cost.py`, ~490 lines) contains the 15 cost functions, each of which takes one or more physical quantities and returns a cost in 2024 euros using lookup tables or fitted curves from industrial catalogs and published studies, together with a few shared helper routines for table lookup and unit conversion.

Data flows through four stages, shown in @fig1. The user's 16 input parameters feed the project type classifier and the electrical sizing calculations in parallel. The project type (1--4) gates which sizing calculations are active and which cost functions return non-zero values. The sized electrical quantities (current I [A], apparent power S [kVA], total power P [kW], and voltage V [kV]) feed 15 cost functions. Each cost function produces one line item in euros. Because Streamlit re-executes the script on every widget change, the project type classification and the field-enable logic run automatically on every interaction without any explicit callback wiring. The electrical sizing and cost calculations, by contrast, are triggered only when the user clicks the Run Analysis button.

#figure(
  image("typst_pictures/fig1_pipeline_abstract.png", width: 100%),
  caption: [Data pipeline overview, with the three architectural layers shown as bands. The presentation layer (`app.py`) holds the user inputs, the orchestration layer (`calls.py`) performs the project type classification, and the computational layer (`cost.py`) contains the electrical sizing calculations and the cost functions. User inputs feed the project type classifier and the sizing calculations in parallel; the project type (1--4) gates which sizing calculations and cost functions are active; and the sized electrical quantities (I, S, P, V) feed 15 cost functions, each producing one line item in euros.],
) <fig1>

== Software Functionalities

*Input parameters.* The tool takes 13 numerical and 3 categorical inputs. The charger parameters, namely the number of chargers $n$, power per charger $P$ [kW], and load power factor $"pf"$, drive the planned apparent load calculation and appear in nearly every cost function. The grid and connection parameters cover the existing grid connection capacity $G$ [kVA], LV and MV voltage levels, available transformer capacity, maximum LV connection power, whether a transformer is already present on site, and the transformer safety margin; together these determine the project type and size the MV and LV electrical equipment. The distance and site parameters capture cable runs from the rectifier to the chargers, from the premises to the nearest MV/LV transformer, and to the nearest MV access point, as well as the land area, pavement material, and terrain type that determine cable costs and site preparation cost.

The planned apparent load is computed as $S = n dot P slash "pf"$ [kVA] and compared against the existing grid connection capacity $G$. If $S$ is at most $G$ the existing connection is sufficient and the project is classified as Type 1. Otherwise, the uncovered load $S - G$ is compared against the local LV connection threshold: if it fits within LV limits a simple LV upgrade suffices (Type 2), and if it exceeds them a new MV connection is needed (Types 3 and 4). Once the type is known, only the relevant cost components are activated, and fields that do not apply are grayed out in the interface automatically (@fig2).

#figure(
  image("typst_pictures/fig2_interface_screenshot.png", width: 95%),
  caption: [Screenshot of the tool's web interface showing the input parameter form.],
) <fig2>

*Project type classification.* The tool compares the total planned load (chargers × power / power factor) against the existing grid capacity and assigns one of four project types. Type 1 means the connection already has enough capacity, so only the chargers need to be installed. Type 2 means a small LV upgrade or new LV connection covers the gap. Type 3 means a transformer exists on site but cannot handle the load, so a new MV connection is needed alongside it. Type 4 means the site has only a basic LV connection and needs a full MV buildout from scratch. The type determines which cost components are included and which are zeroed out. @fig3 shows the decision logic.

#figure(
  image("typst_pictures/fig3_classification_flowchart.pdf", width: 80%),
  caption: [Flowchart for automatic project type classification.],
) <fig3>

*Investment cost model.* The model covers everything from the grid connection point to the charging plug (@fig4) and computes the 15 cost items in three groups. @fig5 shows three representative examples of how inputs flow through the pipeline to produce a cost in euros, ranging from a simple passthrough (Chargers) to a linear sizing calculation (Transformer) to a chained function (MV Connection Cost, which takes the MV cable material cost as its own input).

The key intermediate calculations that size electrical components are shown in @tab-sizing, and the cost functions that map those quantities to euros are listed in @tab-costs.

#figure(
  table(
    columns: (auto, 1fr),
    stroke: 0.5pt,
    fill: (col, row) => if row == 0 { luma(230) } else { white },
    [*Quantity*], [*Formula*],
    [Planned apparent load], [$S = n dot P slash "pf"$ [kVA]],
    [LV current], [$I = (n dot P dot 1000) / (sqrt(3) dot V_"LV")$ [A]],
    [MV current (Type 3)], [$I = (n dot P slash "pf" - G) / (sqrt(3) dot V_"MV")$ [A]],
    [MV current (Type 4)], [$I = (n dot P slash "pf") / (sqrt(3) dot V_"MV")$ [A]],
    [Transformer rating], [$S_T = (n dot P slash "pf" - G) dot (1 + "margin" slash 100)$ [kVA]],
    [Rectifier modules], [$k = ceil(n dot P slash 200)$],
  ),
  caption: [Key intermediate calculations for electrical component sizing.],
) <tab-sizing>

#figure(
  table(
    columns: (auto, auto, 1fr),
    stroke: 0.5pt,
    fill: (col, row) => if row == 0 { luma(230) } else { white },
    [*Component*], [*Formula type*], [*Key formula*],
    [LV/DC cables], [Linear], [$C = 0.276 dot I dot "dist"$ [€]],
    [MV cables], [Exponential], [$C = 53.976 dot e^(0.0034 dot I) dot "dist"$ [€]],
    [LV cabinet], [Linear], [$C = 10.319 dot I - 900.26$ [€]],
    [Rectifier], [Step], [$C = k dot 44\,400$ [€]],
    [Transformer], [Lookup table], [$S_T$ [kVA] → catalog price [€]],
    [MV switchgear], [Weighted linear], [$C = "base" + sum w_i x_i$ [€]],
    [Surge arresters], [Lookup table], [$V_"MV"$ [kV] → catalog price [€]],
    [Charger planning], [Linear], [$C = n dot (25.064 dot P + 275.07)$ [€]],
    [Charger installation], [Linear], [$C = n dot (155.83 dot P + 5822.5)$ [€]],
    [Site preparation], [Lookup table], [$C = A dot r,\ r in {45.2, 55.2, 150.6}$ [€/m²]],
  ),
  caption: [Cost functions mapping electrical quantities to euros.],
) <tab-costs>

On the MV and substation side, the model prices MVAC cables through an exponential fit to current and length, sizes the transformer through power-law scaling from apparent power [15], rates the MV switchgear through a weighted score on voltage, current, and configuration, and prices surge arresters and grounding resistors from a voltage-indexed lookup table [16]. The LV equipment group covers LVAC distribution cables applicable to Type 2 only and priced linearly on current, the LV switchboard also priced linearly on current, the rectifier at 222 €/kW in 200 kW modules and absent for charger power below 40 kW, LVDC cables from the rectifier to the chargers, and the chargers or DC dispensers themselves priced through an interpolated lookup over the 10 to 350 kW range [4]. Labor and site work are captured through linear regressions for charger planning and installation costs based on charger count and power [4,6], cable installation costs derived from expert interview data and cable material cost [17], and site preparation at a fixed rate per square metre depending on pavement material and terrain type. Any component that does not apply to the selected project type returns zero.

#figure(
  image("typst_pictures/fig4_station_layout.png", width: 90%),
  caption: [General layout of a high-power charging station with centralized conversion.],
) <fig4>

*Analysis modes.* Three modes are available. Cost Breakdown produces a full itemized table for the exact configuration, exportable to Excel. Single-Variable Sensitivity sweeps one parameter across a user-defined range while holding everything else fixed. Because the swept parameter passes through the full pipeline on every step, increasing the number of chargers, for example, can shift the project type mid-sweep from Type 1 to Type 3 once the planned load exceeds the grid connection capacity, which in turn activates a different set of cost components; the resulting stacked bar chart makes these discontinuities visible. Two-Parameter Sensitivity sweeps two parameters at once and displays the results as a scatter plot color-coded by the second parameter, with full component breakdowns on hover. In both sensitivity modes, every evaluation re-runs the complete pipeline covering project type classification, electrical sizing, and cost computation, so the output reflects the true non-linear response of the cost model to input variation.

*Export and deployment.* Every analysis can be exported to Excel. The tool also generates a PDF report with all inputs, tables, and charts included. It runs locally with `streamlit run app.py` or on a cloud host like Streamlit Community Cloud. No installation is needed beyond Python 3.10 and the packages in `requirements.txt`.

#figure(
  image("typst_pictures/fig5_pipeline_examples.png", width: 100%),
  caption: [Three representative cost item pipelines. (a) Chargers: inputs $n$ and $P$ pass directly through a lookup table. (b) Transformer: six inputs drive a linear sizing calculation producing $S$ [kVA], which indexes a catalog lookup table. (c) MV Connection Cost: a chained function that takes the MV cable material cost as input rather than raw electrical quantities.],
) <fig5>

// ── 3. Illustrative Examples ─────────────────────────────────
= Illustrative Examples

The tool is applied to nine real sites across Germany, Italy, and the United Kingdom, chosen to cover all four project types at different scales. Site selection started from a spatial analysis that cross-referenced truck stop locations [18] with nearby high-power chargers from Open Charge Map [19], specifically CCS stations of at least 100 kW within 200 meters of a truck stop. The logic is that if high-power chargers already exist nearby, there is likely MV grid capacity in the area. @tab-cases lists the nine cases.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    stroke: 0.5pt,
    fill: (col, row) => if row == 0 { luma(230) } else { white },
    [*Case*], [*Type*], [*Country*], [*Chargers*], [*Power [kW]*], [*Grid [kVA]*], [*Transformer*],
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
) <tab-cases>

Results span a wide range: roughly €20,000 per plug for large Type 1 sites down to over €80,000 for small Type 4 projects (@fig6). The pattern is consistent across countries. Specific cost (€/kW) drops as installed power grows, but the savings flatten out at higher power. For Type 1 projects, chargers, rectifiers, and installation labor make up most of the bill, and specific cost falls from above 1,500 €/kW at 10 kW to below 800 €/kW at 150 kW. Type 4 projects carry the extra burden of a full MV buildout (transformer, switchgear, MV cables, trenching), which does not scale as well; their specific cost drops to about 1,000--1,100 €/kW and then levels off. The gap between Type 1 and Type 4 at the same power level is roughly 60% MV equipment and 40% additional labor.

#figure(
  image("typst_pictures/fig6_cost_per_plug.pdf", width: 95%),
  caption: [Investment cost per plug as a function of deployment scale, for 20 kW and 100 kW chargers.],
) <fig6>

@fig7 breaks down each case by component. Case 3UK costs the most in absolute terms (30 chargers at 160 kW with a new MV connection), but its per-kW cost is among the lowest because the fixed MV costs are spread over 4.8 MW of capacity. Smaller projects like 2DE and 1IT stay under €500,000 total but pay more per kilowatt.

#figure(
  image("typst_pictures/fig7_case_studies.pdf", width: 95%),
  caption: [Investment cost and specific cost (€/kW) for the nine public parking case studies.],
) <fig7>

// ── 4. Impact ────────────────────────────────────────────────
= Impact

The tool provides decision-makers with a fast, transparent way to estimate and compare overnight HDV charging infrastructure costs before committing to a project. Fleet operators, infrastructure developers, and policymakers can use it to understand how site-specific design choices such as charger count and power, grid connection type, and cable distances drive total investment cost. AFIR requires over 300,000 truck charging points across Europe by 2030 at an estimated €7 billion [7,8], and the range of per-plug costs found here (€20,000--€80,000) shows that informed design choices can make a substantial difference in how that budget is spent.

In practice, an operator can compare high-power against low-power chargers, check whether an LV upgrade is sufficient or an MV connection is unavoidable, and see which parameters move the total cost most. Policymakers can draw on the same results to design subsidy schemes, set grid connection standards, or decide which TEN-T corridor locations to prioritize for public charging infrastructure.

For researchers, the value lies in the open, modular structure of the codebase. Every cost function can be inspected, modified, or replaced with local data, and if MCS connector pricing becomes available or a user wants to substitute labor rates for a specific country, the relevant lookup tables can be edited directly [20,21]. The tool was developed in collaboration with Scania AB, with cost assumptions informed by interviews with nine industry professionals [17]. On the operational side it complements FleetRL [14], so that together the two tools cover both the capital investment and the ongoing operational costs of electric truck depot charging.

// ── 5. Conclusions ───────────────────────────────────────────
= Conclusions

This paper has introduced an open-source tool that estimates the investment cost of overnight HDV charging infrastructure in Europe, covering 15 cost components from the grid connection to the plug. It classifies projects into four types by grid connection requirement and supports cost breakdown, single-variable, and two-parameter sensitivity analysis through a web interface.

Across nine case studies in Germany, Italy, and the UK, costs range from about €20,000 per plug (large Type 1 sites with existing grid capacity) to over €80,000 (small Type 4 sites needing a full MV buildout). Economies of scale are real but have a floor: MV equipment adds a fixed layer that does not shrink much with more chargers. For Type 1 projects, chargers and installation dominate; for Type 3 and 4, the transformer, switchgear, and MV cabling become the main differentiator.

Future work will extend the tool in several directions. The most significant addition would be electricity cost optimization and levelized cost of charging (LCOC) calculations, which would allow users to compare not just the capital investment but the full cost of ownership across configurations. Shorter-term extensions include lead time estimation by project type, updated pricing for Megawatt Charging System (MCS) connectors as that standard matures in the European market, and tools for scaling the methodology from individual sites to regional deployment planning.

// ── Back matter ──────────────────────────────────────────────
#line(length: 100%)

*CRediT Authorship Contribution Statement*

*Davide Ferraro:* Writing -- original draft, Software, Methodology, Investigation, Formal analysis, Data curation, Visualization, Validation. *Jagruti Thakur:* Writing -- review & editing, Supervision, Methodology, Conceptualization, Resources, Project administration. *Maria Carolina Gil Ribeiro:* Writing -- review & editing.

*Declaration of Competing Interest*

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

*Acknowledgments*

The authors thank Antonius Kies (Scania AB) for industrial supervision and guidance, and the nine industry professionals who participated in expert interviews to validate assumptions and provide cost data.

*Data Availability*

The source code is available at https://github.com/davide-ferraro/ev-charging-cost-estimator. The full methodology and data sources are documented in the accompanying master's thesis report, available at https://kth.diva-portal.org/smash/record.jsf?pid=diva2%3A2007635.

// ── Bibliography ─────────────────────────────────────────────
#line(length: 100%)

*References*

#set par(hanging-indent: 1.5em)

[1] European Commission, Heavy-duty vehicles, (2024). https://climate.ec.europa.eu/eu-action/transport-decarbonisation/road-transport/heavy-duty-vehicles_en

[2] Climate Change Connection, Tailpipe Emissions, (n.d.). https://climatechangeconnection.org/emissions/tailpipe-emissions/

[3] International Energy Agency (IEA), Global EV Outlook 2023, (2023). https://www.iea.org/reports/global-ev-outlook-2023

[4] ACEA, ChargeUp Europe, Transport & Environment, A European EV Charging Infrastructure Masterplan, (2022).

[5] McKinsey & Company, Why most eTrucks will choose overnight charging, (2022).

[6] International Council on Clean Transportation, Estimating Charging Infrastructure Costs for Electric Trucks, (2022).

[7] Official Journal of the European Union, Regulation (EU) 2023/1804, (2023). https://eur-lex.europa.eu/eli/reg/2023/1804/oj/eng

[8] B. Broer et al., Building Europe's Electric-Truck Charging Infrastructure, McKinsey (2023).

[9] UK Department for Transport, Improving the Grid Connection Process for EV Charging Infrastructure, (2024).

[10] B. Borlaug, S. Salisbury, M. Gerdes, M. Muratori, Levelized Cost of Charging Electric Vehicles in the United States, Joule 4 (2020) 1470--1485.

[11] E. Burton et al., Evaluating Utility Cost Savings for Electric Vehicle Charging Infrastructure, NREL Report (2020).

[12] U.S. Department of Energy (AFDC), Costs Associated With Non-Residential Electric Vehicle Supply Equipment, (2015).

[13] Transport & Environment, Oeko-Institut, Fraunhofer ISI, Truck Depot Charging -- Final Report, (2022).

[14] E. Cording, J. Thakur, FleetRL: Realistic reinforcement learning environments for commercial vehicle fleets, SoftwareX 26 (2024) 101671.

[15] E. Csanyi, What is the price of a power transformer?, (2022). https://electrical-engineering-portal.com/price-of-a-transformer

[16] IEEE Std 142-2007, IEEE Recommended Practice for Grounding of Industrial and Commercial Power Systems, (2007).

[17] Synthesis of Expert Interviews: Charging Infrastructure for Battery Electric Trucks, (2024).

[18] P. Plötz, D. Speth, Truck Stop Locations in Europe: Final Report, Fraunhofer (2021).

[19] Open Charge Map project, Open Charge Map: Open Source Electric Vehicle Charging Stations. https://openchargemap.org/site

[20] CharIN e.V., Megawatt Charging System (MCS), (2024). https://www.charin.global/technology/mcs/

[21] HoLa Innovation Cluster, Megawatt Charging Networks (HoLa project), (2021).

[22] National Renewable Energy Laboratory, EVI-X Modeling Suite (EVI-Pro, EVI-FAST), NREL, (n.d.). https://www.nrel.gov/transportation/evi-x

[23] L. Lanz, B. Noll, T.S. Schmidt, B. Steffen, Comparing the levelized cost of electric vehicle charging options in Europe, Nature Communications 13 (2022) 5277. https://doi.org/10.1038/s41467-022-32835-7

[24] Atlas Public Policy, EV Charging Cost Calculator, (n.d.). https://atlaspolicy.com/ev-charging-cost-calculator/

[25] M. Nicholas, Estimating electric vehicle charging infrastructure costs across major U.S. metropolitan areas, ICCT Working Paper 2019-14, International Council on Clean Transportation (2019). https://theicct.org/publication/estimating-electric-vehicle-charging-infrastructure-costs-across-major-u-s-metropolitan-areas/

[26] B. Borlaug, M. Muratori, M. Gilleran, D. Woody, W. Muston, T. Canada, et al., Heavy-duty truck electrification and the impacts of depot charging on electricity distribution systems, Nature Energy 6 (2021) 673–682. https://doi.org/10.1038/s41560-021-00855-0

[27] G. Wang, M. Miller, L. Fulton, The infrastructure cost for depot charging of battery electric trucks, The Electricity Journal (2025). https://www.sciencedirect.com/science/article/abs/pii/S1040619025000351

[28] E. Gümrükcü, A. Ahmadifar, A. Yavuzer, F. Ponci, A. Monti, datafev: A Python framework for development and testing of management algorithms for electric vehicle charging infrastructures, Software Impacts 15 (2023) 100467. https://www.sciencedirect.com/science/article/pii/S2665963823000040

[29] E. Balogun, E. Buechler, S. Bhela, S. Onori, R. Rajagopal, EV-EcoSim: A grid-aware co-simulation platform for the design and optimization of electric vehicle charging infrastructure, IEEE Transactions on Smart Grid (2024). https://doi.org/10.1109/TSG.2023.3339374
