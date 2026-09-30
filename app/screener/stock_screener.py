from sqlalchemy.orm import Session

from app.db.models import (
    Company,
    Security,
    MarketData,
    FinancialMetrics,
    Shareholding,
    
)


class StockScreener:

    def __init__(self, db: Session):
        self.db = db

    def screen(
        self,
        max_market_cap: float | None = None,
        max_pe: float | None = None,
        min_eps: float | None = None,
        min_dividend_yield: float | None = None,
        min_promoter_holding: float | None = None,
        min_net_profit_margin: float | None = None,
        max_debt_equity : float | None = None
    ):
        """
        Screen stocks using:

        - Market capitalization
        - PE ratio
        - EPS
        - Dividend yield
        - Promoter holding
        - Net profit margin
        - Debt-to-equity ratio

        Returns matching companies/securities.
        """

        query = (
            self.db.query(
                Company.company_id,
                Company.name,
                Security.symbol,
                MarketData.price,
                MarketData.market_cap,
                FinancialMetrics.pe,
                FinancialMetrics.eps,
                FinancialMetrics.dividend_yield,
                FinancialMetrics.net_profit_margin,
                FinancialMetrics.debt_equity,
                Shareholding.promoter_holding,
            )
            .join(
                Security,
                Security.company_id == Company.company_id,
            )
            .join(
                MarketData,
                MarketData.security_id == Security.security_id,
            )
            .join(
                FinancialMetrics,
                FinancialMetrics.security_id == Security.security_id,
            )
            .outerjoin(
                Shareholding,
                Shareholding.company_id == Company.company_id,
            )
        )

        # --------------------------------
        # Market Cap
        # --------------------------------
        if max_market_cap is not None:
            query = query.filter(
                MarketData.market_cap <= max_market_cap
            )

        # --------------------------------
        # PE
        # --------------------------------
        if max_pe is not None:
            query = query.filter(
                FinancialMetrics.pe <= max_pe
            )

        # --------------------------------
        # EPS
        # --------------------------------
        if min_eps is not None:
            query = query.filter(
                FinancialMetrics.eps >= min_eps
            )

        # --------------------------------
        # Dividend Yield
        # --------------------------------
        if min_dividend_yield is not None:
            query = query.filter(
                FinancialMetrics.dividend_yield >= min_dividend_yield
            )

        # --------------------------------
        # Promoter Holding
        # --------------------------------
        if min_promoter_holding is not None:
            query = query.filter(
                Shareholding.promoter_holding >= min_promoter_holding
            )

        if min_net_profit_margin is not None:
            query = query.filter(
                FinancialMetrics.net_profit_margin >= min_net_profit_margin
            )

        if max_debt_equity is not None:
            query = query.filter(
                FinancialMetrics.debt_equity <= max_debt_equity
            )

        return query.all()