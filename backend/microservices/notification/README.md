# notification microservice

Python / FastAPI microservice, **no database**, with Swagger documentation generated automatically.
It exposes one endpoint for now; the notification logic is a TODO for students (see [TODO.md](TODO.md)).

## Run
```bash
cd chemin\vers\notification

# 1. Créer et activer l'environnement virtuel (une seule fois)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Installer les dépendances
python -m pip install -r requirements.txt

# 3. Lancer le microservice
python -m uvicorn app.main:app --reload --port 8084   # or: python -m app.main
```
- API: http://localhost:8084/api/notifications/hello
- Swagger UI: http://localhost:8084/swagger-ui
- OpenAPI JSON: http://localhost:8084/v3/api-docs
- ReDoc: http://localhost:8084/redoc

Port `8084` (candidat = 8081, job = 8082, meeting = 8083).

## Plusieurs instances (Eureka)
Le port annoncé à Eureka est lu dans la variable `PORT`, sinon dans l'argument `--port`, sinon 8084.
Dans un 2e terminal (venv activé) :
```powershell
python -m uvicorn app.main:app --port 8094
# ou
$env:PORT=8094; python -m app.main
```
Le dashboard http://localhost:8761 doit afficher NOTIFICATION (2) avec les ports 8084 et 8094.

## Endpoint
| Method | Path | Response |
|---|---|---|
| GET | /api/notifications/hello | `200 {"message": "hello I'm microservice notification"}` |

## Tests
```bash
pip install -r requirements-dev.txt
pytest
```

## Structure
```
notification/
├── app/
│   ├── main.py                    FastAPI app + Swagger config
│   ├── schemas.py                 Pydantic models (validation + Swagger schemas)
│   └── routers/notification.py    /api/notifications routes (hello + TODO)
├── tests/test_hello.py
├── TODO.md                        work for students
├── requirements.txt / requirements-dev.txt
└── pytest.ini
```
