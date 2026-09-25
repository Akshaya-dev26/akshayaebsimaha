from pathlib import Path

from fastapi import (
FastAPI,
Request,
)

from fastapi.responses import (
HTMLResponse,
RedirectResponse,
)

from fastapi.staticfiles import StaticFiles

from fastapi.templating import (
Jinja2Templates,
)

from fastapi.middleware.cors import (
CORSMiddleware,
)

from .database import (
Base,
engine,
settings,
)

from .routes import (
auth,
planners,
history,
)

BASE_DIR = Path(__file__).resolve().parent

UPLOADS_DIR = (
BASE_DIR.parent / "uploads"
)

UPLOADS_DIR.mkdir(
exist_ok=True
)
Base.metadata.create_all(
    bind=engine
)
app = FastAPI(
title=settings.app_name,
version="1.0.0",
)

app.add_middleware(
CORSMiddleware,

allow_origins=["*"],

allow_credentials=True,

allow_methods=["*"],

allow_headers=["*"],


)

app.mount(
"/static",
StaticFiles(
directory=BASE_DIR / "static"
),
name="static",
)

templates = Jinja2Templates(
directory=BASE_DIR / "templates"
)

app.include_router(
auth.router,
prefix="/api",
)

app.include_router(
planners.router,
prefix="/api",
)

app.include_router(
history.router,
prefix="/api",
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(
        bind=engine
    )


@app.get(
    "/",
    response_class=HTMLResponse,
)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get(
    "/login",
    response_class=HTMLResponse,
)
def login_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


@app.get(
    "/register",
    response_class=HTMLResponse,
)
def register_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )


@app.get(
    "/planner/{planner_type}",
    response_class=HTMLResponse,
)
def planner_page(
    request: Request,
    planner_type: str,
):
    if planner_type not in {
        "home",
        "party",
        "jewelry",
    }:
        return RedirectResponse("/")

    return templates.TemplateResponse(
        request=request,
        name="planner.html",
        context={
            "planner_type": planner_type,
        },
    )


@app.get(
    "/history",
    response_class=HTMLResponse,
)
def history_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
    }

