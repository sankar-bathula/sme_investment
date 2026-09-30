from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Security(Base):
    __tablename__ = "securities"

    security_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    company_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("companies.company_id"),
        nullable=False,
        index=True,
    )

    exchange: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    symbol: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    isin: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True,
    )

    security_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="EQUITY",
    )

    series: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    company = relationship(
        "Company",
        back_populates="securities",
    )

    market_data = relationship(
        "MarketData",
        back_populates="security",
        cascade="all, delete-orphan",
    )

    financial_metrics = relationship(
        "FinancialMetrics",
        back_populates="security",
        cascade="all, delete-orphan",
    )

    corporate_actions = relationship(
        "CorporateAction",
        back_populates="security",
        cascade="all, delete-orphan",
    )

    performance_metrics = relationship(
        "PerformanceMetrics",
        back_populates="security",
        cascade="all, delete-orphan",
    )