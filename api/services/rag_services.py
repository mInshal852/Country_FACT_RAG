import logging
from fastapi import HTTPException

from rag_pipeline.inference.a7_rag import RAG

# Create a logger for this file.
# A logger is used to save errors and important information.
# Unlike print(), logs can be written to files, monitoring systems,
# or shown in the terminal with different severity levels.
logger = logging.getLogger(__name__)


class RAGService:

    def __init__(self):
        # Create the RAG object only once.
        # This avoids loading the retriever, LLM, and other resources
        # every time a new request comes in.
        self.rag = RAG()

    def ask(self, question: str):
        try:
            # Call the actual RAG pipeline.
            answer = self.rag.ask(question)

            return {
                "question": question,
                "answer": answer,
            }

        except Exception as e:
            # logger.exception(...) automatically logs:
            # - the error message
            # - the complete traceback (where the error happened)
            #
            # This is very useful for debugging because if something
            # fails in production, you can inspect the logs to see
            # exactly what went wrong.
            logger.exception("Failed to generate answer")

            # HTTPException tells FastAPI to return an HTTP error response.
            #
            # Instead of crashing the server or returning a generic
            # "Internal Server Error", the client receives a clean,
            # meaningful JSON response.
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while generating the answer.",
            )

    def retrieve(self, question: str):
        try:
            # Call the retriever directly without generating an answer.
            chunks = self.rag.retriever.retrieve(
                query=question,
                top_k=5,
            )

            return {
                "question": question,
                "chunks": chunks,
            }

        except Exception:
            logger.exception("Failed to retrieve chunks")

            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while retrieving chunks.",
            )

    def decompose(self, question: str):
        pass


# Create one shared service object for the entire application.
# Every API request will reuse this object instead of creating
# a new RAGService each time.
rag_service = RAGService()
