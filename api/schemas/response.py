from pydantic import BaseModel
from typing import Any


class AnswerResponse(BaseModel):
    question: str
    answer: str


class RetrieveResponse(BaseModel):
    question: str
    chunks: list[Any]
