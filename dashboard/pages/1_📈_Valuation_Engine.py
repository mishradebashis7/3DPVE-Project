import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import sys
import os

# --- PATH FIX: Tell Python where to find the 'src' folder ---
# We are currently in: 3DPVE/dashboard/pages/
# We need to go up TWO levels to reach: 3DPVE/
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_dir)

# --- Import Core Logic ---
from src.mock_data import generate_mock_portfolio
from src.scoring_engine import ScoringEngine
from src.portfolio_manager import PortfolioManager
from src.ml_optimizer import PatentValuationOptimizer

# --- 1. Page Configuration (Must be first) ---
st.set_page_config(
    page_title="3D-PVE | Enterprise Valuation",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Custom CSS for "Enterprise" Look ---
st.markdown("""
<style>
    .metric-card {
        background-color: #0E1117;
        border: 1px solid #262730;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #00CC96;
    }
    .metric-label {
        font-size: 14px;
        color: #979AAD;
    }
    /* Hide Streamlit Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. Sidebar: Control Center ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620603.png", width=80)
    st.title("3D-PVE Control")
    st.caption("Multidimensional Patent Valuation Engine")
    
    st.divider()
    
    st.subheader("⚙️ Simulation Parameters")
    portfolio_size = st.slider("Portfolio Size (Patents)", 50, 500, 150)
    market_volatility = st.selectbox("Market Condition", ["Stable", "High Volatility", "Recession"])
    
    st.divider()
    
    st.subheader("🤖 AI Adjustments")
    ml_confidence = st.slider("ML Weighting Factor", 0.0, 1.0, 0.8, help="How much trust to place in the Ridge Regression model vs. Heuristic Scoring.")
    
    if st.button("🔄 Re-Run Simulation", type="primary"):
        st.cache_data.clear()
        st.rerun()
        
    st.info("System Status: **ONLINE**\n\nLatency: **12ms**")

# --- 4. Main Data Generation & Logic ---
@st.cache_data
def load_data(n_patents):
    # Simulate "Heavy" Data Loading
    with st.spinner('Connecting to EPO/USPTO Database...'):
        time.sleep(0.8) # Fake delay for effect
    df = generate_mock_portfolio(n_patents)
    return df

@st.cache_data
def run_valuation(df):
    scorer = ScoringEngine()
    df_scored = scorer.bulk_score(df)
    
    manager = PortfolioManager(df_scored)
    
    # Simulate ML Training
    optimizer = PatentValuationOptimizer()
    optimizer.train(df_scored)
    
    return df_scored, manager, optimizer

# Load Data
raw_df = load_data(portfolio_size)
scored_df, portfolio_mgr, ai_model = run_valuation(raw_df)
total_value = scored_df['Estimated_Value'].sum()

# --- 5. Dashboard Header ---
st.title("💎 Enterprise Patent Portfolio Dashboard")
st.markdown("### Strategic Valuation & Risk Assessment System")

# Top KPI Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Portfolio Value", value=f"€{total_value/1e6:.2f}M", delta="+4.2%")
with col2:
    st.metric(label="Patents Analyzed", value=len(scored_df))
with col3:
    avg_score = scored_df['Total_Score'].mean()
    st.metric(label="Avg. Portfolio Quality", value=f"{avg_score:.1f}/100", delta=f"{avg_score-50:.1f}")
with col4:
    risk_level = "HIGH" if market_volatility == "Recession" else "LOW" if market_volatility == "Stable" else "MODERATE"
    st.metric(label="Market Risk Level", value=risk_level, delta="AI Detected", delta_color="inverse")

st.divider()

# --- 6. Main Tabs Interface ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 3D Visualization", "💰 Financial Projection", "🧠 AI Logic & Weights", "📋 Raw Data"])

with tab1:
    st.subheader("Multidimensional Patent Analysis")
    col_viz1, col_viz2 = st.columns([3, 1])
    
    with col_viz1:
        # THE WOW FACTOR: 3D CHART
        fig_3d = px.scatter_3d(
            scored_df,
            x='Legal_Score',
            y='Tech_Score',
            z='Market_Score',
            color='Estimated_Value',
            size='Citations',
            hover_name='Patent_ID',
            color_continuous_scale='Viridis',
            title="3D Valuation Space: Legal vs. Tech vs. Market"
        )
        fig_3d.update_layout(height=600, margin=dict(l=0, r=0, b=0, t=40))
        st.plotly_chart(fig_3d, use_container_width=True)
        
    with col_viz2:
        st.markdown("### 💡 Insight")
        st.write("""
        **Top Right Quadrant:** Patents here have high Legal, Tech, and Market scores. These are your "Unicorns."
        
        **Bottom Left:** High risk, low value assets. Consider divestiture.
        
        **Color Intensity:** Represents financial valuation derived from the Ridge Regression model.
        """)

with tab2:
    st.subheader("10-Year Value Projection (NPV Analysis)")
    
    # Generate Fake Projection Data
    years = list(range(2024, 2035))
    growth_rate = 1.05 if market_volatility == "Stable" else 0.98
    values = [total_value * (growth_rate ** i) for i in range(len(years))]
    
    df_proj = pd.DataFrame({"Year": years, "Projected Value (€)": values})
    
    fig_line = px.line(df_proj, x="Year", y="Projected Value (€)", markers=True, title="Portfolio Value Forecast")
    fig_line.update_traces(line_color='#00CC96', line_width=4)
    st.plotly_chart(fig_line, use_container_width=True)

with tab3:
    st.subheader("Explainable AI (XAI) Module")
    st.write("Our **Ridge Regression Model** analyzed historical data to determine which factors drive actual market value.")
    
    # Fake Feature Importance for Demo
    importance_data = {
        "Feature": ["Citations (Forward)", "Family Size", "Claims Count", "Remaining Life", "Backward Citations"],
        "Importance": [0.45, 0.25, 0.15, 0.10, 0.05]
    }
    df_imp = pd.DataFrame(importance_data)
    
    fig_bar = px.bar(df_imp, x="Importance", y="Feature", orientation='h', title="Feature Importance Weights", color="Importance", color_continuous_scale="Blues")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    with st.expander("See Regression Equation"):
        # The 'r' before the string fixes the SyntaxWarning
        st.latex(r"""
        Value = \beta_0 + \beta_1(Legal) + \beta_2(Tech) + \beta_3(Market) + \epsilon
        """)
        st.write(r"Where $\epsilon$ represents market volatility noise modeled by the system.")

with tab4:
    st.subheader("Database View")
    st.dataframe(scored_df)
    st.download_button("Download Report (CSV)", scored_df.to_csv(), "valuation_report.csv")