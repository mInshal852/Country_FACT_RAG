from fastapi import APIRouter
from api.schemas.request import QuestionRequest
from api.schemas.response import AnswerResponse
from api.services.rag_services import rag_service
import logging
import time

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ask", tags=["ask"])


@router.post(
    "/",
    response_model=AnswerResponse,
    summary="Generate an answer",
    description="Answers a country-related question using the Country FACT RAG pipeline.",
)
def asking(request: QuestionRequest):
    start_time = time.perf_counter()
    logger.info("Received question")

    result = rag_service.ask(request.question)
    logger.info("Answer generated successfully")
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    logger.info(f"Total time in Answer generating: {elapsed}")
    return result
