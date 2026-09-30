from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class MarketData(Base):
    __tablename__ = "market_data"

    market_data_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    security_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("securities.security_id"),
        nullable=False,
        index=True,
    )

    price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    price_open: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    high: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    low: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    close: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    volume: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    market_cap: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    high_52: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    low_52: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    currency: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    data_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    security = relationship(
        "Security",
        back_populates="market_data",
    )
