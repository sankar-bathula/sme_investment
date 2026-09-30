from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    Float,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Shareholding(Base):
    __tablename__ = "shareholdings"

    shareholding_id: Mapped[int] = mapped_column(
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

    period_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    promoter_holding: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    fii_holding: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    dii_holding: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    public_holding: Mapped[float | None] = mapped_column(
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
        back_populates="shareholdings",
    )

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "period_date",
            name="uq_shareholdings_company_period",
        ),
    )