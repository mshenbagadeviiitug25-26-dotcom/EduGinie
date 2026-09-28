from functools import lru_cache

from fastapi import HTTPException
from google import genai
from google.genai import types

from config import settings


@lru_cache(maxsize=1)
def get_client() -> genai.Client:

    if not settings.gemini_api_key:

        raise HTTPException(
            status_code=503,
            detail=(
                "GEMINI_API_KEY is not configured. "
                "Create a .env file and add your Gemini API key."
            ),
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(
    prompt: str,
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
) -> str:

    client = get_client()

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )

    text = getattr(response, "text", None)

    if not text:

        raise HTTPException(
            status_code=502,
            detail="Gemini returned an empty response.",
        )

    return text.strip()


def generate_json(
    prompt: str,
    schema,
    temperature: float = 0.2,
    max_output_tokens: int = 1800,
):

    client = get_client()

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )

    text = getattr(response, "text", None)

    if not text:

        raise HTTPException(
            status_code=502,
            detail="Gemini returned an empty structured response.",
        )

    return text.strip()