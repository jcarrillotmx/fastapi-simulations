from urllib.parse import quote_plus
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# # URL de conexión correcta como string
# DATABASE_URL = "mysql+pymysql://root:ovilla@localhost:3306/fastapi"

# # Crear engine una sola vez
# engine = create_engine(DATABASE_URL)

# # MetaData para usar luego en models
# meta = MetaData()

# connection = engine.connect()

# MySQL Connection
host = '192.168.3.15'
user = 'devturingmx'
password = quote_plus('des@rrollo')
database = 'sistema_monitoreo'

# Create SQLAlchemy engine
connection_url = f'mysql+pymysql://{user}:{password}@{host}/{database}'

engine = create_engine(connection_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
