from sklearn.linear_model import Ridge
import pandas as pd
import numpy as np

class PatentValuationOptimizer:
    def __init__(self):
        self.model = Ridge(alpha=1.0)
        self.is_trained = False

    def train(self, df):
        """
        Simulates training an ML model on the scored data.
        """
        # We use the 3 scores to predict the Value (Reverse engineering our own logic for the demo)
        features = ['Tech_Score', 'Legal_Score', 'Market_Score']
        target = 'Estimated_Value'
        
        if len(df) > 0:
            X = df[features]
            y = df[target]
            self.model.fit(X, y)
            self.is_trained = True
            
    def predict(self, tech, legal, market):
        if not self.is_trained:
            return 0
        input_data = pd.DataFrame([[tech, legal, market]], 
                                columns=['Tech_Score', 'Legal_Score', 'Market_Score'])
        return self.model.predict(input_data)[0]