import pandas as pd
import os
import sys

# --- PATH CONFIGURATION ---
# Ensures the 'src' directory is in the path so mock_data can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

class DataManager:
    """
    Handles data orchestration between the Live EPO Data Lake, 
    Static CSV snapshots (Real Data), and Synthetic Mock data.
    """
    def __init__(self, mode="🟢 Mock Data (Safe)"):
        self.mode = mode
        self.client = None
        
        # Initialize connection ONLY if Live/Dynamic Mode is selected
        if "Live" in self.mode or "Dynamic" in self.mode:
            try:
                from epo.tipdata.patstat import PatstatClient
                # 'PROD' environment validated for multi-table JOIN access
                self.client = PatstatClient(env='PROD')
                print(f"📡 {self.mode}: Connected to EPO PROD Data Lake")
            except Exception as e:
                print(f"⚠️ Live Connection Failed: {e}. Falling back to Mock.")
                self.mode = "🟢 Mock Data (Safe)"

    def get_data(self, query=None):
        """
        Retrieves data based on selected mode. 
        Maintains Standard SQL dialect for BigQuery-backed tables.
        """
        
        # 1. DYNAMIC / LIVE MODE (Real-time SQL)
        if ("Live" in self.mode or "Dynamic" in self.mode) and self.client:
            try:
                # Use a simple default if no query is passed
                sql = query.strip() if query else "SELECT * FROM tls201_appln LIMIT 100"
                
                # Standard SQL is strictly required for JOINs in this environment
                results = self.client.sql_query(sql, use_legacy_sql=False)
                df = pd.DataFrame(results)
                
                if df.empty:
                    print("⚠️ Query returned 0 results. Checking Static Fallback...")
                    return self._get_static_data()
                return df
                
            except Exception as e:
                print(f"❌ SQL Execution Error: {e}")
                return self._get_static_data()

        # 2. STATIC MODE (Gold Standard Snapshot)
        elif "Static" in self.mode:
            return self._get_static_data()

        # 3. MOCK MODE (Synthetic Data)
        else:
            return self._get_mock_data()

    def _get_static_data(self):
        """
        Loads the 'Gold Standard' snapshot. 
        This is real data saved from a previous Dynamic session.
        """
        # Look for the snapshot in /data relative to project root
        root = os.path.abspath(os.path.join(current_dir, '..'))
        file_path = os.path.join(root, 'data', 'static_portfolio.csv')
        
        if os.path.exists(file_path):
            print(f"📁 Loading Static Snapshot: {file_path}")
            return pd.read_csv(file_path)
        else:
            print("⚠️ Static snapshot 'static_portfolio.csv' not found. Falling back to Mock.")
            return self._get_mock_data()

    def _get_mock_data(self):
        """Internal helper to fetch synthetic mock portfolio."""
        try:
            # Try direct import first
            from mock_data import generate_mock_portfolio
            return generate_mock_portfolio(100)
        except ImportError:
            # Fallback for structured package access
            try:
                from src.mock_data import generate_mock_portfolio
                return generate_mock_portfolio(100)
            except Exception:
                # Final emergency fallback if import still fails
                return pd.DataFrame({'Patent_ID': range(100), 'Year': 2022})