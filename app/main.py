from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
from . import models, database

from .routes.auth import auth_router
from .routes.home import home_router
from .routes.config import config_router

from .utils.startup import lifespan

app = FastAPI(lifespan=lifespan)

models.Base.metadata.create_all(bind=database.engine)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

app.add_middleware(SessionMiddleware, secret_key="dkjsf0ffdfjf3")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.state.templates = Jinja2Templates(directory=TEMPLATE_DIR)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth")
app.include_router(home_router, prefix="/home")
app.include_router(config_router, prefix="/config")

@app.get("/")
def Main(request: Request):
    return RedirectResponse("/auth/login", status_code=303)




