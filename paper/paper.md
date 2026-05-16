# Investment Cost Estimation Tool for Overnight Charging Infrastructure of Heavy-Duty Vehicles in Europe

**Davide Ferraro, Jagruti Thakur\***

*KTH Royal Institute of Technology, Stockholm, 11428, Sweden*

\* Corresponding author. *E-mail address:* jrthakur@kth.se (Jagruti Thakur).

---

## Article Info

**Keywords:**
Heavy-duty vehicles · Depot charging · Investment cost modeling · Charging infrastructure · Grid connection · Techno-economic analysis · Decision-support tool

## Abstract

The deployment of ==overnight== charging infrastructure for battery-electric heavy-duty vehicles (HDVs) is critical for decarbonizing European freight transport, yet decision-makers lack transparent, component-level cost estimation tools. This paper introduces an open-source, web-based investment cost calculator for overnight depot and public parking charging stations. The tool takes site-specific electrical parameters as input (number and power of chargers, grid connection type, voltage levels, cable distances, and site conditions) and automatically determines the project type (one of four categories based on grid connection requirements). It then sizes every electrical component from the grid connection point to the charging plug and computes itemized costs using real-world pricing data. The tool supports three analysis modes: cost breakdown, single-variable sensitivity, and two-parameter sensitivity analysis, enabling users to explore how different design choices affect total investment cost. Applied to nine case studies across Germany, Italy, and the United Kingdom, the tool produces investment costs ranging from €20,000 to €80,000 per charging plug, depending on grid connection type, charger power level, and deployment scale.

---

## Code Metadata

| Field | Value |
|---|---|
| Current code version | v1.0.0 |
| Permanent link to code/repository used for this code version | https://github.com/davide-ferraro/ev-charging-cost-estimator |
| Legal Code License | MIT |
| Code versioning system used | git |
| Software code languages, tools, and services used | Python, Streamlit, Plotly, Pandas, NumPy, OpenPyXL |
| Compilation requirements, operating environments & dependencies | Python ≥ 3.10 |
| If available, link to developer documentation/manual | https://kth.diva-portal.org/smash/record.jsf?pid=diva2%3A2007635 |
| Support email for questions | davideferraro275@gmail.com |

---

## 1 Motivation and Significance

Battery-electric trucks are entering the European market at a pace that the charging infrastructure has not kept up with. Heavy-duty vehicles (HDVs) account for over a quarter of EU road transport greenhouse gas emissions and roughly 6% of total EU emissions, despite being a small share of the fleet [1]. The EU's "Fit for 55" package now mandates CO₂ reductions of 45% by 2030, 65% by 2035, and 90% by 2040 for new HDVs [1]. Since electric trucks produce no tailpipe CO₂, they count as zero-emission under these rules, which is a direct incentive for manufacturers and fleet operators to go electric [2]. Battery costs have fallen enough that electric trucks now work across most freight segments [3,4], and McKinsey expects most e-truck operators to prefer overnight depot charging for its predictable schedules and cheap off-peak electricity [5].

The problem is on the infrastructure side. A single long-haul truck battery can hold 300–800 kWh, and a depot charging multiple trucks at once may need several megawatts of grid capacity [3,4,6]. The Alternative Fuels Infrastructure Regulation (AFIR) requires EU Member States to install at least 3.6 MW of truck charging capacity every 60 km along the core road network by 2030 [7]. Europe had roughly 10,000 public truck charging points in 2023; that number needs to reach 300,000 by the end of the decade, at an estimated cost of €7 billion [8]. Most existing depots cannot supply this kind of power, and getting a grid connection upgraded is slow, expensive, and tangled in permitting, sometimes taking years [9].

==Cost estimation makes this harder.== Charging infrastructure for ==passenger cars== is well studied, but trucks need bigger chargers, heavier electrical equipment, and site-specific civil works. Fleet managers and investors rarely have clear numbers for how costs change across different configurations [10]. For instance, how much more a depot serving fifty trucks costs compared to one serving five, or what the price difference is between a site that already has a medium-voltage (MV) connection and one that needs a new one built from scratch. Borlaug et al. [10] found that smaller U.S. depots can often avoid costly grid upgrades, but larger sites typically need high-power connections and new substations. The ICCT notes that transformer sizing, permitting rules, and site characteristics create wide cost variation even within a single country [6]. Burton et al. [11] showed that utilities can cut grid-related costs by sizing components around actual truck usage patterns rather than peak demand. Still, the literature mostly reports cost in broad categories ("equipment," "labor," "grid fees") without breaking it down to individual components like cable cross-sections or switchgear ratings [4,8]. Most studies also focus on North America [10,12], where electricity pricing, grid regulations, and equipment standards differ from Europe. Lead time and permitting data is scarce as well [9,13].

> **[REVIEW]** On *"Cost estimation makes this harder"*: What is this? what its harder?
>
> **[REVIEW]** On *"passenger cars"*: Are there softwares for passenger cars?

==No open-source tool currently lets a user enter site-specific parameters and get a component-level investment cost breakdown for an HDV charging station. FleetRL [14], published in SoftwareX, is a reinforcement learning environment for fleet charging optimization. It decides when and how much to charge but does not model the physical infrastructure or its cost. ICCT reports [6] give aggregate estimates in static PDFs, not interactive calculators. Borlaug et al. [10] defined the levelized cost of charging (LCOC) framework for the U.S. but did not publish a reusable tool. Nothing covers the full cost chain from the MV grid connection point to the DC charging plug for European HDV overnight charging.==

> **[REVIEW]** I think this literature review of softwares is short, and FleetRL is not even so related. What Types of softwares exist and which gap this software fills? For sure reviewers will ask for a more indeep review.

This paper fills that gap with the first open-source, web-based tool for estimating overnight charging infrastructure investment costs for battery-electric HDVs in Europe. The tool: (1) models 19 individual cost components from the grid connection to the plug; (2) automatically classifies projects into four types based on grid connection requirements; (3) uses real equipment pricing data in 2024 euros from catalogs, suppliers, and published studies; (4) supports cost breakdown, single-variable, and two-parameter sensitivity analyses; and (5) runs as a Streamlit web application that requires no installation and produces interactive charts and downloadable reports. It was developed at KTH Royal Institute of Technology with Scania AB, and validated through interviews with nine industry professionals across Europe.

---

## 2 Software Description

The tool is a Python web application built on Streamlit. Users configure a charging station, run one or more analyses, and get itemized cost results they can export.

### 2.1 Software Architecture

> **[REVIEW]** I think the whole Software Architecture section looks like a description of the code organization than an actual software architecture section. Right now it mainly lists the files (app.py, calls.py, cost.py) and explains what each one does, but it does not really describe the architecture of the system itself.
>
> The figure helps to show the overall workflow, but it still feels quite high level/generic. Maybe the section could focus more explicitly on the software layers/components and how they interact. For example, describing the Streamlit front end as the presentation layer, calls.py as the orchestration/logic layer, and cost.py as the computational layer containing the engineering/cost models.
>
> It would also help to explain the data flow more clearly. Right now that flow is implied but not really discussed in detail.

The code is split into three files totaling about 1,800 lines (Figure 1):

- **`app.py`** (~995 lines): the Streamlit front end. Collects inputs, validates them, shows results as Plotly charts, and handles Excel/PDF export.
- **`utils/calls.py`** (~325 lines): the orchestration layer. Checks whether LV or MV upgrades are needed (`medium_requirement`, `hard_requirement`), picks the project type (`case_definition`), runs all 19 cost functions (`compute_all_costs`), and drives the sensitivity sweeps.
- **`utils/cost.py`** (~490 lines): the 19 cost functions themselves. Each takes a physical quantity (apparent power, current, cable length, or area) and returns a cost in 2024 euros, using lookup tables and fitted curves from industrial catalogs and published data.

In practice: the user fills in the input form; `calls.py` validates the inputs, determines the project type (1–4), and calls each relevant cost function with the right sizes; the results land in an itemized table and interactive charts.

![Figure 1: Software architecture overview.](figures/Figure%201.png)

*Figure 1: Software architecture overview.*

### 2.2 Software Functionalities

**Input parameters.** The user provides 13 numbers and 3 categorical choices: how many chargers, at what power, what voltage levels, the existing grid connection capacity, cable distances, the power factor, and site preparation details (land area, surface material, terrain). The form also asks about LV and MV connection specifics: transformer capacity, distances to the nearest transformer and MV access point, and safety margins. Fields that do not apply to the current configuration are grayed out automatically; for example, MV parameters only appear when the planned load exceeds what the existing connection can supply (Figure 2).

> **[REVIEW]** In this section needs to introduce the main functions of the software and formulas. What is written is configuration, that can be place in other section.
>
> **[REVIEW]** Also, is not clear what are the things that can be choosen, where they fit in the software work flow.

![Figure 2: Screenshot of the tool's web interface showing the input parameter form.](figures/Figure%203.png)

*Figure 2: Screenshot of the tool's web interface showing the input parameter form.*

**Project type classification.** The tool compares the total planned load (chargers × power / power factor) against the existing grid capacity and assigns one of four project types. **Type 1:** the connection already has enough capacity, so only the chargers need to be installed. **Type 2:** a small LV upgrade or new LV connection covers the gap. **Type 3:** a transformer exists on site but cannot handle the load, so a new MV connection is needed alongside it. **Type 4:** the site has only a basic LV connection and needs a full MV buildout from scratch. The type determines which cost components are included and which are zeroed out. Figure 3 shows the decision logic.

![Figure 3: Flowchart for automatic project type classification.](figures/Figure%202.png)

*Figure 3: Flowchart for automatic project type classification.*

**Investment cost model.** The model covers everything from the grid connection point to the charging plug (Figure 4) and computes 15 cost items through 19 functions in three groups. **MV/substation equipment:** MVAC cables (exponential fit to current and length), transformer (power-law scaling from apparent power [15]), MV switchgear (score-based on voltage, current, and configuration), surge arresters and grounding resistors (lookup by voltage [16]). **LV equipment:** LVAC cables (linear, Type 2 only), LV switchboard (linear on current), rectifier (222 €/kW in 200 kW modules; absent below 40 kW), LVDC cables (linear on current, distance, and charger count), chargers or DC dispensers (interpolated lookup, 10–350 kW [4]). **Labor and site work:** planning and installation (linear on charger count and power [4,6]), MV and LV cable installation (from expert interview data and cable cost [17]), site preparation (€/m² by material and terrain). Any component that does not apply to the selected project type returns zero.

![Figure 4: General layout of a high-power charging station with centralized conversion.](figures/Figure%204.png)

*Figure 4: General layout of a high-power charging station with centralized conversion.*

**Analysis modes.** Three modes are available. **Cost Breakdown** produces a full itemized table for the exact configuration, exportable to Excel. **Single-Variable Sensitivity** lets the user sweep one or more parameters across a range while holding everything else fixed; the result is a stacked bar chart showing how each component changes. **Two-Parameter Sensitivity** sweeps two parameters at once, displayed as a scatter plot color-coded by the second parameter, with full component breakdowns on hover.

**Export and deployment.** Every analysis can be exported to Excel. The tool also generates a PDF report with all inputs, tables, and charts included. It runs locally with `streamlit run app.py` or on a cloud host like Streamlit Community Cloud. No installation is needed beyond Python 3.10 and the packages in `requirements.txt`.

---

## 3 Illustrative Examples

==We applied the tool== to nine real sites across Germany, Italy, and the United Kingdom, chosen to cover all four project types at different scales. Site selection started from a spatial analysis that cross-referenced truck stop locations [18] with nearby high-power chargers from Open Charge Map [19], specifically CCS stations of at least 100 kW within 200 meters of a truck stop. The logic: if high-power chargers already exist nearby, there is likely MV grid capacity in the area. Table 1 lists the nine cases.

> **[REVIEW]** The text should not include words like We. In this section, the tool is test using..

*Table 1: Overview of the nine case studies.*

| Case | Type | Country | Chargers | Power [kW] | Grid [kVA] | Transformer |
|------|------|---------|----------|------------|------------|-------------|
| 1IT  | 1    | Italy   | 3        | 200        | 650        | Yes         |
| 3IT  | 3    | Italy   | 20       | 160        | 1800       | Yes         |
| 4IT  | 4    | Italy   | 10       | 200        | 200        | No          |
| 1DE  | 1    | Germany | 20       | 160        | 2100       | Yes         |
| 2DE  | 2    | Germany | 4        | 100        | 30         | No          |
| 4DE  | 4    | Germany | 40       | 20         | 50         | No          |
| 2UK  | 2    | UK      | 10       | 200        | 1800       | Yes         |
| 3UK  | 3    | UK      | 30       | 160        | 2100       | Yes         |
| 4UK  | 4    | UK      | 20       | 160        | 200        | No          |

Results span a wide range: roughly €20,000 per plug for large Type 1 sites down to over €80,000 for small Type 4 projects (Figure 5). The pattern is consistent across countries. Specific cost (€/kW) drops as installed power grows. Economies of scale are real, but they hit a floor. For Type 1 projects, chargers, rectifiers, and installation labor make up most of the bill, and specific cost falls from above 1,500 €/kW at 10 kW to below 800 €/kW at 150 kW. Type 4 projects carry the extra burden of a full MV buildout (transformer, switchgear, MV cables, trenching), which does not scale as well; their specific cost drops to about 1,000–1,100 €/kW and then levels off (Figure 7). The gap between Type 1 and Type 4 at the same power level is roughly 60% MV equipment and 40% additional labor.

![Figure 5: Investment cost per plug as a function of deployment scale, for 20 kW and 100 kW chargers.](figures/Figure%205.png)

*Figure 5: Investment cost per plug as a function of deployment scale, for 20 kW and 100 kW chargers.*

Figure 6 breaks down each case by component. Case 3UK costs the most in absolute terms (30 chargers at 160 kW with a new MV connection), but its per-kW cost is among the lowest because the fixed MV costs are spread over 4.8 MW of capacity. Smaller projects like 2DE and 1IT stay under €500,000 total but pay more per kilowatt.

![Figure 6: Investment cost and specific cost (€/kW) for the nine public parking case studies.](figures/Figure%206.png)

*Figure 6: Investment cost and specific cost (€/kW) for the nine public parking case studies.*

![Figure 7: Investment cost comparison: Type 1 vs. Type 4 projects for 20 kW and 100 kW chargers as a function of total installed power.](figures/Figure%207.png)

*Figure 7: Investment cost comparison: Type 1 vs. Type 4 projects for 20 kW and 100 kW chargers as a function of total installed power.*

---

## 4 Impact

==AFIR requires over 300,000 truck charging points across Europe by 2030, at an estimated €7 billion [7,8]. That money will be spent site by site, and the range of per-plug costs (€20,000–€80,000) means design choices matter.==

> **[REVIEW]** I think this is not a good first sentence on Impact. Should be a clear sentence of the impact of the Tool. Where can be used and the benefits.

Fleet operators can use the tool before committing to a project: compare high-power versus low-power chargers, check whether an LV upgrade is enough or an MV connection is unavoidable, and see which parameters move the total cost most. Policymakers can use the same numbers to design subsidies, set grid connection policies, or decide which TEN-T corridor locations to prioritize.

For researchers, the value is in the open, modular structure. Every cost function can be inspected, modified, or replaced. If MCS connector pricing data becomes available, or if a user wants to plug in local labor rates for a country not covered here, the lookup tables can be edited directly [20,21]. The tool was built with Scania AB and tested against input from nine industry professionals [17]. It pairs well with FleetRL [14], which handles the operational side (charging schedules and electricity costs). Together, the two tools cover both the capital and operational parts of the picture.

---

## 5 Conclusions

This paper has introduced an open-source tool that estimates the investment cost of overnight HDV charging infrastructure in Europe, covering 19 cost components from the grid connection to the plug. ==It classifies projects into four types by grid connection requirement and supports cost breakdown, single-variable, and two-parameter sensitivity analysis through a web interface.==

> **[REVIEW]** This was not clear before in the document

Across nine case studies in Germany, Italy, and the UK, costs range from about €20,000 per plug (large Type 1 sites with existing grid capacity) to over €80,000 (small Type 4 sites needing a full MV buildout). Economies of scale are real but have a floor: MV equipment adds a fixed layer that does not shrink much with more chargers. For Type 1 projects, chargers and installation dominate; for Type 3 and 4, the transformer, switchgear, and MV cabling become the main differentiator.

Next steps include adding electricity cost optimization and levelized cost of charging (LCOC) calculations, lead time estimation by project type, updated pricing for Megawatt Charging System (MCS) connectors as that standard matures, and scaling the methodology to regional deployment planning.

---

## CRediT Authorship Contribution Statement

**Davide Ferraro:** Writing – original draft, Software, Methodology, Investigation, Formal analysis, Data curation, Visualization, Validation. **Jagruti Thakur:** Writing – review & editing, Supervision, Methodology, Conceptualization, Resources, Project administration.

## Declaration of Competing Interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Acknowledgments

The authors thank Antonius Kies (Scania AB) for industrial supervision and guidance, and the nine industry professionals who participated in expert interviews to validate assumptions and provide cost data.

## Data Availability

The source code is available at https://github.com/davide-ferraro/ev-charging-cost-estimator. The full methodology and data sources are documented in the accompanying master's thesis report, available at https://kth.diva-portal.org/smash/record.jsf?pid=diva2%3A2007635.

---

## Bibliography

[1] European Commission, Heavy-duty vehicles, (2024). https://climate.ec.europa.eu/eu-action/transport-decarbonisation/road-transport/heavy-duty-vehicles_en.

[2] Climate Change Connection, Tailpipe Emissions, (n.d.). https://climatechangeconnection.org/emissions/tailpipe-emissions/.

[3] International Energy Agency (IEA), Global EV Outlook 2023, (2023). https://www.iea.org/reports/global-ev-outlook-2023.

[4] ACEA, ChargeUp Europe, Transport & Environment, A European EV Charging Infrastructure Masterplan, (2022). https://www.acea.auto/files/Research-Whitepaper-A-European-EV-Charging-Infrastructure-Masterplan.pdf.

[5] McKinsey & Company, Why most eTrucks will choose overnight charging, (2022). https://www.mckinsey.com/industries/automotive-and-assembly/our-insights/why-most-etrucks-will-choose-overnight-charging.

[6] International Council on Clean Transportation, Estimating Charging Infrastructure Costs for Electric Trucks, (2022). https://theicct.org/wp-content/uploads/2022/12/charging-infrastructure-trucks-zeva-dec22.pdf.

[7] Official Journal of the European Union, Regulation (EU) 2023/1804 of the European Parliament and of the Council of 13 September 2023 on the deployment of alternative fuels infrastructure, and repealing Directive 2014/94/EU, (2023). https://eur-lex.europa.eu/eli/reg/2023/1804/oj/eng.

[8] B. Broer, A. Tschiesner, M. Stuchtey, N. Müller, W.G. Aulbur, Building Europe's Electric-Truck Charging Infrastructure, (2023). https://www.mckinsey.com/industries/automotive-and-assembly/our-insights/building-europes-electric-truck-charging-infrastructure.

[9] UK Department for Transport, Improving the Grid Connection Process for Electric Vehicle Charging Infrastructure, (2024). https://www.gov.uk/government/publications/improving-the-grid-connection-process-for-electric-vehicle-charging-infrastructure/improving-the-grid-connection-process-for-electric-vehicle-charging-infrastructure.

[10] B. Borlaug, S. Salisbury, M. Gerdes, M. Muratori, Levelized Cost of Charging Electric Vehicles in the United States, Joule 4 (2020) 1470–1485. https://www.sciencedirect.com/science/article/pii/S2542435120302312.

[11] E. Burton, M. Melaina, B. Bush, M. Muratori, J. Gonder, Evaluating Utility Cost Savings for Electric Vehicle Charging Infrastructure, National Renewable Energy Laboratory (NREL) Report (2020) 1–52. https://docs.nrel.gov/docs/fy20osti/75269.pdf.

[12] A.F.D.C. U.S. Department of Energy, Costs Associated With Non-Residential Electric Vehicle Supply Equipment, (2015). https://afdc.energy.gov/files/u/publication/evse_cost_report_2015.pdf.

[13] Transport & Environment, Oeko-Institut, Fraunhofer ISI, Truck Depot Charging – Final Report, (2022). https://www.transportenvironment.org/uploads/files/TE_truck-depot-charging_final-report.pdf.

[14] E. Cording, J. Thakur, FleetRL: Realistic reinforcement learning environments for commercial vehicle fleets, Softwarex 26 (2024) 101671–101671. https://www.sciencedirect.com/science/article/pii/S2352711024000426.

[15] E. Csanyi, What is the price of a power transformer?, (2022). https://electrical-engineering-portal.com/price-of-a-transformer.

[16] IEEE, IEEE Recommended Practice for Grounding of Industrial and Commercial Power Systems (IEEE Std 142-2007), (2007). https://hibp.ecse.rpi.edu/~connor/education/Fields/IEEEStd142_2007.pdf.

[17] S.o. Expert Interviews, Charging Infrastructure for Battery Electric Trucks: Synthesis of Expert Interviews, (2024).

[18] P. Plötz, D. Speth, Truck Stop Locations in Europe: Final Report, (2021). https://publica.fraunhofer.de/entities/publication/e9695859-88a6-4c5f-9da0-64814a2383bf.

[19] Open Charge Map project, Open Charge Map: Open Source Electric Vehicle Charging Stations, (n.d.). https://openchargemap.org/site.

[20] CharIN e.V., Megawatt Charging System (MCS), (2024). https://www.charin.global/technology/mcs/.

[21] HoLa Innovation Cluster, Megawatt Charging Networks (HoLa project), (2021). https://hochleistungsladen-lkw.de/hola-en/results/megawatt_charging_networks.php.
