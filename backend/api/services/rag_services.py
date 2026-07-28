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

        # Call the actual RAG pipeline.
        answer = self.rag.ask(question)

        return {
            "question": question,
            "answer": answer,
        }

    def retrieve(self, question: str):

        # Call the retriever directly without generating an answer.
        chunks = self.rag.retriever.retrieve(
            query=question,
            top_k=5,
        )

        return {
            "question": question,
            "chunks": chunks,
        }

    def decompose(self, question: str):
        # Ask the query decomposer to split the question
        # into one or more simpler search queries.
        sub_queries = self.rag.retriever.query_decomposer.decompose(question)

        return {
            "question": question,
            "sub_queries": sub_queries,
        }


# Create one shared service object for the entire application.
# Every API request will reuse this object instead of creating
# a new RAGService each time.
rag_service = RAGService()
