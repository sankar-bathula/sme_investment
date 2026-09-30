from app.db.database import SessionLocal
from app.screener.stock_screener import StockScreener


def main():
    db = SessionLocal()

    try:
        screener = StockScreener(db)

        stocks = screener.screen(
            max_market_cap=5000,
            max_pe=20,
            min_eps=0,
            # min_promoter_holding=35,
            # min_net_profit_margin=5,
            # max_debt_equity=1,
            # min_dividend_yield=0,
        )

        print(f"\nQualified stocks: {len(stocks)}\n")

        for stock in stocks:
            print(
                f"{stock.symbol:10} "
                f"{stock.name[:30]:30} "
                f"Price={stock.price} "
                f"MarketCap={stock.market_cap} "
                f"PE={stock.pe} "
                f"EPS={stock.eps}"
            )

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
