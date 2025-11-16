# Text Processing API

Prosty serwis REST napisany w FastAPI, który udostępnia trzy endpointy:

- `GET /health` – sprawdza kondycję aplikacji.
- `POST /process` – przyjmuje tekst i zwraca liczbę słów oraz oryginalny tekst.
- `POST /uppercase` – waliduje tekst i zwraca jego wersję zapisaną wielkimi literami wraz z metadanymi.

## Endpointy

### GET /health
- **Opis**: szybki health-check.
- **Przykładowa odpowiedź**: `{ "status": "ok" }`

### POST /process
- **Body (JSON)**: `{ "text": "dowolny tekst" }`
- **Odpowiedź**: `{ "text": "dowolny tekst", "word_count": 2 }`
- **Zastosowanie**: oblicza liczbę słów w tekście przy zachowaniu oryginalnej treści.

### POST /uppercase
- **Body (JSON)**: `{ "text": "dowolny tekst" }`
- **Walidacja**: `text` musi być niepusty (znaki białe są traktowane jako pusty tekst).
- **Odpowiedź**: `{ "original_text": "dowolny tekst", "uppercase_text": "DOWOLNY TEKST", "length": 13 }`
- **Zastosowanie**: otrzymaj tekst pisany wersalikami wraz z długością i oryginałem.

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

## Przykłady użycia

```bash
curl -X POST http://127.0.0.1:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "dowolny tekst"}'
```

```bash
curl -X POST http://127.0.0.1:8000/uppercase \
  -H "Content-Type: application/json" \
  -d '{"text": "Dowolny Tekst"}'
```