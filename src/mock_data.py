import pandas as pd
import numpy as np

def generate_mock_portfolio(n_patents=150):
    """
    Generates a synthetic dataset of patents for the hackathon demo.
    """
    np.random.seed(42) # Fixed seed for reproducibility
    
    # Generate random Patent IDs (e.g., EP-1029384)
    ids = [f"EP-{np.random.randint(1000000, 9999999)}" for _ in range(n_patents)]
    
    data = {
        'Patent_ID': ids,
        'Citations': np.random.poisson(15, n_patents),    # Forward citations
        'Family_Size': np.random.randint(1, 20, n_patents), # How many countries
        'Remaining_Life': np.random.randint(1, 20, n_patents), # Years until expiry
        'Claims_Count': np.random.randint(5, 50, n_patents),   # Complexity
        'Backward_Citations': np.random.randint(0, 50, n_patents) # Prior art
    }
    
    return pd.DataFrame(data)