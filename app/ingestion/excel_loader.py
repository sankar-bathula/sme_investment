from datetime import date

import pandas as pd

from app.connectors.files.excel import ExcelConnector
from app.db.database import SessionLocal
from app.db.models import (
    Company,
    Security,
    MarketData,
    FinancialMetrics,
    PerformanceMetrics,
    Recommendation,
)


def clean_value(value):
    """
    Convert empty/invalid Excel values to None.
    """
    if pd.isna(value):
        return None

    if isinstance(value, str):
        value = value.strip()

        if value.upper() in (
            "#N/A",
            "N/A",
            "NA",
            "",
        ):
            return None

    return value


def to_float(value):
    """
    Safely convert Excel value to float.
    """
    value = clean_value(value)

    if value is None:
        return None

    # Handle values such as:
    # 3,44,37,191.00
    if isinstance(value, str):
        value = value.replace(",", "")
        value = value.strip()

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def load_excel(file_path: str):
    """
    Load Excel data into:

        Company
        Security
        MarketData
        FinancialMetrics
        PerformanceMetrics
        Recommendation

    Existing records are updated.
    New records are inserted.

    One Excel file is processed inside one database transaction.
    """

    connector = ExcelConnector(file_path)

    result = connector.run()

    records = result["records"]

    db = SessionLocal()

    # Counters
    inserted_companies = 0
    updated_companies = 0

    inserted_securities = 0
    updated_securities = 0

    inserted_market_data = 0
    updated_market_data = 0

    inserted_financials = 0
    updated_financials = 0

    inserted_performance = 0
    updated_performance = 0

    inserted_recommendations = 0
    updated_recommendations = 0

    data_date = date.today()

    try:

        for row in records:

            # ==========================================================
            # 1. BASIC VALUES
            # ==========================================================

            code = clean_value(
                row.get("Code")
            )

            if not code:
                continue

            script_name = clean_value(
                row.get("Script Name")
            )

            exchange = (
                clean_value(row.get("Exchange"))
                or "UNKNOWN"
            )

            # ==========================================================
            # 2. COMPANY
            # ==========================================================

            company = (
                db.query(Company)
                .filter(
                    Company.script_name == script_name
                )
                .first()
            )

            if company is None:

                company = Company(
                    name=script_name or code,
                    script_name=script_name,
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

                inserted_companies += 1

            else:

                company.name = (
                    script_name
                    or company.name
                )

                company.script_name = script_name

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

                updated_companies += 1

            # ==========================================================
            # 3. SECURITY
            # ==========================================================

            security = (
                db.query(Security)
                .filter(
                    Security.company_id
                    == company.company_id,
                    Security.symbol
                    == code,
                    Security.exchange
                    == exchange,
                )
                .first()
            )

            if security is None:

                security = Security(
                    company_id=company.company_id,
                    exchange=exchange,
                    symbol=code,
                    isin=clean_value(
                        row.get("ISIN")
                    ),
                    security_type="EQUITY",
                    series=clean_value(
                        row.get("Series")
                    ),
                )

                db.add(security)
                db.flush()

                inserted_securities += 1

            else:

                security.isin = clean_value(
                    row.get("ISIN")
                )

                security.series = clean_value(
                    row.get("Series")
                )

                updated_securities += 1

            # ==========================================================
            # 4. MARKET DATA
            # ==========================================================

            market_data = (
                db.query(MarketData)
                .filter(
                    MarketData.security_id
                    == security.security_id,
                    MarketData.data_date
                    == data_date,
                )
                .first()
            )

            if market_data is None:

                market_data = MarketData(
                    security_id=security.security_id,
                    data_date=data_date,
                )

                db.add(market_data)

                inserted_market_data += 1

            else:

                updated_market_data += 1

            market_data.price = to_float(
                row.get("price")
            )

            market_data.price_open = to_float(
                row.get("priceopen")
            )

            market_data.high = to_float(
                row.get("high")
            )

            market_data.low = to_float(
                row.get("low")
            )

            market_data.close = to_float(
                row.get("close")
            )

            market_data.volume = to_float(
                row.get("volume")
            )

            market_data.market_cap = to_float(
                row.get("marketcap")
            )

            market_data.high_52 = to_float(
                row.get("high52")
            )

            market_data.low_52 = to_float(
                row.get("low52")
            )

            market_data.currency = clean_value(
                row.get("currency")
            )

            # ==========================================================
            # 5. FINANCIAL METRICS
            # ==========================================================

            financial = (
                db.query(FinancialMetrics)
                .filter(
                    FinancialMetrics.company_id
                    == company.company_id,
                    FinancialMetrics.financial_year
                    == data_date,
                    FinancialMetrics.period_type
                    == "SNAPSHOT",
                )
                .first()
            )

            if financial is None:

                financial = FinancialMetrics(
                    company_id=company.company_id,
                    financial_year=data_date,
                    period_type="SNAPSHOT",
                )

                db.add(financial)

                inserted_financials += 1

            else:

                updated_financials += 1

            financial.pe = to_float(
                row.get("pe")
            )

            financial.eps = to_float(
                row.get("eps")
            )

            # ==========================================================
            # 6. PERFORMANCE METRICS
            # ==========================================================

            performance = (
                db.query(PerformanceMetrics)
                .filter(
                    PerformanceMetrics.security_id
                    == security.security_id,
                    PerformanceMetrics.data_date
                    == data_date,
                )
                .first()
            )

            if performance is None:

                performance = PerformanceMetrics(
                    security_id=security.security_id,
                    data_date=data_date,
                )

                db.add(performance)

                inserted_performance += 1

            else:

                updated_performance += 1

            performance.return_7d = to_float(
                row.get("7 Days")
            )

            performance.return_15d = to_float(
                row.get("15 Days")
            )

            performance.return_30d = to_float(
                row.get("30 day")
            )

            performance.return_60d = to_float(
                row.get("60 day")
            )

            performance.return_90d = to_float(
                row.get("90 Day")
            )

            performance.return_180d = to_float(
                row.get("180 Day")
            )

            performance.return_365d = to_float(
                row.get("365 day")
            )

            # ==========================================================
            # 7. RECOMMENDATION
            # ==========================================================

            recommendation_value = clean_value(
                row.get("Recommendation")
            )

            if recommendation_value:

                recommendation = (
                    db.query(Recommendation)
                    .filter(
                        Recommendation.company_id
                        == company.company_id,
                        Recommendation.recommendation_date
                        == data_date,
                    )
                    .first()
                )

                if recommendation is None:

                    recommendation = Recommendation(
                        company_id=company.company_id,
                        recommendation=(
                            str(
                                recommendation_value
                            )
                        ),
                        recommendation_date=data_date,
                    )

                    db.add(recommendation)

                    inserted_recommendations += 1

                else:

                    recommendation.recommendation = (
                        str(
                            recommendation_value
                        )
                    )

                    updated_recommendations += 1

        # ==============================================================
        # COMMIT
        # ==============================================================

        db.commit()

        return {
            "status": "success",
            "processed_rows": len(records),

            "inserted_companies": inserted_companies,
            "updated_companies": updated_companies,

            "inserted_securities": inserted_securities,
            "updated_securities": updated_securities,

            "inserted_market_data": inserted_market_data,
            "updated_market_data": updated_market_data,

            "inserted_financials": inserted_financials,
            "updated_financials": updated_financials,

            "inserted_performance": inserted_performance,
            "updated_performance": updated_performance,

            "inserted_recommendations": (
                inserted_recommendations
            ),
            "updated_recommendations": (
                updated_recommendations
            ),
        }

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()