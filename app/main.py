from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routes.urls import router as urls_router

app = FastAPI(
    title="IG URL Collector API",
    version="0.1.0"
)

# Static files (CSS / JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

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
