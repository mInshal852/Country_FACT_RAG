from pydantic import BaseModel
from typing import Any


class AnswerResponse(BaseModel):
    question: str
    answer: str


class RetrieveResponse(BaseModel):
    question: str
    chunks: list[Any]


class DecomposeResponse(BaseModel):
    question: str
    sub_queries: list[str]
