from kafka import KafkaConsumer
import json
import time

# Configurar el consumidor
consumer = KafkaConsumer(
    'rigcore-data',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='rigcore-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


def main():
    print("Iniciando consumer en formato JSON...")
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
                            # Reemplaza con la última versión
                            data_batch[table] = data

            # Imprimir el batch completo como JSON
            if data_batch:
                json_output = []
                for table, data in data_batch.items():
                    json_output.append({
                        "table": table,
                        "data": data
                    })

                print(json.dumps(json_output, indent=2, ensure_ascii=False))
            else:
                print("[]")

    except KeyboardInterrupt:
        print("Consumer detenido manualmente.")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
