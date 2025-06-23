from fastapi import APIRouter, HTTPException
from kafka import KafkaConsumer
import time
import threading
import json

kafka = APIRouter()

# Variable global para almacenar el último mensaje de Kafka
latest_kafka_data = {}

# Diccionario para almacenar la última fila de cada tabla
latest_rows_by_table = {}


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

    # try:
    #     # Ciclo para extraer los datos del consumer
    #     for message in consumer:
    #         # Guardamos los datos en una variable
    #         data = message.value
    #         print(f"Mensaje recibido: {data}")
    #         # AQUÍ GUARDAMOS LA DATA
    #         latest_kafka_data = data
    #         time.sleep(3)
    # except Exception as e:
    #     print(f"Error: {e}")

    try:
        while True:
            start_time = time.time()
            data_batch = {}

            # Recolectar mensajes durante 3 segundos
            while time.time() - start_time < 3:
                raw_msgs = consumer.poll(timeout_ms=100)
                for tp, messages in raw_msgs.items():
                    for message in messages:
                        value = message.value
                        table = value.get("table")
                        data = value.get("data")
                        if table and data:
                            # Sobrescribimos si hay nuevo
                            data_batch[table] = data
                            print(
                                f"[Kafka] Recibido desde {table}: {data}", flush=True)

            # Guardar el batch como última versión global
            if data_batch:
                latest_rows_by_table.update(data_batch)

    except Exception as e:
        print(f"Error en kafka_listener: {e}")


# Lanzar hilo para escuchar a kafka en segundo plano
threading.Thread(target=kafka_listener, daemon=True).start()


# Endpoint para consultar la última data
@kafka.get("/kafka")
def get_latest_kafka_data():
    if latest_kafka_data:
        return {"data": latest_kafka_data}
    return {"message": "No data received yet"}


# Nuevo endpoint: devolver toda la data agrupada por tabla
@kafka.get("/kafka/all")
def get_all_latest_data():
    if latest_rows_by_table:
        return [
            {
                "table": table,
                "data": data
            }

            for table, data in latest_rows_by_table.items()
        ]
    return {"message": "No se ha recibido información de Kafka aún."}


# Endpoint individual por nombre de tabla
@kafka.get("/kafka/tabla/{table_name}")
def get_table_data(table_name: str):
    data = latest_rows_by_table.get(table_name)
    if data:
        return {"table": table_name, "data": data}
    raise HTTPException(
        status_code=404, detail=f"No hay datos disponibles para la tabla '{table_name}'")
