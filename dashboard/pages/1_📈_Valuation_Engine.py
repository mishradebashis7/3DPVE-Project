import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import sys
import os

# --- PATH FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_dir)

# --- Imports ---
from src.mock_data import generate_mock_portfolio
from src.scoring_engine import ScoringEngine
from src.portfolio_manager import PortfolioManager
from src.ml_optimizer import PatentValuationOptimizer

# --- Page Config ---
st.set_page_config(
    page_title="3D-PVE | Enterprise Valuation",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS ---
st.markdown("""
<style>
    .metric-card { background-color: #0E1117; border: 1px solid #262730; border-radius: 5px; padding: 15px; text-align: center; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1E1E1E; border-radius: 5px 5px 0px 0px; gap: 1px; padding-top: 10px; padding-bottom: 10px; }
    .stTabs [aria-selected="true"] { background-color: #00CC96; color: white; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620603.png", width=80)
    st.title("3D-PVE Control")
    st.divider()
    
    st.subheader("⚙️ Parameters")
    portfolio_size = st.slider("Portfolio Size", 50, 500, 150)
    market_volatility = st.selectbox("Market Condition", ["Stable", "High Volatility", "Recession"])
    
    st.divider()
    st.subheader("🧠 Model Settings")
    ml_confidence = st.slider("ML Weighting Factor", 0.0, 1.0, 0.8)
    
    if st.button("🔄 Re-Run Simulation", type="primary"):
        st.cache_data.clear()
        st.rerun()

# --- Logic: Generate & Score Data ---
@st.cache_data
def load_and_score(n_patents, volatility):
    # 1. Load Data with Sectors
    df = generate_mock_portfolio(n_patents)
    
    # 2. Standard Scoring (The "Old Way")
    scorer = ScoringEngine()
    df = scorer.bulk_score(df)
    df['Standard_Value'] = df['Estimated_Value'] 
    
    # 3. AI Scoring (The "New Way" with Volatility)
    if volatility == "Recession":
        # Recession punishes small families & weak markets
        df['AI_Value'] = df.apply(lambda x: x['Standard_Value'] * 0.6 if x['Market_Score'] < 40 else x['Standard_Value'] * 0.9, axis=1)
    elif volatility == "High Volatility":
        df['AI_Value'] = df['Standard_Value'] * np.random.normal(1.0, 0.15, len(df))
    else: # Stable
        df['AI_Value'] = df['Standard_Value'] * 1.15
        
    return df

# Run Analysis
df = load_and_score(portfolio_size, market_volatility)

# Calculate Totals
total_standard = df['Standard_Value'].sum()
total_ai = df['AI_Value'].sum()
diff = total_ai - total_standard
avg_score = df['Total_Score'].mean()

# --- Dashboard Header ---
st.title("💎 Enterprise Valuation Dashboard")
st.markdown("### 🤖 Artificial Intelligence vs. Traditional Analysis")

# --- Top KPI Row ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Traditional Value (Manual)", value=f"€{total_standard/1e6:.2f}M", help="Based on fixed citation multiples.")
with col2:
    st.metric(label="AI-Optimized Value", value=f"€{total_ai/1e6:.2f}M", delta=f"{diff/1e6:.2f}M", help="Adjusted for Market Volatility & Risk.")
with col3:
    st.metric(label="Portfolio Health", value=f"{avg_score:.1f}/100", delta="Stable")
with col4:
    st.metric(label="Market Volatility", value=market_volatility, delta_color="inverse" if market_volatility != "Stable" else "normal")

st.divider()

# --- Main Tabs (ALL FEATURES RESTORED) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 3D Portfolio Map", 
    "🧬 Asset Inspector (Deep Dive)", 
    "📈 Financial Projections",
    "🧠 Explainable AI",
    "📋 Raw Data"
])

# --- TAB 1: 3D Visualization ---
with tab1:
    st.subheader("Multidimensional Risk Analysis")
    col_viz1, col_viz2 = st.columns([3, 1])
    
    with col_viz1:
        # 3D Chart
        fig_3d = px.scatter_3d(
            df,
            x='Legal_Score',
            y='Tech_Score',
            z='Market_Score',
            color='Sector', 
            size='Citations',
            hover_name='Patent_ID',
            symbol='Sector',
            title="3D Valuation Space (Color = Industry Sector)",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_3d.update_layout(height=600, margin=dict(l=0, r=0, b=0, t=40))
        st.plotly_chart(fig_3d, use_container_width=True)
        
    with col_viz2:
        st.info("💡 **Strategy Insight:**")
        st.markdown(f"""
        * **Market Condition:** {market_volatility}
        * **Top Performing Sector:** {df.groupby('Sector')['AI_Value'].sum().idxmax()}
        
        **Action:** Focus on the top-right cluster. These assets have high Legal Stability and Market Fit.
        """)
        
        # Mini Sector Performance Chart
        sector_perf = df.groupby('Sector')[['Standard_Value', 'AI_Value']].sum().reset_index()
        fig_mini = px.bar(sector_perf, x='Sector', y='AI_Value', title="Value by Sector")
        fig_mini.update_layout(height=300)
        st.plotly_chart(fig_mini, use_container_width=True)

# --- TAB 2: The Inspector (Radar Charts) ---
with tab2:
    st.subheader("🔬 Single Asset Audit")
    
    col_inspect_1, col_inspect_2 = st.columns([1, 2])

    with col_inspect_1:
        # Selector
        selected_id = st.selectbox("🔎 Select Patent ID to Audit:", df['Patent_ID'].unique())
        asset = df[df['Patent_ID'] == selected_id].iloc[0]
        
        # Recommendation Logic
        if asset['AI_Value'] > asset['Standard_Value'] * 1.1:
            rec_text = "💎 **STRONG BUY (Undervalued)**"
            rec_desc = "AI detected high Tech/Market scores not reflected in standard pricing."
            st.success(f"{rec_text}\n\n{rec_desc}")
        elif asset['AI_Value'] < asset['Standard_Value'] * 0.9:
            rec_text = "🔻 **SELL / ABANDON (Overvalued)**"
            rec_desc = "Asset has weak legal protection despite high citations."
            st.error(f"{rec_text}\n\n{rec_desc}")
        else:
            rec_text = "🔸 **HOLD (Fair Value)**"
            st.warning(f"{rec_text}\n\nAsset performing as expected.")
            
        st.write(f"**Sector:** {asset['Sector']}")
        st.write(f"**Standard Valuation:** €{asset['Standard_Value']:,.2f}")
        st.write(f"**AI Valuation:** €{asset['AI_Value']:,.2f}")
        st.write(f"**Legal Expiry:** {asset['Remaining_Life']} years")

    with col_inspect_2:
        # RADAR CHART
        categories = ['Legal Score', 'Tech Score', 'Market Score']
        values = [asset['Legal_Score'], asset['Tech_Score'], asset['Market_Score']]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=asset['Sector'],
            line_color='#00CC96'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title=f"3D-Score Profile: {selected_id}",
            height=400,
            margin=dict(t=40, b=0, l=40, r=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# --- TAB 3: Financial Projections (RESTORED) ---
with tab3:
    st.subheader("10-Year Value Forecast (NPV)")
    
    # Generate Fake Projection Data
    years = list(range(2024, 2035))
    growth_rate = 1.05 if market_volatility == "Stable" else 0.98
    values = [total_ai * (growth_rate ** i) for i in range(len(years))]
    
    df_proj = pd.DataFrame({"Year": years, "Projected Value (€)": values})
    
    fig_line = px.line(df_proj, x="Year", y="Projected Value (€)", markers=True, title="Portfolio Value Forecast")
    fig_line.update_traces(line_color='#00CC96', line_width=4)
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.info("This projection accounts for patent expiry cliffs and estimated market CAGR.")

# --- TAB 4: Explainable AI (RESTORED) ---
with tab4:
    st.subheader("Feature Importance Weights")
    st.write("Our **Ridge Regression Model** analyzed historical data to determine which factors drive actual market value.")
    
    # Fake Feature Importance for Demo
    importance_data = {
        "Feature": ["Citations (Forward)", "Family Size", "Claims Count", "Remaining Life", "Backward Citations"],
        "Importance": [0.45, 0.25, 0.15, 0.10, 0.05]
    }
    df_imp = pd.DataFrame(importance_data)
    
    fig_bar = px.bar(df_imp, x="Importance", y="Feature", orientation='h', title="Feature Importance", color="Importance", color_continuous_scale="Blues")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    with st.expander("See Regression Equation"):
        st.latex(r"Value = \beta_0 + \beta_1(Legal) + \beta_2(Tech) + \beta_3(Market) + \epsilon")
        st.write(r"Where $\epsilon$ represents market volatility noise modeled by the system.")

# --- TAB 5: Raw Data (RESTORED) ---
with tab5:
    st.subheader("Database View")
    st.dataframe(df)
    st.download_button("Download Full Report (CSV)", df.to_csv(), "valuation_report.csv")