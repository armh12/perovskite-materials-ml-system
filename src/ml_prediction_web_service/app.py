from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ml_prediction_web_service.api.prediction_router import router as predictions_router

app = FastAPI(title="Perovskite ML Intelligence API")

BASE_DIR = Path(__file__).resolve().parent

static_dir_path = BASE_DIR / "api" / "static"
app.mount("/static", StaticFiles(directory=static_dir_path), name="static")

templates_path = BASE_DIR / "api" / "templates"
templates = Jinja2Templates(directory=templates_path)

app.include_router(predictions_router)

@app.get("/", include_in_schema=False)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})