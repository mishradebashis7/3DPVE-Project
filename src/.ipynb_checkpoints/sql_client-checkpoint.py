import pandas as pd
import sqlite3
import numpy as np

# --- SECTION 1: THE SQL QUERIES ---
# We store them here as standard Python strings.

QUERY_LEGAL = """
SELECT 
    appln_id, 
    event_code 
FROM 
    TLS231_INPADOC_LEGAL_EVENT
WHERE 
    event_code IN ('EP', 'PGR', 'PL', 'PR', 'OPP')
"""

QUERY_ECO = """
SELECT 
    t201.appln_id,
    t201.appln_filing_year,
    COUNT(DISTINCT t218.publ_auth) as family_size,
    (2026 - t201.appln_filing_year) as years_active
FROM 
    TLS201_APPLN t201
JOIN 
    TLS218_DOCDB_FAM t218 ON t201.appln_id = t218.appln_id
GROUP BY 
    t201.appln_id, t201.appln_filing_year
"""

QUERY_TECH = """
SELECT 
    t211.pat_publn_id_src as appln_id,
    t224.cpc_class_symbol
FROM 
    TLS211_PAT_CITN t211
JOIN 
    TLS224_APPLN_CPC t224 ON t211.pat_publn_id_cited = t224.appln_id
"""

# --- SECTION 2: THE PYTHON HANDLER ---

class SQLProcessor:
    def __init__(self, db_path=None):
        """
        If db_path is provided, connects to real DB.
        If None, builds a temporary simulation DB in memory.
        """
        self.is_simulation = db_path is None
        
        if self.is_simulation:
            print("[System] No DB path provided. Initializing In-Memory Simulation Database...")
            self.conn = sqlite3.connect(":memory:") # RAM-only database
            self._setup_simulation_data()
        else:
            print(f"[System] Connecting to database at {db_path}...")
            self.conn = sqlite3.connect(db_path)

    def _setup_simulation_data(self):
        """
        Creates fake tables (TLS231, TLS201, etc.) inside the RAM database
        so that the SQL queries have something to run against.
        """
        # 1. Create TLS201_APPLN (Application Data)
        ids = range(1000, 1050) # 50 patents
        df_201 = pd.DataFrame({
            'appln_id': ids,
            'appln_filing_year': np.random.randint(2005, 2024, 50)
        })
        df_201.to_sql('TLS201_APPLN', self.conn, index=False)
        
        # 2. Create TLS218_DOCDB_FAM (Family Data)
        # Generate random family members
        fam_data = []
        for aid in ids:
            n_members = np.random.randint(1, 10)
            for _ in range(n_members):
                fam_data.append({'appln_id': aid, 'publ_auth': 'US'}) # Simplified
        pd.DataFrame(fam_data).to_sql('TLS218_DOCDB_FAM', self.conn, index=False)
        
        # 3. Create TLS231_LEGAL (Legal Events)
        legal_data = []
        for aid in ids:
            # 10% chance of being Revoked ('EP')
            if np.random.random() < 0.1:
                legal_data.append({'appln_id': aid, 'event_code': 'EP'})
            else:
                legal_data.append({'appln_id': aid, 'event_code': 'NO_EVENT'})
        pd.DataFrame(legal_data).to_sql('TLS231_INPADOC_LEGAL_EVENT', self.conn, index=False)
        
        # 4. Create Tech tables (Simplified for demo)
        pd.DataFrame({'appln_id': [], 'cpc_class_symbol': []}).to_sql('TLS211_PAT_CITN', self.conn, index=False)
        pd.DataFrame({'appln_id': [], 'cpc_class_symbol': []}).to_sql('TLS224_APPLN_CPC', self.conn, index=False)
        
        print("[System] Simulation Data Ready. You can now run SQL queries.")

    def fetch_data(self):
        """
        Runs the SQL queries and returns a merged DataFrame.
        """
        print("[SQL] Executing Economic Query...")
        df_eco = pd.read_sql(QUERY_ECO, self.conn)
        
        print("[SQL] Executing Legal Query...")
        df_legal = pd.read_sql(QUERY_LEGAL, self.conn)
        
        # Merge in Python
        print("[ETL] Merging datasets...")
        df_merged = pd.merge(df_eco, df_legal, on='appln_id', how='left')
        
        # Fill missing legal status
        df_merged['event_code'] = df_merged['event_code'].fillna('NONE')
        
        # Rename for the 3D-PVE Engine
        df_merged['legal_status'] = df_merged['event_code'].apply(
            lambda x: 'Revocation' if x == 'EP' else 'No Challenge'
        )
        df_merged.rename(columns={'appln_id': 'patent_id'}, inplace=True)
        
        # Mocking tech diversity for now as SQL logic is complex
        df_merged['tech_diversity'] = np.random.beta(2, 5, len(df_merged))
        
        return df_merged

# Self-test block
if __name__ == "__main__":
    processor = SQLProcessor() # No path = Simulation Mode
    df = processor.fetch_data()
    print("\n--- RESULTS FROM SQL EXECUTION ---")
    print(df.head())