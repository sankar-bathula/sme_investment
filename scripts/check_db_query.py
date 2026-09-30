from sqlalchemy import text

from app.db.database import engine


def main():

    print("=" * 80)
    print("DATABASE CHECK")
    print("=" * 80)

    try:
        with engine.connect() as conn:

            # ----------------------------------------
            # 1. Check database connection
            # ----------------------------------------
            result = conn.execute(
                text("SELECT current_database(), current_user;")
            )

            row = result.fetchone()

            print()
            print("Database :", row[0])
            print("User     :", row[1])

            # ----------------------------------------
            # 2. Table counts
            # ----------------------------------------
            print()
            print("=" * 80)
            print("TABLE COUNTS")
            print("=" * 80)

            result = conn.execute(
                text("""
                    SELECT
                        (SELECT COUNT(*) FROM companies) AS companies,
                        (SELECT COUNT(*) FROM securities) AS securities,
                        (SELECT COUNT(*) FROM market_data) AS market_data,
                        (SELECT COUNT(*) FROM financial_metrics) AS financial_metrics,
                        (SELECT COUNT(*) FROM performance_metrics) AS performance_metrics,
                        (SELECT COUNT(*) FROM recommendations) AS recommendations,
                        (SELECT COUNT(*) FROM shareholding) AS shareholding;
                """)
            )

            row = result.fetchone()

            for column, value in zip(result.keys(), row):
                print(f"{column:<25}: {value}")

            # ----------------------------------------
            # 3. Actual stock data
            # ----------------------------------------
            print()
            print("=" * 80)
            print("STOCK DATA")
            print("=" * 80)

            result = conn.execute(
                text("""
                    SELECT
                        s.symbol,
                        m.price,
                        m.market_cap,
                        f.pe,
                        f.eps
                    FROM securities s
                    JOIN market_data m
                        ON m.security_id = s.security_id
                    LEFT JOIN financial_metrics f
                        ON f.company_id = s.company_id
                    ORDER BY m.market_cap ASC NULLS LAST
                    LIMIT 20;
                """)
            )

            rows = result.fetchall()

            if not rows:
                print("No stock data found.")
            else:
                print(
                    f"{'SYMBOL':<12}"
                    f"{'PRICE':>12}"
                    f"{'MARKET CAP':>18}"
                    f"{'PE':>12}"
                    f"{'EPS':>12}"
                )

                print("-" * 70)

                for row in rows:
                    print(
                        f"{str(row[0]):<12}"
                        f"{str(row[1]):>12}"
                        f"{str(row[2]):>18}"
                        f"{str(row[3]):>12}"
                        f"{str(row[4]):>12}"
                    )

            # ----------------------------------------
            # 4. Screener diagnostic
            # ----------------------------------------
            print()
            print("=" * 80)
            print("SCREENER DIAGNOSTIC")
            print("=" * 80)

            result = conn.execute(
                text("""
                    SELECT
                        COUNT(*) AS total,

                        COUNT(*) FILTER (
                            WHERE m.market_cap <= 5000
                        ) AS market_cap_pass,

                        COUNT(*) FILTER (
                            WHERE f.pe <= 20
                        ) AS pe_pass,

                        COUNT(*) FILTER (
                            WHERE f.eps >= 0
                        ) AS eps_pass,

                        COUNT(*) FILTER (
                            WHERE m.market_cap <= 5000
                              AND f.pe <= 20
                        ) AS market_cap_pe_pass,

                        COUNT(*) FILTER (
                            WHERE m.market_cap <= 5000
                              AND f.pe <= 20
                              AND f.eps >= 0
                        ) AS all_filters_pass

                    FROM securities s

                    JOIN market_data m
                        ON m.security_id = s.security_id

                    LEFT JOIN financial_metrics f
                        ON f.company_id = s.company_id;
                """)
            )

            row = result.fetchone()

            print(f"Total records       : {row[0]}")
            print(f"Market cap <= 5000  : {row[1]}")
            print(f"PE <= 20            : {row[2]}")
            print(f"EPS >= 0            : {row[3]}")
            print(f"Market cap + PE     : {row[4]}")
            print(f"ALL FILTERS         : {row[5]}")

            # ----------------------------------------
            # 5. Qualified stocks
            # ----------------------------------------
            print()
            print("=" * 80)
            print("QUALIFIED STOCKS")
            print("=" * 80)

            result = conn.execute(
                text("""
                    SELECT
                        s.symbol,
                        m.price,
                        m.market_cap,
                        f.pe,
                        f.eps
                    FROM securities s
                    JOIN market_data m
                        ON m.security_id = s.security_id
                    JOIN financial_metrics f
                        ON f.company_id = s.company_id
                    WHERE m.market_cap <= 5000
                      AND f.pe <= 20
                      AND f.eps >= 0
                    ORDER BY m.market_cap ASC
                    LIMIT 50;
                """)
            )

            rows = result.fetchall()

            if not rows:
                print("No qualified stocks.")
            else:
                for row in rows:
                    print(
                        f"{row[0]:<12} "
                        f"Price={row[1]} "
                        f"MarketCap={row[2]} "
                        f"PE={row[3]} "
                        f"EPS={row[4]}"
                    )

    except Exception as exc:
        print()
        print("=" * 80)
        print("ERROR")
        print("=" * 80)
        print(type(exc).__name__)
        print(exc)


if __name__ == "__main__":
    main()
