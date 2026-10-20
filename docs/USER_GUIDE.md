# CHARGE-IT user guide

CHARGE-IT estimates the investment cost of an overnight charging station for battery-electric heavy-duty vehicles, from the grid connection point to the charging plug. This page documents the inputs, the project type logic, the analysis functions, the output files, and how to change the price data. The full derivation of every cost function is in the thesis: [Techno-Economic Evaluation of Overnight Charging Infrastructure for Heavy-Duty Vehicles in Europe, KTH 2025](https://kth.diva-portal.org/smash/record.jsf?pid=diva2%3A2007635).

## Running the app

```bash
git clone https://github.com/davide-ferraro/ev-charging-cost-estimator.git
cd ev-charging-cost-estimator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

A hosted copy runs at https://ev-charging-cost-estimator.streamlit.app.

To run the regression tests:

```bash
python -m pytest tests -q
```

## Inputs

Three categorical inputs:

| Input | Values | Used for |
|---|---|---|
| Transformer already present on the premises | Yes / No | Project type (Types 3 and 4 differ only here) |
| Pavement material | Asphalt / Concrete | Site preparation cost |
| Land type | Low slope and light vegetation / High slope and heavy vegetation | Site preparation cost |

Fourteen numerical inputs:

| Input | Unit | Range | Default | Notes |
|---|---|---|---|---|
| Number of chargers (n) | – | 1–100 | 4 | |
| Power of chargers (P) | kW | 10–350 | 100 | Per plug |
| Low voltage level | V | 200–1000 | 480 | LV side of the station |
| Grid connection capacity (G) | kVA | 0–5000 | 500 | Without a transformer: the maximum apparent power allowed. With a transformer: its spare capacity. |
| Distance between the rectifier and the chargers | m | 0–1000 | 100 | DC cable run |
| Load power factor (pf) | – | 0.70–1.00 | 0.90 | |
| Simultaneity factor (f) | – | 0.1–1.0 | 1.0 | Share of the installed charger power drawn from the grid at the same time. 1.0 means every plug at full power (unmanaged charging). Lower values represent managed charging that caps the site peak. |
| Maximum power for LV connections in your area | kVA | 10–1000 | 200 | Local DSO rule; 200 kVA is a common European value |
| Available capacity of the closest MV/LV transformer | kVA | 0–5000 | 1000 | Only used when an LV upgrade is possible |
| Distance to the closest MV/LV transformer | m | 0–5000 | 500 | LV distribution cable run (Type 2) |
| Medium voltage level | kV | 10–45 | 10 | |
| Transformer size safety margin | % | 0–100 | 20 | Oversizing of a new transformer (Types 3 and 4) |
| Distance to the closest MV access point | m | 0–5000 | 500 | MV cable run (Types 3 and 4) |
| Land to prepare for the parking lot | m² | 0–100000 | 0 | |

Fields that do not apply to the current configuration are greyed out automatically.

## Project type

The planned apparent load is

    S = f · n · P / pf   [kVA]

and the classification follows this order:

1. If the grid connection capacity G covers S, the project is **Type 1**: only the chargers and their LV-side equipment are needed.
2. Otherwise the uncovered load is computed. With a transformer on site it is S − G, without one it is S.
3. If the uncovered load is within the local LV connection limit **and** the closest MV/LV transformer has at least that much spare capacity, an LV upgrade is enough: **Type 2**.
4. If not, a new MV connection and a new transformer are needed. With a transformer already on site this is **Type 3**, otherwise **Type 4**.

The project type switches cost items on and off. Items that do not apply return zero.

## What the simultaneity factor changes

The factor scales the coincident load used for the project type and for the grid-side items: LV distribution cables, MV cables, transformer, switchgear, and the connection costs derived from the cables. Items at the plug keep the full installed power: chargers, rectifier, LV cabinet, DC cables, planning and installation. With f = 1.0 the results are identical to version 1.0.0.

## Cost items

Fifteen items in three groups.

| Group | Item | Sized on |
|---|---|---|
| Substation (Types 3 and 4) | MVAC cables, transformer, MV switchgear, surge arresters, grounding resistors | Uncovered load, MV voltage, cable distance |
| LV equipment | LVAC distribution cables (Type 2), LV cabinet, rectifier, DC cables, chargers | Installed power, LV voltage, distances |
| Other | Planning, installation, MV connection cost, LV connection cost, site preparation | Charger count and power, cable cost, land area |

Formulas and price tables are in `utils/cost.py`; the orchestration (project type, which function runs when) is in `utils/calls.py`.

## Analysis functions

- **Cost Breakdown**: itemized table and chart for the configuration entered.
- **Single-Variable Sensitivity**: one or more inputs are swept across a user-defined range, everything else fixed. Every point re-runs the full pipeline, so the project type can change along the sweep.
- **Two-Parameter Sensitivity**: two inputs are swept together; results are shown as a scatter plot coloured by the second input, with the full breakdown on hover.

## Exports

- Excel (`.xlsx`) for every result table.
- PDF report with the inputs, the tables and the charts.

## Updating the price data

All prices are 2024 euros and live in `utils/cost.py` as plain Python literals:

- Lookup tables are dictionaries keyed by size, for example `trafo_price_2024` in `transformer_cost_function` (kVA → €) and the charger price table in `charger_cost_function` (kW → €). Add or replace rows; the lookup picks the smallest catalogue size that is at least the required size.
- Linear and exponential fits are the numeric coefficients in `LV_cables_cost`, `MV_cable_cost`, `lv_cabinet_cost_function`, `charger_planning_cost_function` and `charger_installation_cost_function`.
- Site preparation rates per square metre are in `site_preparation_cost_function`.

Nothing else needs to change: `calls.py` and `app.py` only pass quantities through. After editing, run the tests.

## Version history

- **1.1.0** (October 2026): simultaneity factor input; fixes to transformer safety margin, cable sizing loop, Type 2 classification consistency and catalogue overflow in sensitivity sweeps; regression tests.
- **1.0.0** (August 2026): first release, as submitted to SoftwareX.
