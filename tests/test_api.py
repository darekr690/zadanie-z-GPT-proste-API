from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_process_endpoint_counts_words():
    payload = {"text": "dowolny   tekst"}
    response = client.post("/process", json=payload)

    assert response.status_code == 200
    assert response.json() == {"text": payload["text"], "word_count": 2}


def test_process_endpoint_handles_empty_text():
    payload = {"text": ""}
    response = client.post("/process", json=payload)

    assert response.status_code == 200
    assert response.json()["word_count"] == 0
