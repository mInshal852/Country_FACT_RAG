from fastapi import APIRouter

from backend.api.schemas.request import QuestionRequest
from backend.api.schemas.response import DecomposeResponse
from backend.api.services.rag_services import rag_service
import logging
import time

logger = logging.getLogger(__name__)
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
    start_time = time.perf_counter()
    logger.info("Decomposing user query")

    result = rag_service.decompose(request.question)
    logger.info("Query decomposed successfully")
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    logger.info(f"Total time in Decomposition: {elapsed}")

    return result
