from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from schemas.ask import AskRequest, AskResponse

alan = APIRouter()


# 📮 Ruta POST /ask
@alan.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    # Validación implícita gracias a Pydantic
    return AskResponse(
        answer=(
            "I'm happy to help! Based on the provided context from technical "
            "documentation and source code, I will provide a detailed analysis "
            "of your question.\n\nPlease go ahead and ask your question."
        ),
        sources=['form.tsx', 'tailwind.config.ts', 'chart.tsx', 'utils.ts'],
        context_type='general'
    )


# Suponemos que esta variable indica si Alan está en línea
alan_online = True
# alan_online = False


@alan.get("/health")
async def health():
    if alan_online:
        return JSONResponse(status_code=200, content={"status": "ok"})
    else:
        # Devuelve un error 404 con mensaje personalizado
        raise HTTPException(status_code=404, detail="Alan is offline")
