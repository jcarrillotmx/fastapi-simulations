from fastapi import APIRouter
from kafka import KafkaConsumer
import time
import threading
import json

kafka = APIRouter()

# Variable global para almacenar el último mensaje de Kafka
latest_kafka_data = {}


# Función que escucha Kafka
def kafka_listener():
    global latest_kafka_data

    consumer = KafkaConsumer(
        'rigcore-data',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='rigcore-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print('Escuchando datos de Kafka...')

    try:
        # Ciclo para extraer los datos del consumer
        for message in consumer:
            # Guardamos los datos en una variable
            data = message.value
            print(f"Mensaje recibido: {data}")
            # AQUÍ GUARDAMOS LA DATA
            latest_kafka_data = data
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")


# Lanzar hilo para escuchar a kafka en segundo plano
threading.Thread(target=kafka_listener, daemon=True).start()


# Endpoint para consultar la última data
@kafka.get("/kafka")
def get_latest_kafka_data():
    if latest_kafka_data:
        return {"data": latest_kafka_data}
    return {"message": "No data received yet"}
