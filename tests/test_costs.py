"""Regression tests for the cost engine (Round 5 bug fixes, Oct 2026)."""
import math
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.calls import case_definition, hard_requirement, compute_all_costs
from utils.cost import (transformer_cost_function,
                        cables_rectifier_to_chargers_cost_function)

DEFAULTS = {
    "Number of chargers": 4,
    "Power of chargers [kW]": 100,
    "Low Voltage level [V]": 480,
    "Grid Connection capacity [kVA]": 500,
    "Distance between the rectifier and the chargers [meters]": 100,
    "Load Power Factor": 0.9,
    "Maximum power for Low Voltage Connections in your area [kVA]": 200,
    "Available Capacity of the closest MV/LV transformer [kVA]": 1000,
    "Distance between your premises and the closest MV/LV transformer [meters]": 500,
    "Medium Voltage level [kV]": 10,
    "Transformer size safety margin for your new transformer [%]": 20,
    "Distance between your premises and the closest Medium Voltage Access point [meters]": 500,
    "Land to prepare for hosting the parking lot [m^2]": 0,
}


def _inputs(**over):
    d = dict(DEFAULTS)
    d.update(over)
    return d


# C1 -- sensitivity sweep on number of chargers used to hit None above 10 MVA
def test_sweep_number_of_chargers_never_returns_none():
    for trafo in (True, False):
        for n in range(1, 101):
            inp = _inputs(**{"Number of chargers": n})
            case = case_definition(inp, trafo)
            costs = compute_all_costs(inp, case, "Asphalt", "Low Slope / Light Vegetation")
            assert all(v is not None for v in costs.values()), (n, trafo, costs)


def test_transformer_above_catalogue_is_split_into_units():
    # 12,000 kVA uncovered -> two 6,000 kVA units, each priced at the 6,300 bracket
    price = transformer_cost_function(130, 100, 1000, 1.0, 0, 3)
    assert price == 2 * 64090


# C2 -- 1 x 350 kW at 200 V used to loop forever
def test_high_current_cable_sizing_terminates():
    cost = cables_rectifier_to_chargers_cost_function(1, 350, 200, 100)
    assert cost > 0 and math.isfinite(cost)


# C3 -- GUI (hard_requirement) and engine (case_definition) must agree
def test_type2_when_nearby_transformer_covers_uncovered_load():
    inp = _inputs(**{"Number of chargers": 3, "Power of chargers [kW]": 100,
                     "Load Power Factor": 1.0,
                     "Grid Connection capacity [kVA]": 200,
                     "Available Capacity of the closest MV/LV transformer [kVA]": 100})
    assert case_definition(inp, True) == 2
    assert hard_requirement(3, 100, 200, 1.0, True, 200, 100) is False
    costs = compute_all_costs(inp, 2, "Asphalt", "Low Slope / Light Vegetation")
    assert costs["transformer_cost"] == 0
    assert costs["cables_MV_distribution_to_site_cost"] == 0


def test_type3_when_nearby_transformer_too_small():
    inp = _inputs(**{"Number of chargers": 3, "Power of chargers [kW]": 100,
                     "Load Power Factor": 1.0,
                     "Grid Connection capacity [kVA]": 200,
                     "Available Capacity of the closest MV/LV transformer [kVA]": 50})
    assert case_definition(inp, True) == 3
    assert hard_requirement(3, 100, 200, 1.0, True, 200, 50) is True


def test_gui_and_engine_agree_on_mv_requirement_over_grid():
    for n in range(1, 40):
        for grid in (0, 100, 200, 500, 1000):
            for near in (0, 100, 200, 500):
                for trafo in (True, False):
                    inp = _inputs(**{"Number of chargers": n,
                                     "Grid Connection capacity [kVA]": grid,
                                     "Available Capacity of the closest MV/LV transformer [kVA]": near})
                    case = case_definition(inp, trafo)
                    mv = hard_requirement(n, 100, grid, 0.9, trafo, 200, near)
                    assert (case >= 3) == mv, (n, grid, near, trafo, case, mv)


# C4 -- safety margin must scale the transformer size
def test_safety_margin_changes_transformer_size():
    # 4 x 100 kW, grid 200 kVA, pf 1 -> 200 kVA uncovered
    p0 = transformer_cost_function(4, 100, 200, 1.0, 0, 3)     # 200 kVA -> 225 bracket
    p50 = transformer_cost_function(4, 100, 200, 1.0, 50, 3)   # 300 kVA -> 300 bracket
    assert p0 == 8679 and p50 == 10315
    assert transformer_cost_function(4, 100, 200, 1.0, 20, 3) == 9497   # 240 -> 250

