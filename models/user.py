# from sqlalchemy import Table, Column
# from sqlalchemy.sql.sqltypes import Integer, String
# from config.db import meta, engine

# # Se define la tabla de usuarios
# users = Table(
#     "users",
#     meta,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(255)),
#     Column("email", String(255)),
#     Column("password", String(255)),
# )

# # Esto crea las tablas en la base de datos
# meta.create_all(engine)
