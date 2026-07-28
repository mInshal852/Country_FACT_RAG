from pydantic import BaseModel, Field, field_validator


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User question",
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str):
        # Remove spaces from the beginning and end.
        value = value.strip()

        # Reject questions that are empty after removing spaces.
        if not value:
            raise ValueError("Question cannot be empty.")

        return value
