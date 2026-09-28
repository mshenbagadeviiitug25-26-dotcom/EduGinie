import json

from models import LearningPathResponse
from gemini_client import generate_json


async def get_learning_recommendations(
    topic: str
) -> LearningPathResponse:

    prompt = f"""
You are EduGenie, an educational learning-path designer.

Create a structured learning path for:

{topic}

Requirements:

1. Start at beginner level.
2. Progress to intermediate level.
3. Progress to advanced level.
4. Include important topics at each level.
5. Give a realistic timeline.
6. Suggest useful resource TYPES such as:
   - documentation
   - books
   - videos
   - articles
   - practice projects
7. Do not invent specific URLs.
8. Include useful study tips.
9. Return only JSON matching the supplied schema.
"""

    raw = generate_json(
        prompt=prompt,
        schema=LearningPathResponse.model_json_schema(),
        temperature=0.35,
        max_output_tokens=2200,
    )

    try:

        data = json.loads(raw)

        result = LearningPathResponse.model_validate(
            data
        )

    except Exception as exc:

        raise ValueError(
            f"Invalid learning path from Gemini: {exc}"
        ) from exc

    if not result.learning_path:

        raise ValueError(
            "Gemini returned an empty learning path."
        )

    return result