
from fastapi import BackgroundTasks, FastAPI
from fastapi.concurrency import asynccontextmanager

from models.db import check_connection, close_db
from schemas.schemas import RequestData
from .scrapper import Scrapper

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Statring up...")
    await check_connection()
    print("DB connection is successful!")
    yield
    print("Shutdown..")
    await close_db()

app = FastAPI(lifespan=lifespan)

def scrape_and_send_email(browser: str, url: str):
    try:
        scrap = Scrapper()
        scrap.set_driver(browser, url)
        data = scrap.check_original_price(2)
        scrap.send_email(data[0], data[1])
    except Exception as e:
        print(f"Error during scraping or email sending: {e}")


@app.post("/show")
async def scrape_price(data_for_request: RequestData, background_tasks: BackgroundTasks):
    browser = data_for_request.browser
    url = data_for_request.url
    
    background_tasks.add_task(scrape_and_send_email, browser, url)

    return {"status": "Processing", "message": "Scraping and email sending started."}




