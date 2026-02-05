from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates_path = "./templates"
templates = Jinja2Templates(directory=templates_path)
router = APIRouter(prefix="/ui", tags=["Frontend"])


@router.get("/admin", response_class=HTMLResponse)
async def get_prediction_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
