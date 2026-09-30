from datetime import date
from pathlib import Path

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


# ============================================================
# VALUE CLEANING
# ============================================================

def clean_value(value):
    """
    Convert empty/invalid Excel values to None.

    Handles:
        None
        NaN
        #N/A
        N/A
        NA
        NULL
        NONE
        ""
    """

    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    if isinstance(value, str):
        value = value.strip()

        if value.upper() in {
            "#N/A",
            "N/A",
            "NA",
            "NULL",
            "NONE",
            "",
        }:
            return None

    return value


def clean_text(value):
    """
    Clean text fields.

    Numeric zero values such as:
        0
        0.0
        0.00

    are treated as missing text and converted to None.

    Example:
        Industry = 0
        -> Industry = NULL
    """

    value = clean_value(value)

    if value is None:
        return None

    value = str(value).strip()

    if value in {
        "0",
        "0.0",
        "0.00",
    }:
        return None

    return value


def to_float(value):
    """
    Safely convert Excel value to float.

    Handles:
        1234
        1234.50
        "1,234.50"
        "#N/A"
        "N/A"
        ""
    """

    value = clean_value(value)

    if value is None:
        return None

    if isinstance(value, str):
        value = value.replace(",", "").strip()

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


# ============================================================
# COLUMN HELPERS
# ============================================================

def normalize_column_name(name):
    """
    Normalize Excel column names.

    Examples:

        '60 Day'
        '60 day'
        ' 60 Day '
        '60  Day'

    all become:

        '60 day'
    """

    if name is None:
        return ""

    return " ".join(
        str(name).strip().lower().split()
    )


def build_column_map(records):
    """
    Build normalized Excel column mapping.

    Example:

        'Script Name' -> 'script name'
        'MarketCap'   -> 'marketcap'
    """

    if not records:
        return {}

    return {
        normalize_column_name(column): column
        for column in records[0].keys()
    }


def get_value(row, column_map, column_name):
    """
    Safely retrieve a value using a normalized column name.
    """

    normalized = normalize_column_name(column_name)

    actual_column = column_map.get(normalized)

    if actual_column is None:
        return None

    return row.get(actual_column)


# ============================================================
# MAIN LOADER
# ============================================================

def load_excel(file_path: str):
    """
    Load one Excel file into PostgreSQL.

    Tables populated:

        companies
        securities
        market_data
        financial_metrics
        performance_metrics
        recommendations

    Existing records are updated.
    New records are inserted.

    One Excel file is processed inside one database transaction.
    """

    file_path = Path(file_path)

    print()
    print("=" * 80)
    print("EXCEL INGESTION")
    print("=" * 80)
    print(f"File: {file_path}")

    # --------------------------------------------------------
    # Read Excel
    # --------------------------------------------------------

    connector = ExcelConnector(str(file_path))

    result = connector.run()

    records = result["records"]

    print(f"Rows found: {len(records)}")

    if not records:
        print("No records found.")

        return {
            "status": "success",
            "processed_rows": 0,
        }

    # --------------------------------------------------------
    # Detect columns
    # --------------------------------------------------------

    column_map = build_column_map(records)

    print()
    print("Detected columns:")

    for column in records[0].keys():
        print(f"  - {column}")

    # --------------------------------------------------------
    # Database session
    # --------------------------------------------------------

    db = SessionLocal()

    # --------------------------------------------------------
    # Counters
    # --------------------------------------------------------

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

    skipped_rows = 0

    data_date = date.today()

    # ========================================================
    # TRANSACTION
    # ========================================================

    try:

        for row_number, row in enumerate(records, start=2):

            # ==================================================
            # 1. BASIC VALUES
            # ==================================================

            code = clean_text(
                get_value(
                    row,
                    column_map,
                    "Code",
                )
            )

            if not code:
                skipped_rows += 1
                continue

            script_name = clean_text(
                get_value(
                    row,
                    column_map,
                    "Script Name",
                )
            )

            exchange = clean_text(
                get_value(
                    row,
                    column_map,
                    "Exchange",
                )
            )

            if not exchange:
                exchange = "UNKNOWN"

            # ==================================================
            # 2. COMPANY
            # ==================================================

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

                    # IMPORTANT:
                    # Use clean_text() so Industry=0 becomes NULL.
                    industry=clean_text(
                        get_value(
                            row,
                            column_map,
                            "Industry",
                        )
                    ),

                    sub_industry=clean_text(
                        get_value(
                            row,
                            column_map,
                            "Sub Industry",
                        )
                    ),

                    category=clean_text(
                        get_value(
                            row,
                            column_map,
                            "Category",
                        )
                    ),

                    segment=clean_text(
                        get_value(
                            row,
                            column_map,
                            "Segment",
                        )
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

                # IMPORTANT:
                # Always pass column_map.
                company.industry = clean_text(
                    get_value(
                        row,
                        column_map,
                        "Industry",
                    )
                )

                company.sub_industry = clean_text(
                    get_value(
                        row,
                        column_map,
                        "Sub Industry",
                    )
                )

                company.category = clean_text(
                    get_value(
                        row,
                        column_map,
                        "Category",
                    )
                )

                company.segment = clean_text(
                    get_value(
                        row,
                        column_map,
                        "Segment",
                    )
                )

                updated_companies += 1

            # ==================================================
            # 3. SECURITY
            # ==================================================

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

                    isin=clean_text(
                        get_value(
                            row,
                            column_map,
                            "ISIN",
                        )
                    ),

                    security_type="EQUITY",

                    series=clean_text(
                        get_value(
                            row,
                            column_map,
                            "Series",
                        )
                    ),
                )

                db.add(security)
                db.flush()

                inserted_securities += 1

            else:

                security.isin = clean_text(
                    get_value(
                        row,
                        column_map,
                        "ISIN",
                    )
                )

                security.series = clean_text(
                    get_value(
                        row,
                        column_map,
                        "Series",
                    )
                )

                updated_securities += 1

            # ==================================================
            # 4. MARKET DATA
            # ==================================================

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
                get_value(
                    row,
                    column_map,
                    "price",
                )
            )

            market_data.price_open = to_float(
                get_value(
                    row,
                    column_map,
                    "priceopen",
                )
            )

            market_data.high = to_float(
                get_value(
                    row,
                    column_map,
                    "high",
                )
            )

            market_data.low = to_float(
                get_value(
                    row,
                    column_map,
                    "low",
                )
            )

            market_data.close = to_float(
                get_value(
                    row,
                    column_map,
                    "close",
                )
            )

            market_data.volume = to_float(
                get_value(
                    row,
                    column_map,
                    "volume",
                )
            )

            market_data.market_cap = to_float(
                get_value(
                    row,
                    column_map,
                    "marketcap",
                )
            )

            market_data.high_52 = to_float(
                get_value(
                    row,
                    column_map,
                    "high52",
                )
            )

            market_data.low_52 = to_float(
                get_value(
                    row,
                    column_map,
                    "low52",
                )
            )

            market_data.currency = clean_text(
                get_value(
                    row,
                    column_map,
                    "currency",
                )
            )

            # ==================================================
            # 5. FINANCIAL METRICS
            # ==================================================
            #
            # IMPORTANT:
            # FinancialMetrics is SECURITY level.
            #
            # Do NOT use:
            #     company_id=company.company_id
            #
            # Use:
            #     security_id=security.security_id
            #
            # This prevents duplicate constraint errors when
            # one company has multiple securities.
            # ==================================================

            financial = (
                db.query(FinancialMetrics)
                .filter(
                    FinancialMetrics.security_id
                    == security.security_id,

                    FinancialMetrics.financial_year
                    == data_date,

                    FinancialMetrics.period_type
                    == "SNAPSHOT",
                )
                .first()
            )

            if financial is None:

                financial = FinancialMetrics(
                    security_id=security.security_id,
                    financial_year=data_date,
                    period_type="SNAPSHOT",
                )

                db.add(financial)

                inserted_financials += 1

            else:

                updated_financials += 1

            financial.pe = to_float(
                get_value(
                    row,
                    column_map,
                    "pe",
                )
            )

            financial.eps = to_float(
                get_value(
                    row,
                    column_map,
                    "eps",
                )
            )

            # ==================================================
            # 6. PERFORMANCE METRICS
            # ==================================================

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
                get_value(
                    row,
                    column_map,
                    "7 Days",
                )
            )

            performance.return_15d = to_float(
                get_value(
                    row,
                    column_map,
                    "15 Days",
                )
            )

            performance.return_30d = to_float(
                get_value(
                    row,
                    column_map,
                    "30 day",
                )
            )

            performance.return_60d = to_float(
                get_value(
                    row,
                    column_map,
                    "60 Day",
                )
            )

            performance.return_90d = to_float(
                get_value(
                    row,
                    column_map,
                    "90 Day",
                )
            )

            performance.return_180d = to_float(
                get_value(
                    row,
                    column_map,
                    "180 Day",
                )
            )

            performance.return_365d = to_float(
                get_value(
                    row,
                    column_map,
                    "365 day",
                )
            )

            # ==================================================
            # 7. RECOMMENDATION
            # ==================================================

            recommendation_value = clean_text(
                get_value(
                    row,
                    column_map,
                    "Recommendation",
                )
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

                        recommendation=str(
                            recommendation_value
                        ),

                        recommendation_date=data_date,
                    )

                    db.add(recommendation)

                    inserted_recommendations += 1

                else:

                    recommendation.recommendation = str(
                        recommendation_value
                    )

                    updated_recommendations += 1

            # ==================================================
            # DEBUG FIRST 5 ROWS
            # ==================================================

            if row_number <= 6:

                pe_value = to_float(
                    get_value(
                        row,
                        column_map,
                        "pe",
                    )
                )

                eps_value = to_float(
                    get_value(
                        row,
                        column_map,
                        "eps",
                    )
                )

                industry_value = clean_text(
                    get_value(
                        row,
                        column_map,
                        "Industry",
                    )
                )

                print(
                    f"Row {row_number}: "
                    f"{code} | "
                    f"Industry={industry_value} | "
                    f"PE={pe_value} | "
                    f"EPS={eps_value}"
                )

        # ====================================================
        # COMMIT
        # ====================================================

        db.commit()

        print()
        print("=" * 80)
        print("INGESTION COMPLETED")
        print("=" * 80)

        print(f"Processed rows           : {len(records)}")
        print(f"Skipped rows             : {skipped_rows}")

        print()
        print("Companies")
        print(f"  Inserted               : {inserted_companies}")
        print(f"  Updated                : {updated_companies}")

        print()
        print("Securities")
        print(f"  Inserted               : {inserted_securities}")
        print(f"  Updated                : {updated_securities}")

        print()
        print("Market Data")
        print(f"  Inserted               : {inserted_market_data}")
        print(f"  Updated                : {updated_market_data}")

        print()
        print("Financial Metrics")
        print(f"  Inserted               : {inserted_financials}")
        print(f"  Updated                : {updated_financials}")

        print()
        print("Performance Metrics")
        print(f"  Inserted               : {inserted_performance}")
        print(f"  Updated                : {updated_performance}")

        print()
        print("Recommendations")
        print(f"  Inserted               : {inserted_recommendations}")
        print(f"  Updated                : {updated_recommendations}")

        return {
            "status": "success",
            "processed_rows": len(records),
            "skipped_rows": skipped_rows,

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

            "inserted_recommendations": inserted_recommendations,
            "updated_recommendations": updated_recommendations,
        }

    except Exception as exc:

        db.rollback()

        print()
        print("=" * 80)
        print("INGESTION FAILED")
        print("=" * 80)

        print(f"File: {file_path}")
        print(
            f"Error: {type(exc).__name__}: {exc}"
        )

        raise

    finally:

        db.close()
