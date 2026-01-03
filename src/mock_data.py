import pandas as pd
import numpy as np

def generate_mock_portfolio(n_patents=150):
    """
    Generates a synthetic dataset of patents with Industry Sectors.
    """
    np.random.seed(42) # Fixed seed for reproducibility
    
    # Generate random Patent IDs
    ids = [f"EP-{np.random.randint(1000000, 9999999)}" for _ in range(n_patents)]
    
    # Industry Sectors with weighted probability
    sectors = ['Biotech', 'AI & Software', 'Automotive', 'Green Energy', 'Semiconductors']
    weights = [0.15, 0.40, 0.15, 0.20, 0.10] 
    
    data = {
        'Patent_ID': ids,
        'Sector': np.random.choice(sectors, n_patents, p=weights),
        'Citations': np.random.poisson(15, n_patents),      # Forward citations
        'Family_Size': np.random.randint(1, 20, n_patents), # Market reach
        'Remaining_Life': np.random.randint(1, 20, n_patents), # Legal validity
        'Claims_Count': np.random.randint(5, 50, n_patents),   # Tech breadth
        'Backward_Citations': np.random.randint(0, 50, n_patents), # Prior art
        # Add internal scores for the 3D Map compatibility
        'Legal_Score': np.random.randint(30, 95, n_patents),
        'Tech_Score': np.random.randint(30, 95, n_patents),
        'Market_Score': np.random.randint(30, 95, n_patents)
    }
    
    return pd.DataFrame(data)

# ALIAS: This ensures that any code looking for 'generate_mock_data' finds this function
def generate_mock_data(n=150):
    df = generate_mock_portfolio(n)
    return {"tls201": df}