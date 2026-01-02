import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class WeightOptimizer:
    """
    PHASE 4: Advanced Optimization Layer
    Uses Ridge Regression to mathematically determine the best alpha/beta weights.
    """

    def __init__(self):
        self.model = Ridge(alpha=1.0) # L2 Regularization strength
        self.best_alpha = 0.6 # Default
        self.best_beta = 0.4  # Default
        self.is_trained = False

    def generate_training_data(self, n_samples=500):
        """
        Since we lack real M&A data for the hackathon, we simulate a 
        'Ground Truth' dataset where we define the hidden relationship.
        """
        np.random.seed(42)

        # Features
        family_sizes = np.random.randint(1, 20, n_samples)
        years_active = np.random.randint(1, 20, n_samples)

        # LOGIC: Prepare the feature matrix X for the regression
        # Feature 1: log(1 + family_size)
        # Feature 2: years_active
        X = np.column_stack([
            np.log(1 + family_sizes),
            years_active
        ])

        # HIDDEN TRUTH: We pretend the market values Family Size much more (0.85) 
        # than Age (0.10) + some random market noise.
        # Target y = 0.85 * Feat1 + 0.10 * Feat2 + Noise
        true_alpha = 0.85
        true_beta = 0.10
        noise = np.random.normal(0, 0.5, n_samples)

        y = (true_alpha * X[:, 0]) + (true_beta * X[:, 1]) + noise

        # Return as DataFrame for clarity
        df = pd.DataFrame({
            'log_family': X[:, 0],
            'years_active': X[:, 1],
            'ma_value': y
        })
        return df

    def train_model(self):
        """
        Executes the Ridge Regression to find the weights.
        """
        print("1. Generating Synthetic M&A Training Data...")
        df = self.generate_training_data()

        X = df[['log_family', 'years_active']]
        y = df['ma_value']

        print(f"2. Splitting Data (80% Train, 20% Test)...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("3. Training Ridge Regression Model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Extract learned coefficients
        # The model learns: y = coeff1 * log_family + coeff2 * years_active
        coeffs = self.model.coef_
        self.best_alpha = round(coeffs[0], 4)
        self.best_beta = round(coeffs[1], 4)

        # Validate
        preds = self.model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))

        print("-" * 30)
        print(f"✅ TRAINING COMPLETE.")
        print(f"   RMSE Error: {rmse:.4f}")
        print(f"   Learned α (Family Weight): {self.best_alpha}")
        print(f"   Learned β (Age Weight):    {self.best_beta}")
        print("-" * 30)

        return {'alpha': self.best_alpha, 'beta': self.best_beta}

if __name__ == "__main__":
    opt = WeightOptimizer()
    opt.train_model()
