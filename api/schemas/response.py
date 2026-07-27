from pydantic import BaseModel


class AnswerResponse(BaseModel):
    question: str
    answer: str
