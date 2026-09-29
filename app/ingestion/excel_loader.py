from datetime import date

import pandas as pd

from app.connectors.files.excel import ExcelConnector
from app.db.database import SessionLocal
from app.db.models import (
    Company,
    MarketData,
    Recommendation,
)


def clean_value(value):
    """
    Convert Excel #N/A, NaN and empty values to None.
    """

    if pd.isna(value):
        return None

    if isinstance(value, str):
        value = value.strip()

        if value in ("#N/A", "", "N/A", "NA"):
            return None

    return value


def to_float(value):
    value = clean_value(value)

    if value is None:
        return None

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def load_excel(file_path: str):

    connector = ExcelConnector(file_path)

    result = connector.run()

    records = result["records"]

    db = SessionLocal()

    inserted = 0
    updated = 0

    try:

        for row in records:

            code = clean_value(row.get("Code"))

            if not code:
                continue

            # -------------------------------------------------
            # COMPANY
            # -------------------------------------------------

            company = (
                db.query(Company)
                .filter(Company.code == code)
                .first()
            )

            if company is None:

                company = Company(
                    script_name=clean_value(
                        row.get("Script Name")
                    ),
                    code=code,
                    industry=clean_value(
                        row.get("Industry")
                    ),
                    sub_industry=clean_value(
                        row.get("Sub Industry")
                    ),
                    category=clean_value(
                        row.get("Category")
                    ),
                    segment=clean_value(
                        row.get("Segment")
                    ),
                )

                db.add(company)
                db.flush()

                inserted += 1

            else:

                company.script_name = clean_value(
                    row.get("Script Name")
                )

                company.industry = clean_value(
                    row.get("Industry")
                )

                company.sub_industry = clean_value(
                    row.get("Sub Industry")
                )

                company.category = clean_value(
                    row.get("Category")
                )

                company.segment = clean_value(
                    row.get("Segment")
                )

                updated += 1

            # -------------------------------------------------
            # MARKET DATA
            # -------------------------------------------------

            market_data = MarketData(
                company_id=company.company_id,

                price=to_float(row.get("price")),

                price_open=to_float(
                    row.get("priceopen")
                ),

                high=to_float(
                    row.get("high")
                ),

                low=to_float(
                    row.get("low")
                ),

                volume=to_float(
                    row.get("volume")
                ),

                market_cap=to_float(
                    row.get("marketcap")
                ),

                pe=to_float(
                    row.get("pe")
                ),

                eps=to_float(
                    row.get("eps")
                ),

                high_52=to_float(
                    row.get("high52")
                ),

                low_52=to_float(
                    row.get("low52")
                ),

                income_dividend=to_float(
                    row.get("incomedividend")
                ),

                currency=clean_value(
                    row.get("currency")
                ),

                data_date=date.today(),
            )

            db.add(market_data)

            # -------------------------------------------------
            # RECOMMENDATION
            # -------------------------------------------------

            recommendation = clean_value(
                row.get("Recommendation")
            )

            if recommendation:

                db.add(
                    Recommendation(
                        company_id=company.company_id,
                        recommendation=recommendation,
                    )
                )

        db.commit()

        return {
            "status": "success",
            "inserted_companies": inserted,
            "updated_companies": updated,
            "processed_rows": len(records),
        }

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()