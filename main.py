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
