import pandas as pd
import numpy as np

class ScoringEngine:
    def bulk_score(self, df):
        """
        Calculates Legal, Tech, and Market scores based on raw data.
        """
        # 1. Tech Score (Based on Forward Citations & Claims)
        df['Tech_Score'] = (df['Citations'] * 2) + (df['Claims_Count'] * 0.5)
        df['Tech_Score'] = np.clip(df['Tech_Score'], 0, 100) # Cap at 100
        
        # 2. Legal Score (Based on Remaining Life & Backward Citations)
        df['Legal_Score'] = (df['Remaining_Life'] * 4) + (df['Backward_Citations'] * 0.5)
        df['Legal_Score'] = np.clip(df['Legal_Score'], 0, 100)
        
        # 3. Market Score (Based on Family Size)
        df['Market_Score'] = df['Family_Size'] * 5
        df['Market_Score'] = np.clip(df['Market_Score'], 0, 100)
        
        # 4. Total Composite Score
        df['Total_Score'] = (df['Tech_Score'] + df['Legal_Score'] + df['Market_Score']) / 3
        
        # 5. Estimated Monetary Value (The "Price Tag")
        # Base value €50k + multipliers
        df['Estimated_Value'] = 50000 * (1 + (df['Total_Score'] / 20))
        
        return df