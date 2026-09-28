from gemini_client import generate_text
from models import QAResponse


async def answer_question(
    question: str
) -> QAResponse:

    question = question.strip()

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question accurately and clearly.

Rules:

1. Use simple language.
2. Give the direct answer first.
3. Explain the important concept.
4. If appropriate, give an example.
5. If calculations are required, show the important steps.
6. Do not invent sources.
7. If the question is ambiguous, clearly state your assumption.

Student question:

{question}
"""

    answer = generate_text(
        prompt=prompt,
        temperature=0.3,
        max_output_tokens=1000,
    )

    return QAResponse(
        answer=answer
    )