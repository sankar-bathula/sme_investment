from datetime import datetime, date
from sqlalchemy import (BigInteger,Date,DateTime,Float,ForeignKey,String,Text,)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    company_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    script_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    industry: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    sub_industry: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    segment: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    market_data = relationship(
        "MarketData",
        back_populates="company",
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="company",
    )


class MarketData(Base):
    __tablename__ = "market_data"

    market_data_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.company_id"),
        nullable=False,
        index=True,
    )

    price: Mapped[float | None] = mapped_column(Float)
    price_open: Mapped[float | None] = mapped_column(Float)
    high: Mapped[float | None] = mapped_column(Float)
    low: Mapped[float | None] = mapped_column(Float)
    volume: Mapped[float | None] = mapped_column(Float)
    market_cap: Mapped[float | None] = mapped_column(Float)
    pe: Mapped[float | None] = mapped_column(Float)
    eps: Mapped[float | None] = mapped_column(Float)
    high_52: Mapped[float | None] = mapped_column(Float)
    low_52: Mapped[float | None] = mapped_column(Float)
    income_dividend: Mapped[float | None] = mapped_column(Float)

    currency: Mapped[str | None] = mapped_column(
        String(20)
    )

    data_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    company = relationship(
        "Company",
        back_populates="market_data",
    )


class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.company_id"),
        nullable=False,
    )

    recommendation: Mapped[str | None] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    company = relationship(
        "Company",
        back_populates="recommendations",
    )