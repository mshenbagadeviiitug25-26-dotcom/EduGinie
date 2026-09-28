from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from models import (
    TaskRequest,
    QAResponse,
    ExplainResponse,
    QuizResponse,
    SummaryResponse,
    LearningPathResponse,
    HealthResponse,
)
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name
        },
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        gemini_configured=bool(settings.gemini_api_key),
        model=settings.gemini_model,
    )


@app.post("/qa", response_model=QAResponse)
async def qa(payload: TaskRequest):
    return await answer_question(payload.text)


@app.post("/explain", response_model=ExplainResponse)
async def explain(payload: TaskRequest):
    return await explain_topic(payload.text)


@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: TaskRequest):
    return await generate_quiz(payload.text)


@app.post("/summarize", response_model=SummaryResponse)
async def summarize(payload: TaskRequest):
    return await summarize_text(payload.text)


@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse,
)
async def learning_recommendations(payload: TaskRequest):
    return await get_learning_recommendations(payload.text)