from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from .services.rss import fetch_feeds

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    feeds = await fetch_feeds()
    return request.app.state.templates.TemplateResponse("index.html", {"request": request, "feeds": feeds})

