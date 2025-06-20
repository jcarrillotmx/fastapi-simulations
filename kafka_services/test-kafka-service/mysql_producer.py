from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from kafka import KafkaProducer
import json
import time
import datetime

# MySQL Connection
host = '192.168.3.102'
user = 'devturingmx'
password = quote_plus('des@rrollo')
database = 'sistema_monitoreo'

# Create SQLAlchemy engine
connection_url = f'mysql+pymysql://{user}:{password}@{host}/{database}'
engine = create_engine(connection_url)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


def fetch_and_send_data():
    try:
        query = "SELECT * FROM fgenerador1_data ORDER BY id DESC LIMIT 1"
        with engine.connect() as connection:
            # Añadimos text ya que sqlalchemy no es compatible directamente con cadenas de texto
            result = connection.execute(text(query)).fetchone()
            if result:
                # Modificamos data para convertir manualmete el timestamp por que json.dumps no puede convertirlo automaticamente
                data = {
                    key: (value.isoformat() if isinstance(
                        value, (datetime.datetime, datetime.date)) else value)
                    for key, value in dict(result._mapping).items()
                }

                producer.send('rigcore-data', value=data)
                producer.flush()
                print(f"Sent data: {data}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    while True:
        fetch_and_send_data()
        time.sleep(1)


if __name__ == "__main__":
    main()

# from sqlalchemy import create_engine
# from urllib.parse import quote_plus
# from kafka import KafkaProducer
# import json
# import time

# # MySQL Connection (reusing your existing configuration)
# host = '192.168.3.102'
# user = 'devturingmx'
# password = quote_plus('des@rrollo')
# database = 'sistema_monitoreo'

# # Create SQLAlchemy engine
# connection_url = f'mysql+pymysql://{user}:{password}@{host}/{database}'
# engine = create_engine(connection_url)

# # Initialize Kafka producer
# producer = KafkaProducer(
#     bootstrap_servers=['localhost:9092'],
#     value_serializer=lambda x: json.dumps(x).encode('utf-8')
# )

# def fetch_and_send_data():
#     try:
#         # Example query - modify according to your needs
#         query = "SELECT * FROM wits_data ORDER BY id DESC LIMIT 1"
#         with engine.connect() as connection:
#             result = connection.execute(query).fetchone()
#             if result:
#                 # Convert row to dictionary
#                 data = dict(result._mapping)
#                 # Send to Kafka topic
#                 producer.send('rigcore-data', value=data)
#                 producer.flush()
#                 print(f"Sent data: {data}")
#     except Exception as e:
#         print(f"Error: {e}")

# def main():
#     while True:
#         fetch_and_send_data()
#         time.sleep(1)  # Wait 1 second before next fetch

# if __name__ == "__main__":
#     main()
