import math

# UTILITIES_________________________________________________________________________________________________________________________________________--
def LV_cables_cost(current):
    return 0.276*current

def MV_cable_cost(current):
    #return 0.6917*current-42.043
    return 53.976*math.exp(0.0034*current)

def MV_cable_cost_to_current(cost):
    if  cost> 53.9756:
        return (1 / 0.0034) * math.log(cost / 53.976)
    else:
        return 0

def get_upper_price(variable, table):
        for key in sorted(table.keys()):
            if key >= variable:
                return table[key]
        return None  # If voltage is higher than max available

# /UTILITIES_________________________________________________________________________________________________________________________________________--

# LV COST FUNCTIONS_________________________________________________________________________________________________________________________________________--
def charger_cost_function(quantity, power):

    """charger_price_from_table = {
    20: 1958,
    30: 2774,
    40: 3511,
    50: 4150,
    60: 4680,
    70: 5110,
    80: 5440,
    90: 5648,
    100: 5750,
    110: 5748,
    120: 5640,
    130: 6002,
    140: 6347,
    150: 6675,
    160: 6987,
    170: 7282,
    180: 7560,
    190: 7727,
    200: 7867,
    210: 7980,
    220: 8067,
    230: 8127,
    240: 8160,
    250: 8375,
    260: 8580,
    270: 8775,
    280: 8960,
    290: 9135,
    300: 9300,
    310: 9455,
    320: 9600,
    330: 9653,
    340: 9690,
    350: 9713,
    }"""

    charger_price_from_table = {
    20: 4679,
    30: 7019,
    40: 9437,
    50: 7291,
    60: 8821,
    70: 10374,
    80: 11952,
    90: 13554,
    100: 15179,
    110: 16829,
    120: 18502,
    130: 20199,
    140: 21920,
    150: 23665,
    160: 24817,
    170: 25915,
    180: 26960,
    190: 27951,
    200: 28890,
    210: 29775,
    220: 30607,
    230: 31385,
    240: 32111,
    250: 32783,
    260: 33402,
    270: 33967,
    280: 34479,
    290: 34938,
    300: 35344,
    310: 35696,
    320: 35996,
    330: 36241,
    340: 36434,
    350: 36573,
    }

    return quantity*get_upper_price(power,charger_price_from_table)

def rectifier_cost_function(quantity, power):

    if power<=40:
        return 0
    else:
        MAX_RECTIFIER_POWER= 200
        SINGLE_RECTIFIER_PRICE=222*MAX_RECTIFIER_POWER

        number_of_rectifiers = math.ceil((quantity*power) / MAX_RECTIFIER_POWER)
        return number_of_rectifiers*SINGLE_RECTIFIER_PRICE

def lv_cabinet_cost_function(quantity, power, low_voltage):
    MAX_SWITCHBOARD_CURRENT = 4000
    MIN_SWITCHBOARD_CURRENT = 200
    MINIMUM_COST = 10.319 * MIN_SWITCHBOARD_CURRENT - 900.26
    MAXIMUM_COST = 10.319 * MAX_SWITCHBOARD_CURRENT - 900.26

    current = quantity * power * 1000 / (math.sqrt(3) * low_voltage)
    rest_of_current = current
    cost = 0

    while rest_of_current > 0:
        if rest_of_current <= MIN_SWITCHBOARD_CURRENT:
            cost += MINIMUM_COST
            rest_of_current = 0
        elif rest_of_current <= MAX_SWITCHBOARD_CURRENT:
            cost += 10.319 * rest_of_current - 900.26
            rest_of_current = 0
        else:
            cost += MAXIMUM_COST
            rest_of_current -= MAX_SWITCHBOARD_CURRENT  # ✅ Fixed

    return cost

def cables_rectifier_to_chargers_cost_function(quantity,power,low_voltage,distance):

    if power > 20:
        voltage_AC_to_DC=1.35
    else:
        voltage_AC_to_DC=1
    
    
    K1_20C=1
    K2_50CM_6cables=0.8

    MAX_CURRENT= 430
    MIN_CURRENT= 40
    MINIMUM_COST=LV_cables_cost(MIN_CURRENT)
    MAXIMUM_COST=LV_cables_cost(MAX_CURRENT)

    current=(quantity*power)/(voltage_AC_to_DC*low_voltage/1000)
    single_cable_current=(current/quantity)/(K1_20C*K2_50CM_6cables)
    single_cable_nominal_current=round(single_cable_current/10,0)*10

    rest_of_current=single_cable_nominal_current
    cost=0
    while rest_of_current > 0:
        if rest_of_current <= MIN_CURRENT:
            cost = cost + LV_cables_cost(MIN_CURRENT)
            rest_of_current=0
        elif rest_of_current <= MAX_CURRENT:
            cost = cost + LV_cables_cost(rest_of_current)
            rest_of_current=0
        elif rest_of_current > MAX_CURRENT:
            cost= cost + LV_cables_cost(MAX_CURRENT)
            rest_of_current=single_cable_nominal_current-MAX_CURRENT
    
    cost_total=cost*quantity*distance

    return cost_total

def cables_LV_distribution_to_site_cost_function(quantity, power,low_voltage,distance,grid_connection,load_factor,case):
    
    MAX_CURRENT= 430
    MIN_CURRENT= 40
    K1_20C=1

    current= ((quantity*power/load_factor)-grid_connection)/(math.sqrt(3)*low_voltage/1000)
    
    k2_50cm = {
        1: 1.00,
        2: 0.86,
        3: 0.76,
        4: 0.72,
        5: 0.66,
        6: 0.66,
        7: 0.66,
        8: 0.61,
        9: 0.61,
    }

    cost_total=0

    if case==2:
        N_cables= math.ceil(current/MAX_CURRENT) #math.ceil is round up
        if N_cables>9:
            N_cables_for_K2=9
        else:
            N_cables_for_K2=N_cables
        K2=k2_50cm[N_cables_for_K2]

        single_cable_current=(current/N_cables)/(K2*K1_20C)
        single_cable_nominal_current=round(single_cable_current/10,0)*10

        rest_of_current=single_cable_nominal_current
        cost=0
        while rest_of_current > 0:
            #print(rest_of_current)
            if rest_of_current <= MIN_CURRENT:
                cost = cost + LV_cables_cost(MIN_CURRENT)
                rest_of_current=0
            elif rest_of_current <= MAX_CURRENT:
                cost = cost + LV_cables_cost(rest_of_current)
                rest_of_current=0
            elif rest_of_current > MAX_CURRENT:
                cost= cost +LV_cables_cost(MAX_CURRENT)
                rest_of_current=single_cable_nominal_current-MAX_CURRENT
        
        cost_total=cost*N_cables*distance
    
    return cost_total

# /LV COST FUNCTIONS_________________________________________________________________________________________________________________________________________--

# MV COST FUNCTIONS_________________________________________________________________________________________________________________________________________--
def cables_MV_distribution_to_site_cost_function(quantity, power,medium_voltage,distance,grid_connection,load_factor,case):
    
    MAX_CURRENT = 590 
    MIN_CURRENT=10
    K1_20C=1

    if case==3:
        current= (quantity*power/load_factor-grid_connection)/(math.sqrt(3)*medium_voltage)
        #print(current)
    elif case==4:
        current= (quantity*power/load_factor)/(math.sqrt(3)*medium_voltage)
        #print(current)
    else:
        current=0

    k2_50cm = {
        1: 1.00,
        2: 0.86,
        3: 0.78,
        4: 0.74,
        5: 0.69,
        6: 0.69
    }

    cost_total=0

    if current > 0:
        N_cables= math.ceil(current/MAX_CURRENT) #math.ceil is round up
        if N_cables>6:
            N_cables_for_K2=6
        else:
            N_cables_for_K2=N_cables

        K2=k2_50cm[N_cables_for_K2]


        single_cable_current=(current/N_cables)/(K2*K1_20C)
        single_cable_nominal_current=round(single_cable_current/10,0)*10

        rest_of_current=single_cable_nominal_current
        cost=0
        while rest_of_current > 0:
            if rest_of_current <= MIN_CURRENT:
                cost = cost + MV_cable_cost(MIN_CURRENT)
                rest_of_current=0
            elif rest_of_current <= MAX_CURRENT:
                cost = cost + MV_cable_cost(rest_of_current)
                rest_of_current=0
            elif rest_of_current > MAX_CURRENT:
                cost= cost +MV_cable_cost(MAX_CURRENT)
                rest_of_current=single_cable_nominal_current-MAX_CURRENT
        
        cost_total=cost*distance
    
    return cost_total

def surge_arresters_cost_function(voltage,case):

    voltage_price_2024 = {
    10: 1168,
    12: 1168,
    14: 1266,
    16: 1363,
    18: 1460,
    20: 1558,
    22: 1655,
    24: 1753,
    26: 1850,
    28: 1947,
    30: 1947,
    32: 1947,
    34: 1947,
    36: 1947,
    38: 1986,
    40: 2025,
    42: 2064,
    44: 2103,
    46: 2142,
    48: 2181,
    50: 2220,
    52: 2259,
    54: 2298,
    56: 2337,
    58: 2337,
    60: 2337,
    62: 2337,
    64: 2337,
    66: 2337,
    68: 2337,
    70: 2337
}
    if case>2:
        price = get_upper_price(voltage, voltage_price_2024)
    else:
        price=0

    return price

def grounding_resistors_cost_function(voltage, case):

    voltage_price_2024 = {
        5: 5757,
        10: 7011,
        15: 8266,
        20: 9521,
        25: 10775,
        30: 12030,
        35: 13285,
        40: 14540,
        45: 15795
    }

    if case>2:
        price = get_upper_price(voltage, voltage_price_2024)
    else:
        price=0

    return price

def transformer_cost_function(quantity,power,grid_connection,load_factor,safety_margin,case):
    if case==3:
        trafo_power= ((quantity*power)/load_factor-grid_connection)*1+(safety_margin/100)
    elif case==4:
        trafo_power= ((quantity*power)/load_factor)*1+(safety_margin/100)
    
    trafo_price_2024 = {
        100: 5336,
        150: 6805,
        160: 7742,
        225: 8679,
        250: 9497,
        300: 10315,
        315: 11548,
        400: 12781,
        500: 14014,
        630: 15944,
        750: 17874,
        800: 19558,
        1000: 21242,
        1250: 24167,
        1500: 27092,
        1600: 29644,
        2000: 32196,
        2500: 36809,
        3000: 41064,
        3750: 46947,
        5000: 55792,
        6300: 64090,
        7500: 71158,
        10000: 84564,
    }

    if case>2:
        price = get_upper_price(trafo_power, trafo_price_2024)
    else:
        price=0

    return price

def switchgear_cost_function(quantity,power,grid_connection,load_factor,medium_voltage,case):

    if case>2:
        if case==3:
            current= (quantity*power/load_factor-grid_connection)/(math.sqrt(3)*medium_voltage)
        elif case==4:
            current= (quantity*power/load_factor)/(math.sqrt(3)*medium_voltage)
        
        MAX_VOLTAGE=52
        MIN_VOLTAGE=3

        MAX_CURRENT=160
        MIN_CURRENT=20

        if medium_voltage>MAX_VOLTAGE:
            medium_voltage=MAX_VOLTAGE
        if medium_voltage<MIN_VOLTAGE:
            medium_voltage=MIN_VOLTAGE

        if current > MAX_CURRENT:
            current = MAX_CURRENT
        if current < MIN_CURRENT:
            current = MIN_CURRENT
        
        wheight_voltage=0.2
        wheight_current=0.5
        wheight_quality=0.1
        wheight_brand=0.1
        wheight_location=0.1

        base_price=44283
        max_price=177131
        max_increment=max_price-base_price

        increment_voltage= max_increment * wheight_voltage
        increment_current= max_increment * wheight_current
        increment_quality= max_increment * wheight_quality
        increment_brand= max_increment * wheight_brand
        increment_location= max_increment * wheight_location

        print(current)
        quality_voltage=(medium_voltage-MIN_VOLTAGE)/(MAX_VOLTAGE-MIN_VOLTAGE)
        quality_current=(current- MIN_CURRENT)/(MAX_CURRENT-MIN_CURRENT)
        quality_quality=1
        quality_brand=1
        quality_location=1

        cost_voltage=increment_voltage*quality_voltage
        cost_current=increment_current*quality_current
        cost_quality=increment_quality*quality_quality
        cost_brand=increment_brand*quality_brand
        cost_location=increment_location*quality_location

        return base_price+cost_voltage+cost_current+cost_quality+cost_brand+cost_location
    else:
        return 0

# /MV COST FUNCTIONS_________________________________________________________________________________________________________________________________________--

# LABOR COST FUNCTIONS_________________________________________________________________________________________________________________________________________--
def charger_planning_cost_function(quantity,power): 
    return quantity*(25.064*power+275.07)

def charger_installation_cost_function(quantity,power,case):
    cost_substation=30000
    cost_chargers = quantity*(155.83*power+5822.5)

    if case>2:
        return cost_chargers+cost_substation
    else:
        return cost_chargers

def site_preparation_cost_function(area,material,land_type):

    if material == "No" or land_type=="No":
        return 0
    if material=="Asphalt" and land_type=="Low Slope / Light Vegetation":
        return area*45.2
    if material=="Asphalt" and land_type=="High Slope / Heavy Vegetation":
        return area*150.6
    if material=="Concrete" and land_type=="Low Slope / Light Vegetation":
        return area*55.2
    if material=="Concrete" and land_type=="High Slope / Heavy Vegetation":
        return area*150.6

def MV_cable_installation_cost_function(cable_cost,distance,case):
    if case>2 and distance >0:
        cable_cost_per_meter= cable_cost/distance
        current_from_cost_per_meter=MV_cable_cost_to_current(cable_cost_per_meter)

        if current_from_cost_per_meter==0:
            return 0
        else:
            total_installation_cost_per_meter=current_from_cost_per_meter*0.3623+246.38
            installation_cost_per_meter=total_installation_cost_per_meter-cable_cost_per_meter
            return installation_cost_per_meter*distance
    else:
        return 0

def LV_cable_installation_cost_function(cable_cost,case):
    if case==2:
        return cable_cost
    else:
        return 0
    
# /LABOR COST FUNCTIONS_________________________________________________________________________________________________________________________________________--