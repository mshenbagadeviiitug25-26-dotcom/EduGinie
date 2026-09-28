from fastapi.testclient import TestClient

import main

from models import (
    QAResponse,
    ExplainResponse,
    QuizQuestion,
    QuizResponse,
    SummaryResponse,
    LearningPathResponse,
    LearningStep,
)


client = TestClient(main.app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_empty_question():

    response = client.post(
        "/qa",
        json={
            "text": ""
        },
    )

    assert response.status_code == 422


def test_qa_endpoint(
    monkeypatch
):

    async def fake_answer(
        question
    ):

        return QAResponse(
            answer=
            f"Mock answer: {question}"
        )

    monkeypatch.setattr(
        main,
        "answer_question",
        fake_answer
    )

    response = client.post(
        "/qa",
        json={
            "text":
            "What is AI?"
        },
    )

    assert response.status_code == 200

    assert "Mock answer" in \
        response.json()["answer"]


def test_explain_endpoint(
    monkeypatch
):

    async def fake_explain(
        topic
    ):

        return ExplainResponse(
            explanation=
            "Simple explanation",
            engine="test",
        )

    monkeypatch.setattr(
        main,
        "explain_topic",
        fake_explain
    )

    response = client.post(
        "/explain",
        json={
            "text":
            "Quantum computing"
        },
    )

    assert response.status_code == 200

    assert response.json()["engine"] == \
        "test"


def test_quiz_endpoint(
    monkeypatch
):

    async def fake_quiz(
        text
    ):

        return QuizResponse(

            questions=[

                QuizQuestion(
                    question=
                    "2 + 2 = ?",

                    options=[
                        "3",
                        "4",
                        "5",
                        "6",
                    ],

                    correct_answer="4",

                    explanation=
                    "Basic addition.",
                ),

                QuizQuestion(
                    question=
                    "Which is a planet?",

                    options=[
                        "Sun",
                        "Earth",
                        "Moon",
                        "Galaxy",
                    ],

                    correct_answer=
                    "Earth",

                    explanation=
                    "Earth is a planet.",
                ),

                QuizQuestion(
                    question=
                    "Water formula?",

                    options=[
                        "CO2",
                        "H2O",
                        "O2",
                        "NaCl",
                    ],

                    correct_answer=
                    "H2O",

                    explanation=
                    "H2O is water.",
                ),
            ]
        )

    monkeypatch.setattr(
        main,
        "generate_quiz",
        fake_quiz
    )

    response = client.post(
        "/quiz",
        json={
            "text":
            "Basic science"
        },
    )

    assert response.status_code == 200

    assert len(
        response.json()["questions"]
    ) == 3


def test_summary_endpoint(
    monkeypatch
):

    async def fake_summary(
        text
    ):

        return SummaryResponse(
            summary="Short summary"
        )

    monkeypatch.setattr(
        main,
        "summarize_text",
        fake_summary
    )

    response = client.post(
        "/summarize",
        json={
            "text":
            "Long educational text"
        },
    )

    assert response.status_code == 200

    assert response.json()["summary"] == \
        "Short summary"


def test_learning_path_endpoint(
    monkeypatch
):

    async def fake_learning_path(
        topic
    ):

        return LearningPathResponse(

            topic=topic,

            learning_path=[

                LearningStep(
                    level="Beginner",
                    topics=["Basics"],
                    timeline="1 week",
                    resources=[
                        "Documentation"
                    ],
                )

            ],

            tips=[
                "Practice daily"
            ],
        )

    monkeypatch.setattr(
        main,
        "get_learning_recommendations",
        fake_learning_path
    )

    response = client.post(
        "/learn/recommendations",
        json={
            "text": "SQL"
        },
    )

    assert response.status_code == 200

    assert response.json()["topic"] == \
        "SQL"