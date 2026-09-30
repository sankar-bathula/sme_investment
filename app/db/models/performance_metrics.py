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


class PerformanceMetrics(Base):
    __tablename__ = "performance_metrics"

    performance_id: Mapped[int] = mapped_column(
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

    data_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    # Performance / return metrics
    return_7d: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    return_15d: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    return_30d: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    return_60d: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    return_90d: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    return_180d: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    return_365d: Mapped[float | None] = mapped_column(
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

    # Relationship
    security = relationship(
        "Security",
        back_populates="performance_metrics",
    )

    # One performance snapshot per security per date
    __table_args__ = (
        UniqueConstraint(
            "security_id",
            "data_date",
            name="uq_performance_security_date",
        ),
    )
