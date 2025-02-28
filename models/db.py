import sys
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from models.models import Base, Price
from schemas.schemas import PricesResponse

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/am"

class DbManager:
    #ADD ENCAPSULATION !!!
    def __init__(self, database_url: str = DATABASE_URL):
        self.engine = create_async_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_db(self):
        async with self.SessionLocal() as session:
            yield session

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def check_connection(self):
        try:
            async with self.engine.connect() as conn:
                async with conn.begin():
                    await conn.execute(text("SELECT 1"))
            print("Database connection is successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise RuntimeError("Database connection failed.") from e

    async def close_connection(self):
        await self.engine.dispose()
        print("Database connection closed.")


    async def save_price(self, response: PricesResponse, db: AsyncSession):
        new_price = Price(
            original_price=response.original_price, 
            sale_price=response.sale_price, 
            timestamp=response.timestamp
        )

        db.add(new_price)
        await db.commit()
        await db.refresh(new_price)

        return PricesResponse.model_validate(new_price)
    
    async def show_prices(self, db: AsyncSession):
        result = await db.execute(select(Price).order_by(Price.ID))
        prices = result.scalars().all()

        price_list = [PricesResponse.model_validate(price) for price in prices]

        return price_list



        



