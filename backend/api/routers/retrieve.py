from fastapi import APIRouter

from api.schemas.request import QuestionRequest
from api.schemas.response import RetrieveResponse
from api.services.rag_services import rag_service
import logging
import time

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/retrieve",
    tags=["Retrieve"],
)


@router.post(
    "/",
    response_model=RetrieveResponse,
    summary="Retrieve relevant chunks",
    description="Returns the most relevant document chunks without generating an answer.",
)
def retrieve(request: QuestionRequest):
    start_time = time.perf_counter()
    logger.info("Retrieving relevant chunks")

    answer = rag_service.retrieve(request.question)

    logger.info("Retrieved relevant chunks successfully")
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    logger.info(f"Total time in retrieval: {elapsed}")

    return answer
