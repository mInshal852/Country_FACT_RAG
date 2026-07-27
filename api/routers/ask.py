from fastapi import APIRouter
from api.schemas.request import QuestionRequest
from api.services.rag_services import rag_service

router = APIRouter(prefix="/ask", tags=["ask"])


@router.post("/")
def asking(request: QuestionRequest):
    result = rag_service.ask(request.question)
    return result
