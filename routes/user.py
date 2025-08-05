# from fastapi import APIRouter, HTTPException, status
# from config.db import connection
# from models.user import users
# from schemas.user import User, UserOut

# from cryptography.fernet import Fernet

# # Encriptar contraseña
# key = Fernet.generate_key()
# key_to_hash = Fernet(key)

# user = APIRouter()


# # Obtener todos los usuarios
# @user.get("/users", response_model=list[UserOut])
# def get_users():
#     return connection.execute(users.select()).fetchall()


# # Obtener un usuario por id
# @user.get("/users/{user_id}", response_model=UserOut)
# def get_user_by_id(user_id: int):
#     # Buscamos al usuario
#     result = connection.execute(
#         users.select().where(users.c.id == user_id)
#     ).fetchone()

#     # Verificiamos que el usuario exista (en caso de que no exista devolvermos una excepcion)
#     if result is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Si el usuario si existe devolvemos su informacion
#     return {
#         "id": result.id,
#         "name": result.name,
#         "email": result.email,
#         # Omitir la contraseña por seguridad
#     }


# # Registrar un usuario
# @user.post("/users", response_model=User)
# def create_user(user: User):
#     # user.password.encode(): Convierte la contraseña (un str) en bytes, necesario para encriptarla.
#     # key_to_hash.encrypt(...): Usa Fernet (de la librería cryptography) para encriptar la contraseña.
#     # .decode(): Convierte el resultado de la encriptación (que está en bytes) de vuelta a str para poder guardarlo en la base de datos.
#     encrypted_password = key_to_hash.encrypt(user.password.encode()).decode()

#     # users.insert(): Es una instrucción SQLAlchemy que genera una sentencia SQL INSERT INTO users (...) VALUES (...).
#     # .values(): Especifica los valores que se van a insertar en las columnas name, email y password
#     # connection.execute(): Ejecuta esa sentencia SQL directamente sobre la base de datos.
#     result = connection.execute(
#         users.insert().values(
#             name=user.name,
#             email=user.email,
#             password=encrypted_password
#         )
#     )

#     # Confirma (guarda) los cambios realizados por la instrucción SQL anterior en la base de datos.
#     connection.commit()

#     # Obtener el id del usuario insertado
#     user_id = result.lastrowid

#     # Recuperar el usuario insertado
#     created_user = connection.execute(
#         users.select().where(users.c.id == user_id)
#     ).fetchone()

#     # Devuelve una respuesta JSON al cliente (por ejemplo, Postman o una app frontend).
#     return {
#         "id": created_user.id,
#         "name": created_user.name,
#         "email": created_user.email,
#         "password": created_user.password
#     }


# # Actualizar un usuario
# @user.put("/users/{user_id}", response_model=UserOut)
# def update_user(user_id: int, updated_user: User):
#     # Verificar que el usuario exista
#     existing_user = connection.execute(
#         users.select().where(users.c.id == user_id)
#     ).fetchone()

#     if existing_user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Encriptar la nueva contraseña
#     encrypted_password = key_to_hash.encrypt(
#         updated_user.password.encode()).decode()

#     # Ejecutar actualización
#     connection.execute(
#         users.update()
#         .where(users.c.id == user_id)
#         .values(
#             name=updated_user.name,
#             email=updated_user.email,
#             password=encrypted_password
#         )
#     )

#     connection.commit()

#     return {
#         "message": "User updated",
#         "id": user_id,
#         "name": updated_user.name,
#         "email": updated_user.email,
#     }


# # Eliminar un usuario
# @user.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(user_id: int):
#     # Buscar usuario
#     result = connection.execute(
#         users.select().where(users.c.id == user_id)
#     ).fetchone()

#     if result is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Eliminar usuario
#     connection.execute(
#         users.delete().where(users.c.id == user_id)
#     )

#     connection.commit()

#     # Devolver los datos eliminados
#     return {
#         "id": result.id,
#         "name": result.name,
#         "email": result.email,
#     }
