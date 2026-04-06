from .cost import *


def medium_requirement(number_of_chargers,power_of_chargers,current_grid_connection_capacity,load_power_factor,transformer_presence,treshold):
    if (number_of_chargers*power_of_chargers/load_power_factor)> current_grid_connection_capacity:
        if transformer_presence==True:
            uncovered_load=(number_of_chargers*power_of_chargers/load_power_factor)-current_grid_connection_capacity
        else:
            uncovered_load=number_of_chargers*power_of_chargers/load_power_factor

        #print(uncovered_load)

        if uncovered_load<=treshold:
            return True
        else:
            return False
    else:
        return False
    
def hard_requirement(number_of_chargers,power_of_chargers,current_grid_connection_capacity,load_power_factor,transformer_presence,treshold,close_trafo_power):
    if (number_of_chargers*power_of_chargers/load_power_factor)> current_grid_connection_capacity:
        if transformer_presence==True:
            uncovered_load=(number_of_chargers*power_of_chargers/load_power_factor)-current_grid_connection_capacity
        else:
            uncovered_load=number_of_chargers*power_of_chargers/load_power_factor

        if uncovered_load <= treshold:
            if close_trafo_power>=uncovered_load:
                return False
            else:
                return True
        else:
            return True
    else:
        return False

def case_definition(input,trafo_presence):
    chargers_load= input["Number of chargers"]*input["Power of chargers [kW]"]/input["Load Power Factor"]
    connection=input["Grid Connection capacity [kVA]"]
    treshold=input["Maximum power for Low Voltage Connections in your area [kVA]"]
    grid_capacity=input["Available Capacity of the closest MV/LV transformer [kVA]"]

    if connection >= chargers_load:
        return 1
    else:
        if trafo_presence==1:
            spare_load = chargers_load-connection
        else:
            spare_load=chargers_load
        
        if spare_load<=treshold and grid_capacity>=treshold:
            return 2
        if trafo_presence==1:
            return 3
        else:
            return 4

def compute_all_costs(input, case, select_material, select_land_type):
    chargers_cost = charger_cost_function(
        input["Number of chargers"],
        input["Power of chargers [kW]"])
    print(1)
    rectifier_cost = rectifier_cost_function(
        input["Number of chargers"],
        input["Power of chargers [kW]"])
    print(2)
    low_voltage_cabinet_cost = lv_cabinet_cost_function(
        input["Number of chargers"],
        input["Power of chargers [kW]"],
        input["Low Voltage level [V]"])
    print(3)
    cables_rectifier_to_chargers_cost = cables_rectifier_to_chargers_cost_function(
        input["Number of chargers"],
        input["Power of chargers [kW]"],
        input["Low Voltage level [V]"],
        input["Distance between the rectifier and the chargers [meters]"])
    print(4)
    cables_LV_distribution_to_site_cost = cables_LV_distribution_to_site_cost_function(
        input["Number of chargers"],
        input["Power of chargers [kW]"],
        input["Low Voltage level [V]"],
        input["Distance between your premises and the closest MV/LV transformer [meters]"],
        input["Grid Connection capacity [kVA]"],
        input["Load Power Factor"],
        case)
    print(5)
    cables_MV_distribution_to_site_cost = cables_MV_distribution_to_site_cost_function(
        input["Number of chargers"],
        input["Power of chargers [kW]"],
        input["Medium Voltage level [kV]"],
        input["Distance between your premises and the closest Medium Voltage Access point [meters]"],
        input["Grid Connection capacity [kVA]"],
        input["Load Power Factor"],
        case)
    print(6)
    surge_arresters_cost = surge_arresters_cost_function(
        input["Medium Voltage level [kV]"],
        case)
    print(7)
    grounding_resistor_cost = grounding_resistors_cost_function(
        input["Medium Voltage level [kV]"],
        case)
    print(8)

    transformer_cost = transformer_cost_function(
        input["Number of chargers"],
        input["Power of chargers [kW]"],
        input["Grid Connection capacity [kVA]"],
        input["Load Power Factor"],
        input["Transformer size safety margin for your new transformer [%]"],
        case)
    print(9)
    switchgear_cost = switchgear_cost_function(
        input["Number of chargers"],
        input["Power of chargers [kW]"],
        input["Grid Connection capacity [kVA]"],
        input["Load Power Factor"],
        input["Medium Voltage level [kV]"],
        case)
    print(10)
    MV_cable_installation_cost=MV_cable_installation_cost_function(
        cables_MV_distribution_to_site_cost,
        input["Distance between your premises and the closest Medium Voltage Access point [meters]"],
        case
    )
    LV_cable_installation_cost=LV_cable_installation_cost_function(
        cables_LV_distribution_to_site_cost,
        case)

    planning_cost=charger_planning_cost_function(
        input["Number of chargers"],
        input["Power of chargers [kW]"])
    
    installation_cost = charger_installation_cost_function(
        input["Number of chargers"],
        input["Power of chargers [kW]"],
        case)
    print(11)
    site_preparation_cost = site_preparation_cost_function(
        input["Land to prepare for hosting the parking lot [m^2]"],
        select_material,
        select_land_type)
    print(12)
    return {
        "chargers_cost": chargers_cost,
        "rectifier_cost": rectifier_cost,
        "low_voltage_cabinet_cost": low_voltage_cabinet_cost,
        "cables_rectifier_to_chargers_cost": cables_rectifier_to_chargers_cost,
        "cables_LV_distribution_to_site_cost": cables_LV_distribution_to_site_cost,
        "cables_MV_distribution_to_site_cost": cables_MV_distribution_to_site_cost,
        "surge_arresters_cost": surge_arresters_cost,
        "grounding_resistor_cost": grounding_resistor_cost,
        "transformer_cost": transformer_cost,
        "switchgear_cost": switchgear_cost,
        "planning_cost":planning_cost,
        "installation_cost": installation_cost,
        "MV_connection_cost":MV_cable_installation_cost,
        "LV_connection_cost": LV_cable_installation_cost,
        "site_preparation_cost": site_preparation_cost
    }

def cost_breakdown_calculation(input, trafo_presence, select_material, select_land_type):
    case = case_definition(input, trafo_presence)
    #print(case)

    costs = compute_all_costs(input, case, select_material, select_land_type)

    table = {
        "Substation Equipment": "",
        "Cables MVAC (Distribution-Site)": f"€{round(costs['cables_MV_distribution_to_site_cost'], 0):,.2f}",
        "Transformer": f"€{round(costs['transformer_cost'], 0):,.2f}",
        "Switchgear": f"€{round(costs['switchgear_cost'], 0):,.2f}",
        "Surge Arresters": f"€{round(costs['surge_arresters_cost'], 0):,.2f}",
        "Grounding Resistors": f"€{round(costs['grounding_resistor_cost'], 0):,.2f}",
        "Low Voltage Equipment": "",
        "Cables LVAC (Distribution-Site)": f"€{round(costs['cables_LV_distribution_to_site_cost'], 0):,.2f}",
        "LV cabinet": f"€{round(costs['low_voltage_cabinet_cost'], 0):,.2f}",
        "Rectifier": f"€{round(costs['rectifier_cost'], 0):,.2f}",
        "Cables LVDC (Rectifier-Chargers)": f"€{round(costs['cables_rectifier_to_chargers_cost'], 0):,.2f}",
        "Chargers": f"€{round(costs['chargers_cost'], 0):,.2f}",
        "Other costs": "",
        "Planning":f"€{round(costs['planning_cost'], 0):,.2f}",
        "Installation": f"€{round(costs['installation_cost'], 0):,.2f}",
        "MV connection cost":f"€{round(costs['MV_connection_cost'], 0):,.2f}",
        "LV connection cost": f"€{round(costs['LV_connection_cost'], 0):,.2f}",
        "Site preparation": f"€{round(costs['site_preparation_cost'], 0):,.2f}",
        "Total": f"€{round(costs['cables_MV_distribution_to_site_cost']+costs['transformer_cost']+costs['switchgear_cost']+costs['surge_arresters_cost']+costs['grounding_resistor_cost']+costs['cables_LV_distribution_to_site_cost']+costs['low_voltage_cabinet_cost']+costs['rectifier_cost']+costs['cables_rectifier_to_chargers_cost']+costs['chargers_cost']+costs['planning_cost']+costs['installation_cost']+costs['MV_connection_cost']+costs['site_preparation_cost']+costs['LV_connection_cost'] , 0):,.2f}"
    }

    return {k: v for k, v in table.items()}

def cost_breakdown_sensitivity_calculation(input, trafo_presence, select_material, select_land_type, sensitivity_ranges):
    
    # Step 1: Identify sensitivity parameters
    sensitivity_labels = list(sensitivity_ranges.keys())
    #print("Sensitivity analysis on:", sensitivity_labels)

    results = {}

    for label in sensitivity_labels:
        min_val, max_val = sensitivity_ranges[label]
        step = sensitivity_step(min_val, max_val,label)

        results[label] = {}

        for value in frange(min_val, max_val, step):
            modified_input = input.copy()
            modified_input[label] = value
            case = case_definition(modified_input, trafo_presence)
            costs = compute_all_costs(modified_input, case, select_material, select_land_type)
            results[label][value] = {
                "Cables MVAC (Distribution-Site)": f"€{round(costs['cables_MV_distribution_to_site_cost'], 0):,.2f}",
                "Transformer": f"€{costs['transformer_cost']}",
                "Switchgear": f"€{round(costs['switchgear_cost'], 0):,.2f}",
                "Surge Arresters": f"€{round(costs['surge_arresters_cost'], 0):,.2f}",
                "Grounding Resistors": f"€{round(costs['grounding_resistor_cost'], 0):,.2f}",
                "Cables LVAC (Distribution-Site)": f"€{round(costs['cables_LV_distribution_to_site_cost'], 0):,.2f}",
                "LV cabinet": f"€{round(costs['low_voltage_cabinet_cost'], 0):,.2f}",
                "Rectifier": f"€{round(costs['rectifier_cost'], 0):,.2f}",
                "Cables LVDC (Rectifier-Chargers)": f"€{round(costs['cables_rectifier_to_chargers_cost'], 0):,.2f}",
                "Chargers": f"€{round(costs['chargers_cost'], 0):,.2f}",
                "Planning":f"€{round(costs['planning_cost'], 0):,.2f}",
                "Installation": f"€{round(costs['installation_cost'], 0):,.2f}",
                "MV connection cost":f"€{round(costs['MV_connection_cost'], 0):,.2f}",
                "LV connection cost": f"€{round(costs['LV_connection_cost'], 0):,.2f}",
                "Site preparation": f"€{round(costs['site_preparation_cost'], 0):,.2f}",
                "Total": f"€{round(costs['cables_MV_distribution_to_site_cost']+costs['transformer_cost']+costs['switchgear_cost']+costs['surge_arresters_cost']+costs['grounding_resistor_cost']+costs['cables_LV_distribution_to_site_cost']+costs['low_voltage_cabinet_cost']+costs['rectifier_cost']+costs['cables_rectifier_to_chargers_cost']+costs['chargers_cost']+costs['installation_cost']+costs['site_preparation_cost'] , 0):,.2f}"
            }

    return results

def frange(start, stop, step):
    while start <= stop:
        yield round(start, 2)
        start += step

def sensitivity_step(min_val, max_val,label):

    custom_steps = {
        "Number of chargers": 1,
        "Power of chargers [kW]": 10,
        "Low Voltage level [V]": 20,
        "Grid Connection capacity [kVA]": 100,
        "Distance between the rectifier and the chargers [meters]": 50,
        "Load Power Factor": 0.02,
        "Maximum power for Low Voltage Connections in your area [kVA]": 100,
        "Available Capacity of the closest MV/LV transformer [kVA]": 100,
        "Distance between your premises and the closest MV/LV transformer [meters]": 100,
        "Medium Voltage level [kV]": 5,
        "Transformer size safety margin for your new transformer [%]": 1,
        "Distance between your premises and the closest Medium Voltage Access point [meters]": 100,
        "Land to prepare for hosting the parking lot [m^2]": 100
    }
    #range_span = max_val - min_val
    if label in custom_steps:
        print("CIAOOOO")
        return custom_steps[label]    
    else:
        print("NOOOOO")
        return 0

def cost_breakdown_double_sensitivity_calculation(input, trafo_presence, select_material, select_land_type, x_label, y_label):
    # Define custom min/max for each label
    range_dict = {
        "Number of chargers": (1, 40, 1),
        "Power of chargers [kW]": (10, 200, 5),
        "Low Voltage level [V]": (200, 480, 20),
        "Grid Connection capacity [kVA]": (50, 3000, 50),
        "Distance between the rectifier and the chargers [meters]": (0, 2000, 100),
        "Load Power Factor": (0.7, 1.0,0.05),
        "Maximum power for Low Voltage Connections in your area [kVA]": (0, 2000, 100),
        "Available Capacity of the closest MV/LV transformer [kVA]": (0, 2000, 100),
        "Distance between your premises and the closest MV/LV transformer [meters]": (0, 2000, 100),
        "Medium Voltage level [kV]": (10, 45, 5),
        "Transformer size safety margin for your new transformer [%]": (0, 50, 5),
        "Distance between your premises and the closest Medium Voltage Access point [meters]": (0, 3000 ,100),
        "Land to prepare for hosting the parking lot [m^2]": (0, 50000, 1000),
    }

    results = {}
    results[(x_label, y_label)] = {}

    x_min, x_max, x_step= range_dict[x_label]
    y_min, y_max, y_step = range_dict[y_label]

    print(x_min)
    print(x_max)
    
    print(y_min)
    print(y_max)
    
    """ x_step = sensitivity_step(x_label, x_min, x_max)
    y_step = sensitivity_step(y_label, y_min, y_max)"""

    print(x_step)
    print(y_step)

    for x in frange(x_min, x_max, x_step):
        for y in frange(y_min, y_max, y_step):
            print(f'{x}-{y}')
            modified_input = input.copy()
            modified_input[x_label] = x
            modified_input[y_label] = y

            case = case_definition(modified_input, trafo_presence)
            costs = compute_all_costs(modified_input, case, select_material, select_land_type)
            print(round(costs['chargers_cost'], 0))
            results[(x_label, y_label)][(x, y)] = {
                "Cables MVAC (Distribution-Site)": f"€{round(costs['cables_MV_distribution_to_site_cost'], 0):,.2f}",
                "Transformer": f"€{round(costs['transformer_cost'], 0):,.2f}",
                "Switchgear": f"€{round(costs['switchgear_cost'], 0):,.2f}",
                "Surge Arresters": f"€{round(costs['surge_arresters_cost'], 0):,.2f}",
                "Grounding Resistors": f"€{round(costs['grounding_resistor_cost'], 0):,.2f}",
                "Cables LVAC (Distribution-Site)": f"€{round(costs['cables_LV_distribution_to_site_cost'], 0):,.2f}",
                "LV cabinet": f"€{round(costs['low_voltage_cabinet_cost'], 0):,.2f}",
                "Rectifier": f"€{round(costs['rectifier_cost'], 0):,.2f}",
                "Cables LVDC (Rectifier-Chargers)": f"€{round(costs['cables_rectifier_to_chargers_cost'], 0):,.2f}",
                "Chargers": f"€{round(costs['chargers_cost'], 0):,.2f}",
                "Planning" : f"€{round(costs['planning_cost'], 0):,.2f}",
                "Installation": f"€{round(costs['installation_cost'], 0):,.2f}",
                "MV connection cost":f"€{round(costs['MV_connection_cost'], 0):,.2f}",
                "LV connection cost": f"€{round(costs['LV_connection_cost'], 0):,.2f}",
                "Site preparation": f"€{round(costs['site_preparation_cost'], 0):,.2f}",
            }
    return results

