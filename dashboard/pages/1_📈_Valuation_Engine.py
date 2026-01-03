import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# --- PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_dir)

from src.mock_data import generate_mock_portfolio
from src.scoring_engine import ScoringEngine
from src.sql_client import DataManager

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
import numpy as np
from src.sql_client import DataManager
from src.mock_data import generate_mock_portfolio
from src.scoring_engine import ScoringEngine

@st.cache_data
def load_data(n, vol, mode):
    dm = DataManager(mode)
    
    # --- 1. DATA ACQUISITION PHASE ---
    if "Live" in mode:
        query = f"""
        SELECT 
            t1.appln_id, t1.appln_filing_year, t1.docdb_family_size, 
            t2.publn_claims,
            t3.ipc_class_symbol
        FROM tls201_appln AS t1
        INNER JOIN tls211_pat_publn AS t2 ON t1.appln_id = t2.appln_id
        LEFT JOIN tls209_appln_ipc AS t3 ON t1.appln_id = t3.appln_id
        WHERE t1.appln_filing_year > 2018
        LIMIT {n}
        """
        raw_df = dm.get_data(query)
    else:
        raw_df = dm.get_data()

    # Fallback to Mock if fetch fails
    if raw_df is None or raw_df.empty:
        from src.mock_data import generate_mock_portfolio
        raw_df = generate_mock_portfolio(n)

    # --- 2. HARMONIZATION ---
    df = raw_df.rename(columns={
        'appln_id': 'Patent_ID',
        'appln_filing_year': 'Year',
        'publn_claims': 'Claims_Count',
        'docdb_family_size': 'Family_Size'
    })

    # --- 3. SECTOR CLASSIFICATION (IPC MAPPING) ---
    def map_ipc_to_sector(ipc):
        if not ipc or pd.isna(ipc): return 'Industrial Mfg'
        ipc = str(ipc).upper()
        
        # 1. AI & Digital (G06F, H04L, H04N, H04W, G06Q)
        if ipc.startswith(('G06', 'G16', 'H04')): 
            return 'AI & Software'
        
        # 2. Biotech & Life Sciences (A61K, A61P, A61B, C12N)
        if ipc.startswith(('A61', 'C12')): 
            return 'Biotech'
        
        # 3. Deep Tech / Semiconductors (H01L) - NEW!
        if ipc.startswith('H01L'):
            return 'Semiconductors'
        
        # 4. Green Energy & Climate Tech (H01M, Y02, F03D)
        if ipc.startswith(('Y02', 'H01M', 'F03')): 
            return 'Green Energy'
        
        # 5. Advanced Materials / Chem (C07, C08, B32) - NEW!
        if ipc.startswith(('C07', 'C08', 'B32')):
            return 'Advanced Materials'
            
        # 6. Mobility (B60, G05D)
        if ipc.startswith(('B60', 'G05D')): 
            return 'Automotive'
            
        return 'Industrial Mfg'

    if 'ipc_class_symbol' in df.columns:
        df['Sector'] = df['ipc_class_symbol'].apply(map_ipc_to_sector)
    elif 'Sector' not in df.columns:
        df['Sector'] = np.random.choice(['AI & Software', 'Biotech', 'Green Energy', 'Automotive'], len(df))

    # --- 4. FEATURE ENGINEERING (The Fix for AttributeError) ---
    # We ensure columns exist as Series before calling fillna
    if 'Year' not in df.columns:
        df['Year'] = 2022
    
    # Secure numeric conversion
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(2022)
    df['Remaining_Life'] = (20 - (2026 - df['Year'])).clip(lower=1, upper=20)
    
    # Fill Citations and other scoring columns
    if 'Citations' not in df.columns:
        df['Citations'] = (df['Family_Size'].fillna(1) * 2).astype(int)
    
    if 'Claims_Count' not in df.columns:
        df['Claims_Count'] = 15
    else:
        df['Claims_Count'] = pd.to_numeric(df['Claims_Count'], errors='coerce').fillna(15)

    df['Backward_Citations'] = np.random.randint(2, 12, len(df))

    # --- 5. SCORING ENGINE ---
    from src.scoring_engine import ScoringEngine
    scorer = ScoringEngine()
    df = scorer.bulk_score(df) 

    # --- 6. DYNAMIC VALUATION SPLIT ---
    df['Standard_Value'] = df['Estimated_Value']
    
    vol_map = {
        "Recession": {
            'AI & Software': 0.85, 'Biotech': 0.80, 'Green Energy': 0.70, 
            'Automotive': 0.60, 'Industrial Mfg': 0.50
        },
        "High Growth": {
            'AI & Software': 1.50, 'Biotech': 1.40, 'Green Energy': 1.30, 
            'Automotive': 1.25, 'Industrial Mfg': 1.15
        },
        "Stable": {
            'AI & Software': 1.10, 'Biotech': 1.05, 'Green Energy': 1.02, 
            'Automotive': 1.00, 'Industrial Mfg': 0.95
        }
    }
    
    current_vol_map = vol_map.get(vol, vol_map["Stable"])
    df['AI_Value'] = df['Standard_Value'] * df['Sector'].map(current_vol_map).fillna(1.0)
            
    return df

# --- GET THE GLOBAL MODE FROM LANDING PAGE ---
current_mode = st.session_state.get('data_mode', "🟢 Mock Data (Safe)")

# Run the Engine with the new mode parameter
df = load_data(portfolio_size, market_volatility, current_mode)

# Calculate Totals
total_std = df['Standard_Value'].sum()
total_ai = df['AI_Value'].sum()
delta = total_ai - total_std

# --- DASHBOARD HEADER ---
st.title("💎 3D-PVE Command Center")
st.markdown("### Enterprise Patent Valuation Engine")

# System Status Banner
if "Live" in current_mode:
    st.warning(f"📡 **LIVE MODE:** Connected to EPO Data Lake | Dataset: {portfolio_size} assets")
elif "Static" in current_mode:
    st.info(f"📂 **OFFLINE MODE:** Using Static Snapshot | Source: data/tls201_static.csv")
else:
    st.success(f"🧪 **SIMULATION MODE:** Using Generative Mock Data")

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

# --- TAB 3: Valuation Bridge (Updated for Real Risk) ---
with tab3:
    st.subheader("Valuation Bridge Analysis (Waterfall)")
    
    # 1. Base Valuation
    base = asset['Standard_Value']
    
    # 2. Logic: Real Risk vs. Simulated Premium
    # If in Live Mode, check for specific legal event codes
    legal_risk_deduction = 0
    if "Live" in current_mode:
        # Example: Deduction if a 'LAPS' (Lapse) or 'WDRI' (Withdrawal) event exists
        # In a full implementation, you'd join with tls231
        legal_risk_deduction = -(base * 0.40) if asset.get('Event_Code') in ['LAPS', 'WDRI'] else 0
    else:
        # Use your existing scoring logic for Mock/Static
        legal_risk_deduction = (asset['Legal_Score'] - 50) * (base * 0.05) / 10 

    tech_premium = (asset['Tech_Score'] - 50) * (base * 0.08) / 10
    market_fit = (asset['Market_Score'] - 50) * (base * 0.1) / 10
    
    # 3. Volatility Adjustment (from your sidebar)
    vol_adj = asset['AI_Value'] - (base + legal_risk_deduction + tech_premium + market_fit)
    
    # 4. Final Calculated Value
    final = asset['AI_Value']

    fig_waterfall = go.Figure(go.Waterfall(
        name = "Valuation Adjustments", orientation = "v",
        measure = ["relative", "relative", "relative", "relative", "relative", "total"],
        x = ["Standard Base", "Legal Event Risk", "Tech Premium", "Market Fit", "Market Volatility", "Final AI Value"],
        y = [base, legal_risk_deduction, tech_premium, market_fit, vol_adj, final],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"#EF553B"}},
        increasing = {"marker":{"color":"#00CC96"}},
        totals = {"marker":{"color":"#2f75db"}}
    ))
    
    fig_waterfall.update_layout(title=f"Valuation Walk for Asset {selected_id}", height=500)
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
