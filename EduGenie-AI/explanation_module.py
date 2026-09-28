from models import ExplainResponse
from gemini_client import generate_text
from config import settings


def local_explanation(topic: str) -> str:

    from transformers import pipeline

    generator = pipeline(
        "text2text-generation",
        model=settings.local_explainer_model,
    )

    prompt = (
        "Explain this educational topic in simple language "
        "for a beginner. Topic: "
        + topic
    )

    result = generator(
        prompt,
        max_new_tokens=220,
        do_sample=False,
    )

    return result[0]["generated_text"].strip()


async def explain_topic(
    topic: str
) -> ExplainResponse:

    topic = topic.strip()

    # Optional local AI model
    if settings.use_local_explainer:

        try:

            explanation = local_explanation(
                topic
            )

            return ExplainResponse(
                explanation=explanation,
                engine="LaMini-Flan-T5",
            )

        except Exception:

            # If local model fails,
            # use Gemini as fallback.
            pass

    prompt = f"""
You are an expert teacher helping a beginner.

Explain this topic:

{topic}

Follow these rules:

1. Start with a simple definition.
2. Explain the concept in easy language.
3. Break difficult ideas into smaller parts.
4. Give a real-world example or analogy.
5. Provide three important points.
6. Avoid unnecessary technical jargon.
7. Make the explanation useful for a student.
"""

    explanation = generate_text(
        prompt=prompt,
        temperature=0.35,
        max_output_tokens=1000,
    )

    return ExplainResponse(
        explanation=explanation,
        engine="Gemini",
    )