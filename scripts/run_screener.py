# from app.db.database import SessionLocal
# from app.screener.stock_screener import StockScreener


# def main():
#     db = SessionLocal()

#     try:
#         screener = StockScreener(db)

#         stocks = screener.screen(
#             max_market_cap=5000,
#             max_pe=20,
#             min_eps=0,
#             # min_promoter_holding=35,
#             # min_net_profit_margin=5,
#             # max_debt_equity=1,
#             # min_dividend_yield=0,
#         )

#         print(f"\nQualified stocks: {len(stocks)}\n")

#         for stock in stocks:
#             print(
#                 f"{stock.symbol:10} "
#                 f"{stock.name[:30]:30} "
#                 f"Price={stock.price} "
#                 f"MarketCap={stock.market_cap} "
#                 f"PE={stock.pe} "
#                 f"EPS={stock.eps}"
#             )

#     except Exception as e:
#         print(f"Error occurred: {e}")

#     finally:
#         db.close()


# if __name__ == "__main__":
#     main()



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

        # Sort by fundamentals
        stocks = sorted(
            stocks,
            key=lambda stock: (
                stock.eps or 0,
                stock.promoter_holding or 0,
                stock.net_profit_margin or 0,
                -(stock.pe or 999),
            ),
            reverse=True,
        )

        # Take only Top 10
        top_10 = stocks[:10]

        print(f"\nQualified stocks: {len(stocks)}")
        print(f"Top 10 stocks:\n")

        print(
            f"{'Rank':<5}"
            f"{'Symbol':<12}"
            f"{'Name':<30}"
            f"{'Price':>12}"
            f"{'MarketCap':>14}"
            f"{'PE':>10}"
            f"{'EPS':>10}"
            f"{'Promoter':>12}"
            f"{'NPM':>10}"
            f"{'D/E':>10}"
        )

        print("-" * 135)

        for rank, stock in enumerate(top_10, start=1):
            print(
                f"{rank:<5}"
                f"{stock.symbol:<12}"
                f"{stock.name[:28]:<30}"
                f"{stock.price or 0:>12.2f}"
                f"{stock.market_cap or 0:>14.2f}"
                f"{stock.pe or 0:>10.2f}"
                f"{stock.eps or 0:>10.2f}"
                f"{stock.promoter_holding or 0:>11.2f}%"
                f"{stock.net_profit_margin or 0:>9.2f}%"
                f"{stock.debt_equity or 0:>10.2f}"
            )

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()