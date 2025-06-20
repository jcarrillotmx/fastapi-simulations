from fastapi import APIRouter

import random

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
            "status_word": str(random.randint(0, 100)),
            "status_word_2": random.randint(0, 100),
            "consumo_actual": round(random.uniform(10, 100), 2),
            "combustible_diferencial_total_usado": round(random.uniform(10, 100), 2),
            "combustible_total_usado_suministrado": round(random.uniform(10, 100), 2),
            "horometro_dfm_suministro": round(random.uniform(10, 100), 2),
            "combustible_total_usado_retorno": round(random.uniform(10, 100), 2),
            "horometro_dfm_retorno": round(random.uniform(10, 100), 2),
            "fuel_temp_suministro": round(random.uniform(10, 100), 2),
            "fuel_temp_retorno": round(random.uniform(10, 100), 2),
            "voltaje": round(random.uniform(200, 250), 2),
            "corriente": round(random.uniform(10, 50), 2),
            "frecuencia": round(random.uniform(49, 61), 2),
            "potencia_aparente": round(random.uniform(500, 2000), 2),
            "potencia_activa": round(random.uniform(400, 1800), 2),
            "potencia_reactiva": round(random.uniform(300, 1500), 2),
            "factor_de_potencia": round(random.uniform(0.5, 1.0), 2),
        }
    }
