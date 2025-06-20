from sqlalchemy import create_engine, MetaData

# URL de conexión correcta como string
DATABASE_URL = "mysql+pymysql://root:ovilla@localhost:3306/fastapi"

# Crear engine una sola vez
engine = create_engine(DATABASE_URL)

# MetaData para usar luego en models
meta = MetaData()

connection = engine.connect()
