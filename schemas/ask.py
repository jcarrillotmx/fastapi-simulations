from pydantic import BaseModel
from typing import List


# 🧠 Modelo del body esperado
class AskRequest(BaseModel):
    question: str
    max_length: int
    rag: bool

# 📤 Modelo de la respuesta


class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    context_type: str
