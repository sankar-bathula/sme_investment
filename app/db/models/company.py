from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    company_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    script_name: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
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
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    securities = relationship(
        "Security",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    shareholdings = relationship(
        "Shareholding",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    corporate_actions = relationship(
        "CorporateAction",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="company",
        cascade="all, delete-orphan",
    )