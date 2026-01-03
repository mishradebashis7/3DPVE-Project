# 3D-PVE: 3D Patent Valuation Engine 🚀

A real-time analytics dashboard that transforms raw EPO PATSTAT data into actionable IP intelligence. 3D-PVE uses a hybrid scoring model to evaluate patent portfolios across Technical, Legal, and Market dimensions.

## 🌟 Key Features
- **Live Data Integration:** Direct connection to the EPO Data Lake (BigQuery/Standard SQL).
- **Hybrid Data Orchestration:** Seamlessly switch between **Dynamic** (Live), **Static** (Verified Snapshot), and **Mock** (Synthetic) data modes.
- **IPC-Based Sector Mapping:** Automatically classifies patents into sectors (AI, Biotech, Green Energy, etc.) using International Patent Classification codes.
- **AI-Adjusted Valuation:** A predictive model that adjusts traditional valuations based on real-world market volatility and sector-specific risk premiums.
- **Interactive 3D Visualization:** Explore patent value clusters in a 3-axis space (Legal Strength vs. Tech Influence vs. Market Potential).

## 🏗️ Technical Architecture


### Data Pipeline
1. **Extraction:** Queries `tls201_appln`, `tls211_pat_publn`, and `tls209_appln_ipc` via Standard SQL.
2. **Harmonization:** Maps raw PATSTAT schema (e.g., `nb_citing_doc`) to unified engine features.
3. **Classification:** Uses regex-based mapping on IPC prefixes to determine industry sectors.
4. **Scoring:** Calculates **Technical Score** (Claims & Citations) and **Legal Score** (Remaining Life & Family Size).

## 📊 Sector Mapping Logic
The engine uses verified IPC distribution data to categorize patents:
- `G06`, `G16`, `H04`: **AI & Software**
- `A61`, `C12`: **Biotech**
- `H01L`: **Semiconductors**
- `Y02`, `H01M`: **Green Energy**
- `B60`, `G05D`: **Automotive**

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Access to EPO TIP PATSTAT environment (`epo-tipdata` library)

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/3DPVE.git](https://github.com/YOUR_USERNAME/3DPVE.git)
   cd 3DPVE

    Install dependencies:
    Bash

pip install -r requirements.txt

Run the Dashboard:
Bash

    streamlit run dashboard/1_📈_Valuation_Engine.py

🛠️ Project Structure

    src/sql_client.py: The data broker handling Live/Static/Mock modes.

    src/scoring_engine.py: The core valuation math and weighted algorithms.

    dashboard/: Streamlit interface and 3D visualization logic.

    data/: Local storage for the 'Gold Standard' static snapshot.

Developed for the [Name of Event/Hackathon] - 2026.


---

### **How to add this to your project:**
1. Create a new file in your root folder named `README.md`.
2. Paste the content above.
3. **Commit it:** ```bash
   git add README.md
   git commit -m "docs: add professional README with architecture and mapping logic"
   git push
