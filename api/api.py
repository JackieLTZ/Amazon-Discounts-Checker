from fastapi import BackgroundTasks, FastAPI
from fastapi.concurrency import asynccontextmanager
from schemas.schemas import RequestData
from .scrapper import Scrapper
from models.db import DbManager
import logging

database_manager = DbManager()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    await database_manager.check_connection()
    await database_manager.create_tables()
    yield
    logger.info("Shutdown..")
    await database_manager.close_connection()

app = FastAPI(lifespan=lifespan)

async def scrape_and_send_email(browser: str, url: str):
    async with database_manager.get_db() as session:
        try:
            scrap = Scrapper()
            scrap.set_driver(browser, url)
            data = scrap.check_original_price(2)
            await database_manager.save_price(data, session)
            scrap.send_email(data)
        except Exception as e:
            logger.error(f"Error during scraping or email sending: {e}")

@app.post("/scrape")
async def scrape_price(data_for_request: RequestData, background_tasks: BackgroundTasks):
    browser = data_for_request.browser
    url = data_for_request.url
    
    background_tasks.add_task(scrape_and_send_email, browser, url)
    return {"status": "Processing", "message": "Scraping and email sending started."}

@app.get("/show")
async def show_prices():
    cars = await database_manager.show_prices()

    return cars

