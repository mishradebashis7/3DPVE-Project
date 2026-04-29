# 3D-PVE: 3D Patent Valuation Engine 🚀

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://3dpve-project.streamlit.app/)
[![EPO PATSTAT](https://img.shields.io/badge/Data-EPO%20PATSTAT-003087?style=for-the-badge)](https://www.epo.org/en/searching-for-patents/business/patstat)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![Developed for EPO CodeFest 2026](https://img.shields.io/badge/EPO-CodeFest%202026-gold?style=for-the-badge)](https://www.epo.org)

> **Transform raw patent data into actionable IP intelligence.** 3D-PVE evaluates patent portfolios across three independent dimensions — Technical, Legal, and Market — and renders them as an interactive 3D valuation landscape powered by live EPO PATSTAT data.

🔗 **[Try the Live Dashboard →](https://3dpve-project.streamlit.app/)**

---

## 🌟 Key Features

| Feature | Description |
|---|---|
| **Live EPO Integration** | Direct connection to EPO Data Lake via BigQuery/Standard SQL |
| **Hybrid Data Modes** | Switch between Live, Snapshot, and Mock data seamlessly |
| **3D Visualization** | Explore patent clusters across Legal × Technical × Market axes |
| **IPC Sector Mapping** | Auto-classifies patents into AI, Biotech, Green Energy, and more |
| **AI-Adjusted Valuation** | ML model adjusts scores for market volatility & sector risk premiums |
| **Portfolio Analytics** | Aggregate scoring and benchmarking across entire patent families |

---

## 🏗️ Technical Architecture

### Scoring Model — The Three Dimensions

```
V_cp = f(S_legal, S_technical, S_economic)
```

| Dimension | Metric | Method |
|---|---|---|
| **Legal (S_leg)** | Opposition survival, active status, remaining life | Weighted event scoring |
| **Technical (S_tech)** | Cross-domain citation influence | Shannon entropy across IPC fields |
| **Economic (S_eco)** | Patent family size × years active | Jurisdiction breadth scoring |

### Data Pipeline

```
EPO PATSTAT
    │
    ▼
sql_client.py ──► [Live / Static Snapshot / Mock]
    │
    ▼
scoring_engine.py ──► Legal Score + Tech Score + Economic Score
    │
    ▼
ml_optimizer.py ──► AI-Adjusted Composite Score (V_cp)
    │
    ▼
Streamlit Dashboard ──► Interactive 3D Scatter Plot
```

### PATSTAT Tables Used

| Table | Purpose |
|---|---|
| `tls201_appln` | Patent applications (filing dates, family info) |
| `tls211_pat_publn` | Publications and citation data |
| `tls209_appln_ipc` | IPC classification codes |
| `tls231_inpadoc_legal_event` | Legal events (grants, oppositions, lapses) |

---

## 📊 IPC Sector Mapping

```python
"G06" | "G16" | "H04"  →  AI & Software
"A61" | "C12"          →  Biotech & Pharma
"H01L"                 →  Semiconductors
"Y02" | "H01M"         →  Green Energy
"B60" | "G05D"         →  Automotive
```

---

## 🔄 Hybrid Data Orchestration

The engine operates in three modes, switchable at runtime:

```
┌─────────────┬──────────────────────────────┬───────────────────────┐
│ Mode        │ Source                       │ Use Case              │
├─────────────┼──────────────────────────────┼───────────────────────┤
│ Dynamic     │ Live EPO PATSTAT (BigQuery)   │ Production / Research │
│ Static      │ Local CSV snapshot           │ Offline / Verified    │
│ Mock        │ Synthetic generated data     │ Demo / Testing        │
└─────────────┴──────────────────────────────┴───────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Access to EPO TIP PATSTAT environment (`epo-tipdata` library)

### Installation

```bash
# Clone the repository
git clone https://github.com/mishradebashis7/3DPVE-Project.git
cd 3DPVE-Project

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard/1_📈_Valuation_Engine.py
```

---

## 🛠️ Project Structure

```
3DPVE-Project/
├── src/
│   ├── scoring_engine.py        # Core valuation math & weighted algorithms
│   ├── sql_client.py            # Tri-modal data broker (Live/Static/Mock)
│   ├── ml_optimizer.py          # AI-adjusted valuation model
│   ├── portfolio_manager.py     # Portfolio-level aggregation & benchmarking
│   └── mock_data.py             # Synthetic data generator
├── dashboard/
│   ├── app.py                   # Streamlit entry point
│   └── pages/                   # Multi-page dashboard views
├── data/                        # Local 'Gold Standard' static snapshots
├── Connection_Test.ipynb        # EPO PATSTAT connection testing
├── create_snapshot.py           # Downloads & caches real EPO data
├── requirements.txt
└── README.md
```

---

## 📈 Live Demo

The dashboard is deployed and accessible at:

**🔗 [https://3dpve-project.streamlit.app/](https://3dpve-project.streamlit.app/)**

Features available in the live demo:
- Interactive 3D patent portfolio visualization
- Sector-based filtering (AI, Biotech, Green Energy, Semiconductors, Automotive)
- Mock data mode for instant exploration without EPO credentials
- Composite score breakdown per patent

---

## 👥 Team

Developed by **Team CaFoscari** for the **EPO CodeFest 2026**
Università Ca' Foscari Venezia

---

*Built on EPO PATSTAT — the world's most comprehensive patent statistics database.*
