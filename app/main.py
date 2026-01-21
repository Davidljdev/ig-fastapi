from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.db import Base, engine
from app.routes.urls import router as urls_router
import sys
from pathlib import Path

# Asegura que Python vea la raíz del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

app = FastAPI(
    title="IG URL Collector API",
    version="0.1.0"
)

# Static files (CSS / JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# API routes
#app.include_router(urls_router, prefix="/urls", tags=["urls"])
app.include_router(urls_router, prefix="/urls")
