import os

os.environ.setdefault(
    "GEMINI_API_KEY",
    "test-key"
)

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)