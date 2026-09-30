from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    Float,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class FinancialMetrics(Base):
    __tablename__ = "financial_metrics"

    financial_metric_id: Mapped[int] = mapped_column(
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

    financial_year: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    period_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="FY",
    )

    revenue: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    net_profit: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    eps: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    pe: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    roe: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    roce: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    net_profit_margin: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    debt_equity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    book_value: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    dividend_yield: Mapped[float | None] = mapped_column(
        Float,
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
        back_populates="financial_metrics",
    )

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "financial_year",
            "period_type",
            name="uq_financial_company_period",
        ),
    )