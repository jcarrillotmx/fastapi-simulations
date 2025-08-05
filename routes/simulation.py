from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from collections import OrderedDict
from fastapi.middleware.cors import CORSMiddleware

import random
import datetime

simulation = APIRouter()


min_value = 0.0
max_value = 120.0


@simulation.get("/data")
def get_channels():
    channels = []
    channel_names = ["Canal 1", "Canal 2", "Canal 3"]

    for name in channel_names:
        min_val = round(random.uniform(50, 100), 2)
        max_val = round(min_val + random.uniform(10, 100), 2)
        value = round(random.uniform(min_val, max_val), 2)
        channel = {
            "name": name,
            "value": value,
            "min_value": min_val,
            "max_value": max_val,
            "unity": "g/cm³"
        }
        channels.append(channel)

    return channels


@simulation.get("/channels")
def get_live_data():
    return {
        "group": "g1",
        "data": {
            "status_word": round(random.uniform(200, 250), 2),
            "status_word_2": round(random.uniform(200, 250), 2),
            "consumo_actual": round(random.uniform(200, 250), 2),
            "combustible_diferencial_total_usado": round(random.uniform(200, 250), 2),
            "combustible_total_usado_suministrado": round(random.uniform(200, 250), 2),
            "horometro_dfm_suministro": round(random.uniform(200, 250), 2),
            "combustible_total_usado_retorno": round(random.uniform(200, 250), 2),
            "horometro_dfm_retorno": round(random.uniform(200, 250), 2),
            "fuel_temp_suministro": round(random.uniform(200, 250), 2),
            "fuel_temp_retorno": round(random.uniform(200, 250), 2),
            "voltaje": round(random.uniform(200, 250), 2),
            "corriente": round(random.uniform(10, 50), 2),
            "frecuencia": round(random.uniform(49, 61), 2),
            "potencia_aparente": round(random.uniform(500, 2000), 2),
            "potencia_activa": round(random.uniform(400, 1800), 2),
            "potencia_reactiva": round(random.uniform(300, 1500), 2),
            "factor_de_potencia": round(random.uniform(0.5, 1.0), 2),
        }
    }


# Información fija (name y unit)
NAMES_UNITS = {
    1: ("Status Word", "unidad"),
    2: ("Status Word 2", "unidad"),
    3: ("Engine Fuel Rate. Differencial", "l"),
    4: ("Total Fuel Used Differencial (Clearabe)", "l"),
    5: ("Flowmeter Hours Of Operation (Clearable)", "m/s"),
    6: ("Flowmeter Hours Of Operation Suministro A-Gen (Clearable)", "unidad"),
    7: ("Total Fuel Used  Retorno A-Gen (Clearabe)", "unidad"),
    8: ("Flowmeter Hours Of Operation Retorno A-Gen (Clearable)", "unidad"),
    9: ("Engine temperature Suministro", "unidad"),
    10: ("Engine temperature Retorno", "°C"),
    11: ("Voltaje", "l"),
    12: ("Corriente", "unidad"),
    13: ("Frecuencia ", "unidad"),
    14: ("Potencia Aparente ", "unidad"),
    15: ("Potencia Activa", "unidad"),
    16: ("Potencia Reactiva", "unidad"),
    17: ("Factor Potencia ", "unidad"),
    18: ("Cosumo Actual", "unidad"),
    19: ("Combustible Diferencial Total Usado", "unidad"),
}


VALID_TABLES = [f"fgenerador{i}_data" for i in range(1, 8)]


@simulation.get("/simulador/{table_name}")
def get_simulated_data(table_name: str):
    if table_name not in VALID_TABLES:
        raise HTTPException(status_code=404, detail="Tabla no encontrada")

    now = datetime.datetime.now().isoformat()
    data = OrderedDict()

    data["id"] = random.randint(4000, 5000)
    data["timestamp"] = now
    data["rig_config_id"] = 3
    data["session_timestamp"] = "2025-06-08T13:00:00"

    for i in range(1, 19):
        name, unit = NAMES_UNITS[i]
        data[f"name_{i}"] = name
        data[f"channel_{i}"] = round(random.uniform(10, 300), 2)
        data[f"unit_{i}"] = unit

    return {
        "table": table_name,
        "data": data
    }


# FGENRADORES
GENERATOR_NAMES_UNITS = {
    1: ("Status Word", "unidad"),
    2: ("Status Word 2", "unidad"),
    3: ("Engine Fuel Rate. Differencial", "l"),
    4: ("Total Fuel Used Differencial (Clearabe)", "l"),
    5: ("Flowmeter Hours Of Operation (Clearable)", "m/s"),
    6: ("Flowmeter Hours Of Operation Suministro A-Gen (Clearable)", "unidad"),
    7: ("Total Fuel Used Retorno A-Gen (Clearabe)", "unidad"),
    8: ("Flowmeter Hours Of Operation Retorno A-Gen (Clearable)", "unidad"),
    9: ("Engine temperature Suministro", "unidad"),
    10: ("Potencia Activa", "kW"),
    11: ("Voltaje", "l"),
    12: ("Corriente", "unidad"),
    13: ("Frecuencia", "unidad"),
    14: ("Potencia Aparente", "unidad"),
    15: ("Combustible Diferencial Total Usado", "unidad"),
    16: ("Potencia Reactiva", "unidad"),
    17: ("Factor Potencia", "unidad"),
    18: ("Consumo Actual", "unidad"),
}

# DRAW WORKS
DRAWWORKS_NAMES_UNITS = {
    1: ("Main Drum RPM", "rpm"),
    2: ("Brake Pressure", "psi"),
    3: ("Line Pull", "tons"),
    4: ("Clutch Temperature", "°C"),
    5: ("Drum Torque", "Nm"),
    6: ("Gearbox Oil Temp", "°C"),
    7: ("Brake Oil Temp", "°C"),
    8: ("Hydraulic Pressure", "bar"),
    9: ("Lubrication Flow", "l/min"),
    10: ("Gearbox Vibration", "mm/s"),
    11: ("Brake Pad Wear", "%"),
    12: ("Control Voltage", "V"),
    13: ("Motor Current", "A"),
    14: ("Hoisting Speed", "m/min"),
    15: ("Brake Torque", "Nm"),
    16: ("Emergency Brake Pressure", "psi"),
    17: ("System Status", "unidad"),
    18: ("Control Signal Strength", "%")
}

# TOP DRIVE
TOP_DRIVE_NAMES_UNITS = {
    1: ("Rotation Speed", "rpm"),
    2: ("Torque Output", "Nm"),
    3: ("Hydraulic Pressure", "bar"),
    4: ("Gearbox Temp", "°C"),
    5: ("Electrical Consumption", "kw"),
    6: ("Main Shaft Vibration", "mm/s"),
    7: ("Cooling System Temp", "°C"),
    8: ("Lubrication Pressure", "psi"),
    9: ("System Voltage", "V"),
    10: ("Drive Motor Current", "A"),
    11: ("Brake Engagement", "%"),
    12: ("Control Signal Quality", "%"),
    13: ("Directional Alignment", "°"),
    14: ("Speed Variance", "rpm"),
    15: ("Torque Fluctuation", "Nm"),
    16: ("Oil Level", "%"),
    17: ("Maintenance Timer", "h"),
    18: ("Operational Status", "unidad")
}

# MUD PUMP
MUD_PUMP_NAMES_UNITS = {
    1: ("Pump Stroke Rate", "spm"),
    2: ("Discharge Pressure", "psi"),
    3: ("Suction Pressure", "psi"),
    4: ("Pump Efficiency", "%"),
    5: ("Hydraulic Oil Temp", "°C"),
    6: ("Pump Liner Wear", "%"),
    7: ("Vibration Level", "mm/s"),
    8: ("Motor Load", "%"),
    9: ("Fluid Flow Rate", "l/min"),
    10: ("Piston Movement", "mm"),
    11: ("Valve Condition", "%"),
    12: ("Seal Pressure", "bar"),
    13: ("Stroke Counter", "cuentas"),
    14: ("Oil Pressure", "bar"),
    15: ("Temperature Rise", "°C"),
    16: ("Pump Speed Variation", "rpm"),
    17: ("Operational Status", "unidad"),
    18: ("Control Signal", "%")
}

# GENERATORS
GENERATOR_GENERAL_NAMES_UNITS = {
    1: ("Generator Status", "unidad"),
    2: ("Fuel Rate", "l/h"),
    3: ("Total Fuel Used", "l"),
    4: ("Running Hours", "h"),
    5: ("Oil Temperature", "°C"),
    6: ("Coolant Temperature", "°C"),
    7: ("Exhaust Temperature", "°C"),
    8: ("Battery Voltage", "V"),
    9: ("Frequency", "Hz"),
    10: ("Active Power", "kW"),
    11: ("Reactive Power", "kVAR"),
    12: ("Apparent Power", "kVA"),
    13: ("Power Factor", "%"),
    14: ("Phase Voltage", "V"),
    15: ("Phase Current", "A"),
    16: ("Engine Load", "%"),
    17: ("Generator RPM", "rpm"),
    18: ("System Alarms", "unidad")
}

VALID_TABLES = [
    *[f"fgenerador{i}_data" for i in range(1, 8)],
    "drawworks",
    "top-drive",
    *[f"mud-pump{i}" for i in range(1, 4)],
    *[f"generator{i}" for i in range(1, 6)],
    "calculos_resultado"
]


TABLE_TO_DICTIONARY = {
    **{f"fgenerador{i}_data": GENERATOR_NAMES_UNITS for i in range(1, 8)},
    "drawworks": DRAWWORKS_NAMES_UNITS,
    "top-drive": TOP_DRIVE_NAMES_UNITS,
    **{f"mud-pump{i}": MUD_PUMP_NAMES_UNITS for i in range(1, 4)},
    **{f"generator{i}": GENERATOR_GENERAL_NAMES_UNITS for i in range(1, 6)},
}


@simulation.get("/simulation/{table_name}")
def get_simulated_data(table_name: str):
    if table_name not in VALID_TABLES:
        raise HTTPException(status_code=404, detail="Tabla no encontrada")

    now = datetime.datetime.now().isoformat()
    data = OrderedDict()
    data["id"] = random.randint(1000, 9999)
    data["timestamp"] = now
    data["session_timestamp"] = (
        datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()

    # ✅ CASO ESPECIAL para codigo_resultado
    if table_name == "calculos_resultado":
        for i in range(1, 21):
            index = str(i).zfill(1)
            data[f"codigo_{index}"] = f"CO2 G{index}"
            data[f"resultado_{index}"] = round(random.uniform(10, 1000), 2)
            data[f"unidad_{index}"] = random.choice(
                ["kg", "m/s", "psi", "°C", "unidad"])
        return {"table": table_name, "data": data}

    # ✅ CASO GENERAL para el resto
    readings = TABLE_TO_DICTIONARY.get(table_name, {})
    for i in range(1, 19):
        name, unit = readings[i]
        data[f"name_{i}"] = name
        data[f"channel_{i}"] = round(random.uniform(10, 300), 2)
        data[f"unit_{i}"] = unit
        data[f"min_{i}"] = round(random.uniform(10, 300), 2)
        data[f"max_{i}"] = round(random.uniform(10, 300), 2)
        data[f"state_{i}"] = random.choice(["normal", "warning", "alarm"])
        data[f"timestamp_{i}"] = datetime.datetime.now().isoformat()

    return {"table": table_name, "data": data}
