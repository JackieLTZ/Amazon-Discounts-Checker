import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/am"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as session:
        yield session

async def close_db():
    async with SessionLocal() as session:
        await session.close()

async def check_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "success", "message": "Database connection is successful!"}
    except Exception as e:
        print(f"Startup failed: {e}")
        sys.exit(1)
        return {"status": "failed", "message": "Connection failed!"}


