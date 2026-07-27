from fastapi import APIRouter

from api.schemas.request import QuestionRequest
from api.schemas.response import RetrieveResponse
from api.services.rag_services import rag_service

router = APIRouter(
    prefix="/retrieve",
    tags=["Retrieve"],
)


@router.post("/", response_model=RetrieveResponse)
def retrieve(request: QuestionRequest):

    return rag_service.retrieve(request.question)
