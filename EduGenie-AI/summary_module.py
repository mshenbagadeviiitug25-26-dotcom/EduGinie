from models import SummaryResponse
from gemini_client import generate_text


async def summarize_text(
    text: str
) -> SummaryResponse:

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational passage.

PASSAGE:

{text}

Requirements:

1. Keep the main ideas.
2. Keep important facts.
3. Remove repetition.
4. Use simple language.
5. Make it useful for revision.
6. Do not add facts that are not in the passage.
7. Use bullet points where useful.
"""

    summary = generate_text(
        prompt=prompt,
        temperature=0.25,
        max_output_tokens=1000,
    )

    return SummaryResponse(
        summary=summary
    )