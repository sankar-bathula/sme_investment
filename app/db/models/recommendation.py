from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id: Mapped[int] = mapped_column(
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

    recommendation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    recommendation_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
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
        back_populates="recommendations",
    )

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "recommendation_date",
            name="uq_recommendation_company_date",
        ),
    )
