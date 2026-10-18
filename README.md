# Student CRUD API

A simple REST API for managing students, built with [FastAPI](https://fastapi.tiangolo.com/) and Pydantic. Data is stored in memory, so it resets when the server restarts.

## Features

- Full CRUD for students
- Request/response validation with Pydantic
- Unique email enforcement
- Correct HTTP status codes
- Interactive docs (Swagger UI) generated automatically

## Requirements

- Python 3.9+

## Setup

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

The API is served at `http://127.0.0.1:8000`.

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Student model

| Field    | Type    | Rules                          |
|----------|---------|--------------------------------|
| `id`     | integer | Auto-generated, read-only      |
| `name`   | string  | Required, 1–100 characters     |
| `email`  | string  | Required, valid email, unique  |
| `age`    | integer | Required, 1–120                |
| `course` | string  | Required, 1–100 characters     |

## Endpoints

| Method   | Path                    | Description          | Success | Errors        |
|----------|-------------------------|----------------------|---------|---------------|
| `POST`   | `/students`             | Create a student     | `201`   | `409`, `422`  |
| `GET`    | `/students`             | List all students    | `200`   |               |
| `GET`    | `/students/{student_id}`| Get one student      | `200`   | `404`         |
| `PUT`    | `/students/{student_id}`| Replace a student    | `200`   | `404`, `409`, `422` |
| `DELETE` | `/students/{student_id}`| Delete a student     | `204`   | `404`         |

Status codes: `404` = student not found, `409` = email already registered, `422` = validation error.

## Examples

Create:

```bash
curl -X POST http://127.0.0.1:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Asha Patil", "email": "asha@example.com", "age": 21, "course": "Computer Science"}'
```

Response (`201 Created`):

```json
{
  "name": "Asha Patil",
  "email": "asha@example.com",
  "age": 21,
  "course": "Computer Science",
  "id": 1
}
```

List, get, update, delete:

```bash
curl http://127.0.0.1:8000/students
curl http://127.0.0.1:8000/students/1
curl -X PUT http://127.0.0.1:8000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Asha Patil", "email": "asha@example.com", "age": 22, "course": "Data Science"}'
curl -X DELETE http://127.0.0.1:8000/students/1
```

## Project structure

```
student_crud_api/
├── main.py            # FastAPI app, models, and routes
├── requirements.txt
├── README.md
└── LICENSE
```

## Notes

- Storage is an in-memory dictionary; swap it for a database (e.g. SQLAlchemy + SQLite) for persistence.
- `PUT` replaces the whole record, so all fields are required.

## License

See [LICENSE](LICENSE).
