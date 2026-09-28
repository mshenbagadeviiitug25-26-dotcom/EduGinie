import json

from models import QuizResponse
from gemini_client import generate_json


async def generate_quiz(
    source_text: str
) -> QuizResponse:

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions from
the following educational content.

CONTENT:

{source_text}

Requirements:

1. Generate exactly 3 questions.
2. Every question must have exactly 4 options.
3. There must be exactly one correct answer.
4. correct_answer must exactly match one option.
5. Include a short explanation for the answer.
6. Questions must be based on the supplied content.
7. Make distractors plausible.
8. Return only valid JSON matching the supplied schema.
"""

    raw = generate_json(
        prompt=prompt,
        schema=QuizResponse.model_json_schema(),
        temperature=0.2,
        max_output_tokens=1800,
    )

    try:

        data = json.loads(raw)

        quiz = QuizResponse.model_validate(
            data
        )

    except Exception as exc:

        raise ValueError(
            f"Invalid quiz response from Gemini: {exc}"
        ) from exc

    if len(quiz.questions) != 3:

        raise ValueError(
            "Gemini must return exactly 3 questions."
        )

    for question in quiz.questions:

        if len(question.options) != 4:

            raise ValueError(
                "Every question must contain exactly 4 options."
            )

        if question.correct_answer not in question.options:

            raise ValueError(
                "Correct answer must match one of the options."
            )

    return quiz