from sqlalchemy import DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

class Base(DeclarativeBase):
    pass  

class Price(Base):
    __tablename__ = "product_prices"

    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_price: Mapped[str] = mapped_column(nullable=False)
    sale_price: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))