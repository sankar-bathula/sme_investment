from app.db.database import Base, engine

# Import all models so SQLAlchemy registers them
from app.db.models import (
    Company,
    Security,
    MarketData,
    FinancialMetrics,
    Shareholding,
    CorporateAction,
)


def create_tables() -> None:
    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()
