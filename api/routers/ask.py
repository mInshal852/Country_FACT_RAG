from fastapi import APIRouter
from api.schemas.request import QuestionRequest
from api.schemas.response import AnswerResponse
from api.services.rag_services import rag_service

router = APIRouter(prefix="/ask", tags=["ask"])


@router.post(
    "/",
    response_model=AnswerResponse,
    summary="Generate an answer",
    description="Answers a country-related question using the Country FACT RAG pipeline.",
)
def asking(request: QuestionRequest):

    result = rag_service.ask(request.question)
    return result
