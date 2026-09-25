# PocketSmart AI

PocketSmart AI is a FastAPI web application that creates budget-aware recommendations for home interiors, parties, and jewelry. It uses Gemini when configured and automatically falls back to local recommendations when Gemini is unavailable.

## Features

- User registration, login, JWT authentication, and session information
- Home interior planner
- Party planner
- Jewelry planner with optional outfit image analysis
- Recommendation history stored per user
- SQLite by default, with SQLAlchemy database support
- Gemini AI integration with local fallback recommendations
- Jinja2 web interface and FastAPI JSON API
- Interactive API documentation

## Requirements

- Python 3.10 or newer
- A virtual environment is recommended
- A Gemini API key is optional; without one, local fallback recommendations are used

## Installation

From the project root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows, PowerShell may require permission to run the activation script. The application can also be run without activating the environment by using `.venv\Scripts\python.exe` and `.venv\Scripts\uvicorn.exe` directly.

## Configuration

Create a `.env` file in the project root when you need to override defaults:

```dotenv
APP_NAME=PocketSmart AI
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=sqlite:///./pocketsmart.db
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.8-flash
ACCESS_TOKEN_EXPIRE_MINUTES=120
MAX_UPLOAD_MB=5
```

Environment variable names are case-insensitive. The defaults are defined in `app/database.py`. Keep `SECRET_KEY` private in any deployed environment.

## Running the application

Start the development server from the project root:

```powershell
uvicorn app.main:app --reload
```

Open these URLs in a browser:

- Web application: `http://127.0.0.1:8000/`
- Swagger API documentation: `http://127.0.0.1:8000/docs`
- ReDoc API documentation: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

The database tables are created automatically when the application starts. The default SQLite database file is `pocketsmart.db` in the project root.

## Web pages

| Path | Purpose |
| --- | --- |
| `/` | Home page |
| `/register` | Registration page |
| `/login` | Login page |
| `/planner/home` | Home interior planner |
| `/planner/party` | Party planner |
| `/planner/jewelry` | Jewelry planner |
| `/history` | Authenticated recommendation history |
| `/health` | Service health check |

## API

All API endpoints use the `/api` prefix. Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

### Authentication

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/register` | Create an account and return a JWT |
| `POST` | `/api/login` | Authenticate and return a JWT |
| `POST` | `/api/logout` | Client-side logout acknowledgement |
| `GET` | `/api/session-info` | Return the current user |
| `GET` | `/api/session-data` | Return user data and planner access |

Registration example:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/register `
	-H "Content-Type: application/json" `
	-d '{"name":"Asha","email":"asha@example.com","password":"secret123"}'
```

The password must contain 6 to 72 characters. Save the `access_token` from the response and use it for protected requests.

### Planner endpoints

| Method | Endpoint | Body | Description |
| --- | --- | --- | --- |
| `POST` | `/api/generate-home` | JSON | Generate a room and interior plan |
| `POST` | `/api/generate-party` | JSON | Generate an event and party plan |
| `POST` | `/api/generate-jewelry` | Multipart form | Generate jewelry recommendations |

Home request:

```json
{
	"budget": 50000,
	"rooms": ["Living Room"],
	"style": "Modern",
	"requirements": "Storage"
}
```

Party request:

```json
{
	"budget": 30000,
	"guests": 25,
	"event_type": "Birthday",
	"venue": "Home",
	"requirements": "Vegetarian food"
}
```

Jewelry requests use multipart fields: `budget`, `occasion`, `style`, and optional `outfit_description`. An optional `outfit_image` may be uploaded as JPG, PNG, or WEBP. The maximum file size is controlled by `MAX_UPLOAD_MB` and defaults to 5 MB.

Each planner response contains `planner_type`, `budget`, `summary`, `allocations`, `recommendations`, `tips`, and `source`. The `source` value identifies whether the response came from Gemini or the local fallback.

### Recommendation history

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/history` | List the authenticated user’s saved recommendations |
| `GET` | `/api/recommendations-details/{recommendation_id}` | Retrieve one saved recommendation |

Planner results are saved automatically after successful generation. Users can only access their own history.

## Testing

Run the test suite from the project root:

```powershell
pytest
```

The API tests use a separate SQLite database, set a test secret, and disable Gemini so they exercise the deterministic local fallback.

## Project structure

```text
pocketsmart-ai/
├── app/
│   ├── main.py                 # FastAPI app and HTML routes
│   ├── database.py             # Settings, engine, and database sessions
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Request and response validation
│   ├── auth.py                 # Password hashing and JWT creation
│   ├── dependencies.py         # Authenticated-user dependencies
│   ├── ai/                     # Gemini client and prompts
│   ├── services/               # Recommendation and fallback logic
│   ├── routes/                 # Authentication, planner, and history APIs
│   ├── templates/              # Jinja2 HTML templates
│   └── static/                 # CSS and browser JavaScript
├── tests/                      # Pytest API tests
├── uploads/                    # Runtime upload directory
├── requirements.txt
└── README.md
```

## Deployment notes

Before deploying, set a strong `SECRET_KEY`, configure a production database, restrict CORS origins in `app/main.py`, and keep `.env` and API credentials out of version control. The built-in logout endpoint does not revoke JWTs; the client must remove its stored token.