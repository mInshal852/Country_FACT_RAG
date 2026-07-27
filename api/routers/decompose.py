from fastapi import APIRouter

from api.schemas.request import QuestionRequest
from api.schemas.response import DecomposeResponse
from api.services.rag_services import rag_service

router = APIRouter(
    prefix="/decompose",
    tags=["Decompose"],
)


@router.post(
    "/",
    response_model=DecomposeResponse,
    summary="Decompose a query",
    description="Splits a complex question into one or more simpler search queries.",
)
def decompose(request: QuestionRequest):
    return rag_service.decompose(request.question)
