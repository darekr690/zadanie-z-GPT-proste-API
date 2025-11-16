from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_stats_returns_basic_counts():
    payload = {"text": "Hello world!"}
    response = client.post("/stats", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "text": payload["text"],
        "word_count": 2,
        "char_count": len(payload["text"]),
        "unique_words": 2,
    }


def test_stats_handles_repeated_words_and_punctuation():
    payload = {"text": "Repeat, repeat; REPEAT."}
    response = client.post("/stats", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "text": payload["text"],
        "word_count": 3,
        "char_count": len(payload["text"]),
        "unique_words": 1,
    }
