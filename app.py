from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from routes.user import user
from routes.simulation import simulation
from routes.notifications import notification
from routes.alan import alan
from routes.kafka import kafka

# Crear un servidor basico
app = FastAPI()


# 📦 Middleware para loguear las peticiones
@app.middleware("http")
async def log_request(request: Request, call_next):
    print(f"➡️  {request.method} {request.url.path}")

    try:
        body = await request.json()
        if body:
            print("📦 Body:", body)
    except:
        # No todas las peticiones tienen body JSON
        pass

    response = await call_next(request)
    return response

# Llamar las rutas definidas en otra carpeta
app.include_router(user)
app.include_router(simulation)
app.include_router(notification)
app.include_router(alan)
app.include_router(kafka)

# 🔓 Middleware para habilitar CORS
app.add_middleware(
    CORSMiddleware,
    # o especifica ["http://localhost:3000"] por seguridad
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
