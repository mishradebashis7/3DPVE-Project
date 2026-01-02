import pandas as pd

class PortfolioManager:
    def __init__(self, portfolio_df):
        """
        Manages the collection of valued patents.
        """
        self.portfolio = portfolio_df

    def get_total_value(self):
        return self.portfolio['Estimated_Value'].sum()

    def get_top_assets(self, n=5):
        return self.portfolio.nlargest(n, 'Estimated_Value')

    def get_risk_profile(self):
        # returns simple stats
        return self.portfolio['Total_Score'].describe()