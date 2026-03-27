from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import asyncio
import logging
from .routes import router
from .services.rss import check_for_new_posts
from .config import RSS_CHECK_INTERVAL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

background_tasks = None

async def background_rss_checker():
    """Background task to check RSS feed periodically"""
    logger.info(f"Starting RSS checker with {RSS_CHECK_INTERVAL}s interval")
    while True:
        try:
            await check_for_new_posts()
        except Exception as e:
            logger.error(f"Error in background RSS checker: {e}")
        await asyncio.sleep(RSS_CHECK_INTERVAL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global background_tasks
    background_tasks = asyncio.create_task(background_rss_checker())
    logger.info("Background RSS checker started")
    yield
    # Shutdown
    background_tasks.cancel()
    logger.info("Background RSS checker stopped")

app = FastAPI(title="RSS Feed Platform", lifespan=lifespan)
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
app.state.templates = templates

