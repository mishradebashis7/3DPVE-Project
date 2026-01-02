import pandas as pd
from src.scoring_engine import PatentValueEngine

class PortfolioManager:
    """
    Handles batch processing of multiple patents.
    Connects Data (CSV/DataFrame) -> Scoring Engine -> Results.
    """
    
    def __init__(self, engine=None):
        # Use existing engine or create new one
        self.engine = engine if engine else PatentValueEngine()

    def process_portfolio(self, df):
        """
        Applies the scoring logic to an entire DataFrame.
        Expected columns: legal_status, family_size, years_active, tech_diversity
        """
        results = []
        
        print(f"Processing {len(df)} patents with mode: {self.engine.mode}...")
        
        for index, row in df.iterrows():
            # 1. Calculate Individual Scores
            s_leg = self.engine.calculate_legal_score(row['legal_status'])
            s_eco = self.engine.calculate_economic_score(row['family_size'], row['years_active'])
            s_tech = self.engine.calculate_tech_score(row['tech_diversity'])
            
            # 2. Composite Score
            v_cp = self.engine.get_composite_score(s_leg, s_eco, s_tech)
            
            # 3. Store
            results.append({
                'patent_id': row['patent_id'],
                'legal_score': round(s_leg, 2),
                'eco_score': round(s_eco, 2),
                'tech_score': round(s_tech, 2),
                'final_value': round(v_cp, 2)
            })
            
        # Return a new DataFrame with scores joined
        scores_df = pd.DataFrame(results)
        return pd.merge(df, scores_df, on='patent_id')

    def identify_top_assets(self, scored_df, top_n=5):
        """Returns the highest valued patents."""
        return scored_df.sort_values(by='final_value', ascending=False).head(top_n)

    def identify_risks(self, scored_df):
        """Returns patents with Zero value (Revoked/Lapsed)."""
        return scored_df[scored_df['final_value'] == 0]