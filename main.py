from fastapi import Body, FastAPI
from pydantic import BaseModel, Field, field_validator

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


class StatsRequest(BaseModel):
    text: str = Field(
        ...,
        description="Text that will be analyzed for statistics.",
        json_schema_extra={"example": "dowolny tekst"},
    )


class StatsResponse(BaseModel):
    text: str = Field(..., description="Original text provided in the request.")
    word_count: int = Field(..., ge=0, description="Number of words in the text.")
    char_count: int = Field(..., ge=0, description="Number of characters in the text.")


class UppercaseRequest(BaseModel):
    text: str = Field(
        ...,
        description="Text that will be converted to uppercase.",
        json_schema_extra={"example": "dowolny tekst"},
    )

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("text must not be empty")
        return value


class UppercaseResponse(BaseModel):
    original_text: str = Field(..., description="Original text provided in the request.")
    uppercase_text: str = Field(..., description="Uppercase representation of the original text.")
    length: int = Field(..., ge=0, description="Length of the original text in characters.")


def count_words(text: str) -> int:
    words = [word for word in text.split() if word]
    return len(words)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/process", response_model=ProcessedText)
def process_text(payload: TextPayload) -> ProcessedText:
    return ProcessedText(text=payload.text, word_count=count_words(payload.text))


@app.post(
    "/stats",
    response_model=StatsResponse,
    summary="Return word and character statistics",
    response_description="Word and character counts for the provided text.",
)
def text_stats(
    payload: StatsRequest = Body(
        ...,
        examples={
            "default": {
                "summary": "Statystyki tekstu",
                "description": "Policz liczbę słów i znaków w tekście.",
                "value": {"text": "dowolny tekst"},
            }
        },
    )
) -> StatsResponse:
    """Return the original text along with its word and character counts."""

    return StatsResponse(
        text=payload.text,
        word_count=count_words(payload.text),
        char_count=len(payload.text),
    )


@app.post(
    "/uppercase",
    response_model=UppercaseResponse,
    summary="Convert text to uppercase",
    response_description="The uppercase text along with metadata.",
)
def uppercase_text(
    payload: UppercaseRequest = Body(
        ...,
        examples={
            "default": {
                "summary": "Tekst przykładowy",
                "description": "Przekonwertuj dowolny tekst na wersaliki.",
                "value": {"text": "dowolny tekst"},
            }
        },
    )
) -> UppercaseResponse:
    """Return uppercase representation of the provided text together with basic metadata.

    The endpoint validates that the input text is not empty and responds with the original text,
    its uppercase variant, and the original length in characters.
    """

    uppercase_value = payload.text.upper()
    return UppercaseResponse(
        original_text=payload.text,
        uppercase_text=uppercase_value,
        length=len(payload.text),
    )
