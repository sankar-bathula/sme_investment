from sqlalchemy import select

from app.db.models import (
    Company,
    MarketData,
    FinancialMetrics,
)


class StockScreener:

    def __init__(self, db):
        self.db = db

    def screen(
        self,
        max_market_cap: float = 5000,
        min_promoter_holding: float = 35,
        min_net_profit_margin: float = 5,
        max_debt_equity: float = 1,
        min_dividend_yield: float = 0,
    ):
        stmt = (
            select(
                Company.code,
                Company.script_name,
                Company.industry,
                MarketData.price,
                MarketData.market_cap,
                MarketData.pe,
                MarketData.eps,
                FinancialMetrics.promoter_holding,
                FinancialMetrics.net_profit_margin,
                FinancialMetrics.debt_equity,
                FinancialMetrics.dividend_yield,
            )
            .join(
                MarketData,
                Company.company_id == MarketData.company_id,
            )
            .join(
                FinancialMetrics,
                Company.company_id == FinancialMetrics.company_id,
            )
            .where(
                MarketData.market_cap < max_market_cap,
                FinancialMetrics.promoter_holding >= min_promoter_holding,
                FinancialMetrics.net_profit_margin > min_net_profit_margin,
                FinancialMetrics.debt_equity < max_debt_equity,
                FinancialMetrics.dividend_yield >= min_dividend_yield,
            )
        )

        return self.db.execute(stmt).mappings().all()