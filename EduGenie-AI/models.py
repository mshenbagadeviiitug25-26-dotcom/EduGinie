from typing import List

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=12000
    )


class QAResponse(BaseModel):
    answer: str


class ExplainResponse(BaseModel):
    explanation: str
    engine: str


class QuizQuestion(BaseModel):
    question: str

    options: List[str] = Field(
        ...,
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str = ""


class QuizResponse(BaseModel):

    questions: List[QuizQuestion] = Field(
        ...,
        min_length=1,
        max_length=10
    )


class SummaryResponse(BaseModel):
    summary: str


class LearningStep(BaseModel):

    level: str

    topics: List[str]

    timeline: str

    resources: List[str]


class LearningPathResponse(BaseModel):

    topic: str

    learning_path: List[LearningStep]

    tips: List[str]


class HealthResponse(BaseModel):

    status: str

    gemini_configured: bool

    model: str