from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Text Processing API",
    description="Simple REST API that returns service health and text statistics.",
    version="0.1.0",
)


class TextPayload(BaseModel):
    text: str


class ProcessedText(BaseModel):
    text: str
    word_count: int


def count_words(text: str) -> int:
    words = [word for word in text.split() if word]
    return len(words)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/process", response_model=ProcessedText)
def process_text(payload: TextPayload) -> ProcessedText:
    return ProcessedText(text=payload.text, word_count=count_words(payload.text))
