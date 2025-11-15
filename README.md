# Text Processing API

Prosty serwis REST napisany w FastAPI, który udostępnia dwa endpointy:

- `GET /health` – sprawdza kondycję aplikacji.
- `POST /process` – przyjmuje tekst i zwraca liczbę słów oraz oryginalny tekst.

## Wymagania

- Python 3.10+
- Zależności z `requirements.txt`

## Instalacja

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uruchamianie API

```bash
uvicorn main:app --reload
```

Po uruchomieniu dokumentacja OpenAPI będzie dostępna pod `http://127.0.0.1:8000/docs`.

## Testy

```bash
pytest
```

## Przykład użycia

```bash
curl -X POST http://127.0.0.1:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "dowolny tekst"}'
```
TT