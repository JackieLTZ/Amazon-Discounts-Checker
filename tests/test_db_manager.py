import pytest
import pytest_asyncio
from schemas.schemas import PricesResponse
from models.db import DbManager
from datetime import datetime

# Define a test database URL (use an in-memory database for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def db_manager():
    manager = DbManager(TEST_DATABASE_URL)
    await manager.create_tables()  # Create tables before testing
    yield manager

    await manager.close_connection()


@pytest.mark.asyncio
async def test_check_connection(db_manager: DbManager):
    await db_manager.check_connection()


@pytest.mark.asyncio
async def test_save_price(db_manager: DbManager):
    sample_response = PricesResponse(
        original_price="20.99",
        discount_price="15.99",
        timestamp=datetime.utcnow(),
    )

    async with db_manager.get_db() as session:
        saved_price = await db_manager.save_price(sample_response, session)

    assert saved_price.original_price == sample_response.original_price
    assert saved_price.discount_price == sample_response.discount_price


@pytest.mark.asyncio
async def test_show_prices(db_manager: DbManager):
    sample_response = PricesResponse(
        original_price="50.99",
        discount_price="45.99",
        timestamp=datetime.utcnow(),
    )

    async with db_manager.get_db() as session:
        await db_manager.save_price(sample_response, session)

    # Fetch the prices
    prices = await db_manager.show_prices()

    assert len(prices) > 0
    assert prices[0].original_price == sample_response.original_price
    assert prices[0].discount_price == sample_response.discount_price
