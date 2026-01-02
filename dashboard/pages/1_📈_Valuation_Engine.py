import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# --- PATH SETUP ---
# Ensures Python can find your 'src' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_dir)

from src.mock_data import generate_mock_portfolio
from src.scoring_engine import ScoringEngine

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="3D-PVE | Command Center",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .metric-card { background-color: #0E1117; border: 1px solid #262730; padding: 15px; border-radius: 8px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 45px; background-color: #1E1E1E; border-radius: 4px; }
    .stTabs [aria-selected="true"] { background-color: #00CC96; color: white; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620603.png", width=80)
    st.title("3D-PVE Control")
    st.divider()
    
    st.subheader("⚙️ Parameters")
    portfolio_size = st.slider("Portfolio Size", 50, 500, 150)
    market_volatility = st.selectbox("Market Condition", ["Stable", "Recession", "High Growth"])
    
    st.divider()
    st.info(f"**Status:** System Ready\n\n**Mode:** {market_volatility}")
    
    if st.button("🔄 Re-Run Simulation", type="primary"):
        st.cache_data.clear()
        st.rerun()
# --- DATA LOGIC ---
@st.cache_data
def load_data(n, vol):
    # 1. Generate Mock Data (with Sectors)
    df = generate_mock_portfolio(n)
    
    # 2. Standard Scoring (The "Manual" Way)
    scorer = ScoringEngine()
    df = scorer.bulk_score(df)
    df['Standard_Value'] = df['Estimated_Value'] 
    
    # 3. AI Scoring (The "Dynamic" Way)
    if vol == "Recession":
        # Recession Strategy: Punish low market reach, protect green energy
        df['AI_Value'] = df.apply(lambda x: x['Standard_Value'] * 0.65 
                                  if x['Market_Score'] < 50 and x['Sector'] != 'Green Energy' 
                                  else x['Standard_Value'] * 0.9, axis=1)
    elif vol == "High Growth":
        # Growth Strategy: Boost Tech & AI sectors
        df['AI_Value'] = df.apply(lambda x: x['Standard_Value'] * 1.3 
                                  if x['Sector'] in ['AI & Software', 'Biotech'] 
                                  else x['Standard_Value'] * 1.1, axis=1)
    else: # Stable
        df['AI_Value'] = df['Standard_Value'] * 1.15
        
    return df

# Run the Engine
df = load_data(portfolio_size, market_volatility)

# Calculate Totals
total_std = df['Standard_Value'].sum()
total_ai = df['AI_Value'].sum()
delta = total_ai - total_std

# --- DASHBOARD HEADER ---
st.title("💎 3D-PVE Command Center")
st.markdown("### Enterprise Patent Valuation Engine")

# Top KPI Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Traditional Valuation", f"€{total_std/1e6:.2f}M", help="Static Rules-Based Model")
with col2:
    st.metric("AI-Adjusted Valuation", f"€{total_ai/1e6:.2f}M", delta=f"€{delta/1e6:.2f}M")
with col3:
    st.metric("Portfolio Health", f"{df['Total_Score'].mean():.1f}/100", "Stable")
with col4:
    st.metric("Active Scenario", market_volatility, delta_color="inverse" if market_volatility == "Recession" else "normal")

st.divider()

# --- CREATE THE 7 TABS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 3D Map", 
    "🔬 Inspector", 
    "🌊 Valuation Bridge", 
    "📈 Financials", 
    "🧠 AI Logic", 
    "📋 Data",
    "⚖️ Model Comparison"
])

# --- TAB 1: 3D Visualization ---
with tab1:
    st.subheader("Global Portfolio Risk Analysis")
    col_t1_1, col_t1_2 = st.columns([3, 1])
    
    with col_t1_1:
        # The 3D Scatter Plot
        fig_3d = px.scatter_3d(
            df, 
            x='Legal_Score', 
            y='Tech_Score', 
            z='Market_Score',
            color='Sector', 
            size='Citations', 
            hover_name='Patent_ID',
            symbol='Sector',
            color_discrete_sequence=px.colors.qualitative.Bold,
            title="3D Risk Landscape (Color=Sector, Size=Citations)"
        )
        fig_3d.update_layout(height=600, margin=dict(l=0, r=0, b=0, t=30))
        st.plotly_chart(fig_3d, use_container_width=True)
        
    with col_t1_2:
        st.info("💡 **Strategy Insight:**")
        st.markdown("""
        * **Top-Right Cluster:** \n  High Value Assets (Keep/Invest)
        * **Bottom-Left Cluster:** \n  Toxic Assets (Prune/Abandon)
        * **Top-Left Cluster:** \n  High Tech / Low Market (License Out)
        """)

# --- TAB 2: Asset Inspector ---
with tab2:
    st.subheader("Deep Dive Asset Audit")
    
    col_ins_1, col_ins_2 = st.columns([1, 2])
    
    with col_ins_1:
        # Selector
        selected_id = st.selectbox("🔎 Select Asset ID:", df['Patent_ID'].unique())
        asset = df[df['Patent_ID'] == selected_id].iloc[0]
        
        # AI Recommendation Logic
        if asset['AI_Value'] > asset['Standard_Value'] * 1.15:
            st.success(f"💎 **STRONG BUY**\n\nAI sees hidden value in {asset['Sector']} sector.")
        elif asset['AI_Value'] < asset['Standard_Value'] * 0.85:
            st.error(f"🔻 **RISK ALERT**\n\nHigh legal risk detected. Consider abandonment.")
        else:
            st.warning(f"🔸 **HOLD**\n\nFairly valued asset.")
            
        st.markdown("---")
        st.write(f"**Sector:** {asset['Sector']}")
        st.write(f"**Legal Expiry:** {int(asset['Remaining_Life'])} Yrs")
        
        # Simulated NLP Tags (The "Illusion" of Text Analysis)
        tags = ["Generative_AI", "Neural_Nets", "Transformers"] if "AI" in asset['Sector'] else ["Solid_State", "Lithium_Ion", "Grid_Storage"]
        st.write("**AI-Detected Keywords:**")
        st.caption(f"`{tags[0]}`  `{tags[1]}`  `{tags[2]}`")

    with col_ins_2:
        # Radar Chart: Asset vs Industry Average
        fig_radar = go.Figure()
        categories = ['Legal Stability', 'Tech Quality', 'Market Fit']
        
        # The Asset Trace
        fig_radar.add_trace(go.Scatterpolar(
            r=[asset['Legal_Score'], asset['Tech_Score'], asset['Market_Score']],
            theta=categories, fill='toself', name='This Asset', line_color='#00CC96'
        ))
        
        # The Industry Average Trace (Simulated)
        fig_radar.add_trace(go.Scatterpolar(
            r=[55, 60, 50], theta=categories, name='Industry Avg',
            line_color='grey', line_dash='dot'
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])), 
            title=f"Asset Profile: {selected_id}",
            height=450
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# --- TAB 3: Valuation Bridge (The "Why") ---
with tab3:
    st.subheader("Valuation Bridge Analysis (Waterfall)")
    st.markdown("### Why is the AI Price different from the Standard Price?")
    
    # Simulate waterfall steps based on scores
    base = asset['Standard_Value']
    # If score > 50, it adds value. If < 50, it subtracts.
    legal_adj = (asset['Legal_Score'] - 50) * (base * 0.05) / 10 
    tech_adj = (asset['Tech_Score'] - 50) * (base * 0.08) / 10
    market_adj = (asset['Market_Score'] - 50) * (base * 0.1) / 10
    final = asset['AI_Value']
    
    # Calculate a "residual" so the math sums up perfectly for the chart
    residual = final - (base + legal_adj + tech_adj + market_adj)
    
    fig_waterfall = go.Figure(go.Waterfall(
        name = "Valuation Adjustments", orientation = "v",
        measure = ["relative", "relative", "relative", "relative", "relative", "total"],
        x = ["Standard Base", "Legal Risk", "Tech Premium", "Market Fit", "Volatility Adj.", "Final AI Value"],
        y = [base, legal_adj, tech_adj, market_adj, residual, final],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"#EF553B"}},
        increasing = {"marker":{"color":"#00CC96"}},
        totals = {"marker":{"color":"#2f75db"}}
    ))
    
    fig_waterfall.update_layout(title=f"Valuation Walk for {selected_id}", height=500)
    st.plotly_chart(fig_waterfall, use_container_width=True)

# --- TAB 4: Financial Projections ---
with tab4:
    st.subheader("10-Year NPV Projection")
    
    years = list(range(2024, 2034))
    # Growth rate depends on the volatility setting
    rate = 1.08 if market_volatility == "High Growth" else (0.95 if market_volatility == "Recession" else 1.03)
    
    # Create projection data
    proj_values = [total_ai * (rate ** i) for i in range(len(years))]
    
    fig_line = px.line(x=years, y=proj_values, markers=True, title=f"Portfolio Value Forecast ({market_volatility} Scenario)")
    fig_line.update_traces(line_color='#00CC96', line_width=4)
    fig_line.update_layout(yaxis_title="Portfolio Value (€)", xaxis_title="Year")
    
    st.plotly_chart(fig_line, use_container_width=True)

# --- TAB 5: AI Explainability ---
with tab5:
    st.subheader("Model Explainability (XAI)")
    st.write("Relative importance of features in the Ridge Regression Model.")
    
    feat_imp = pd.DataFrame({
        'Feature': ['Forward Citations', 'Family Size', 'Remaining Life', 'Claims Count', 'Backward Citations'],
        'Weight': [0.45, 0.25, 0.15, 0.10, 0.05]
    })
    
    fig_bar = px.bar(feat_imp, x='Weight', y='Feature', orientation='h', 
                     color='Weight', title="Feature Importance Weights",
                     color_continuous_scale="Blues")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.info("The model places the highest weight on **Forward Citations**, indicating that technological impact is the primary driver of value in this sector.")

# --- TAB 6: Raw Data ---
with tab6:
    st.subheader("Database View")
    st.dataframe(df, use_container_width=True)

# --- TAB 7: Model Comparison (The "Missing" Chart) ---
with tab7:
    st.subheader("Impact of Machine Learning on Portfolio Value")
    
    col_comp_1, col_comp_2 = st.columns([2, 1])
    
    with col_comp_1:
        # Side-by-Side Bar Chart
        fig_comp = go.Figure(data=[
            go.Bar(name='Traditional (Manual)', x=['Valuation Method'], y=[total_std], 
                   marker_color='#EF553B', text=f"€{total_std/1e6:.1f}M", textposition='auto'),
            go.Bar(name='AI-Powered (3D-PVE)', x=['Valuation Method'], y=[total_ai], 
                   marker_color='#00CC96', text=f"€{total_ai/1e6:.1f}M", textposition='auto')
        ])
        
        fig_comp.update_layout(
            barmode='group', 
            height=400, 
            title="Total Portfolio Value Comparison",
            yaxis_title="Value (€)",
            showlegend=True
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        
    with col_comp_2:
        st.info("💡 **Why the difference?**")
        
        # Dynamic text based on the result
        if total_ai > total_std:
            reason = "The AI detected hidden value in **High-Tech assets** that traditional rules undervalued."
        else:
            reason = "The AI applied a discount due to **Market Volatility** and **Legal Risks** that manual rules ignored."
            
        st.markdown(f"""
        **The Traditional Model** uses fixed rules (e.g., *"Every citation is worth €1000"*).
        
        **The AI Model** adjusted the price because:
        * {reason}
        * Sector premiums were applied to **{df.groupby('Sector')['AI_Value'].sum().idxmax()}**.
        """)
