import os
import pandas as pd
from epo.tipdata.patstat import PatstatClient

# Ensure the data folder exists
output_folder = 'data'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("📸 Connecting to EPO Data Lake for Snapshot...")
client = PatstatClient()

# 1. Download Real Patents (Tesla & Sample)
print("   - Downloading tls201_appln...")
query_appln = "SELECT * FROM tls201_appln WHERE appln_filing_year > 2020 LIMIT 50"
df_appln = client.sql_query(query_appln, use_legacy_sql=False)
pd.DataFrame(df_appln).to_csv(f'{output_folder}/tls201_static.csv', index=False)

# 2. Download Real Legal Events
print("   - Downloading tls231_legal_event...")
query_legal = "SELECT * FROM tls231_inpadoc_legal_event LIMIT 50"
df_legal = client.sql_query(query_legal, use_legacy_sql=False)
pd.DataFrame(df_legal).to_csv(f'{output_folder}/tls231_static.csv', index=False)

print(f"✅ Snapshot saved to {output_folder}/. You are ready for offline mode.")