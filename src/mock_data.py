import pandas as pd
import numpy as np

def generate_mock_portfolio(n_patents=150):
    """
    Generates a synthetic dataset of patents with Industry Sectors.
    """
    np.random.seed(42) # Fixed seed for reproducibility
    
    # Generate random Patent IDs
    ids = [f"EP-{np.random.randint(1000000, 9999999)}" for _ in range(n_patents)]
    
    # NEW: Industry Sectors with weighted probability
    sectors = ['Biotech', 'AI & Software', 'Automotive', 'Green Energy', 'Semiconductors']
    weights = [0.15, 0.40, 0.15, 0.20, 0.10] # 40% of patents are AI
    
    data = {
        'Patent_ID': ids,
        'Sector': np.random.choice(sectors, n_patents, p=weights),
        'Citations': np.random.poisson(15, n_patents),    # Forward citations
        'Family_Size': np.random.randint(1, 20, n_patents), # Market reach
        'Remaining_Life': np.random.randint(1, 20, n_patents), # Legal validity
        'Claims_Count': np.random.randint(5, 50, n_patents),   # Tech breadth
        'Backward_Citations': np.random.randint(0, 50, n_patents) # Prior art
    }
    
    return pd.DataFrame(data)