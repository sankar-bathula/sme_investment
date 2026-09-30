from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class CorporateAction(Base):
    __tablename__ = "corporate_actions"

    corporate_action_id: Mapped[int] = mapped_column(
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

    security_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("securities.security_id"),
        nullable=True,
        index=True,
    )

    action_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    ex_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        index=True,
    )

    record_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    payment_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    ratio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    amount: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    currency: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
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
        back_populates="corporate_actions",
    )

    security = relationship(
        "Security",
        back_populates="corporate_actions",
    )