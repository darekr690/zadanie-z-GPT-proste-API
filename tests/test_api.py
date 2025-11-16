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


def test_uppercase_endpoint_success():
    payload = {"text": "Dowolny Tekst"}
    response = client.post("/uppercase", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "original_text": payload["text"],
        "uppercase_text": payload["text"].upper(),
        "length": len(payload["text"]),
    }


def test_uppercase_endpoint_rejects_empty_text():
    response = client.post("/uppercase", json={"text": ""})

    assert response.status_code == 422
    body = response.json()
    assert "text must not be empty" in body["detail"][0]["msg"]
