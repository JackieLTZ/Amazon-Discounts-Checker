from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select

import config
from models.models import Base, Price
from schemas.schemas import PricesResponse

DATABASE_URL = config.DATABASE_URL


class DbManager:
    def __init__(self, database_url = DATABASE_URL):
        self._engine = create_async_engine(database_url, echo=True)
        self._SessionLocal = async_sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_db(self):
        async with self._SessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()

    async def create_tables(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def check_connection(self):
        try:
            async with self._engine.connect() as conn:
                async with conn.begin():
                    await conn.execute(text("SELECT 1"))
            print("Database connection is successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise RuntimeError("Database connection failed.") from e

    async def close_connection(self):
        await self._engine.dispose()
        print("Database connection closed.")

    @staticmethod
    async def save_price(response: PricesResponse, db: AsyncSession):
        new_price = Price(
            original_price=response.original_price, 
            discount_price=response.discount_price, 
            timestamp=response.timestamp
        )

        db.add(new_price)
        await db.commit()
        await db.refresh(new_price)

        return PricesResponse.model_validate(new_price)
    
    async def show_prices(self):
        async with self._SessionLocal() as session:
            result = await session.execute(select(Price).order_by(Price.ID))
            prices = result.scalars().all()

            price_list = [PricesResponse.model_validate(price) for price in prices]

            return price_list
