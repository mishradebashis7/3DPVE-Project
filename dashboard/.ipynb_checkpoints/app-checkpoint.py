import streamlit as st
import plotly.graph_objects as go
import sys
import os

# Allow importing from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.scoring_engine import PatentValueEngine

# Init
engine = PatentValueEngine()

st.title("3D-PVE: Patent Valuation Engine")

# --- SWITCHER ---
mode = st.radio("Select Model Mode:", ('Heuristic', 'ML_Optimized'), horizontal=True)
engine.set_model_mode(mode)

st.caption(f"Current Weights: α={engine.alpha}, β={engine.beta}")

# --- INPUTS ---
col1, col2 = st.columns(2)
with col1:
    legal = st.selectbox("Legal Event", ['No Challenge', 'Opposition (Survived)', 'Revocation'])
    family = st.slider("Family Size", 1, 50, 10)
with col2:
    years = st.slider("Years Active", 1, 20, 5)
    div = st.slider("Tech Diversity", 0.0, 1.0, 0.5)

# --- CALC ---
s_leg = engine.calculate_legal_score(legal)
s_eco = engine.calculate_economic_score(family, years)
s_tech = engine.calculate_tech_score(div)
v_cp = engine.get_composite_score(s_leg, s_eco, s_tech)

# --- RADAR ---
fig = go.Figure(data=go.Scatterpolar(
    r=[s_leg*2, s_eco, s_tech*2],
    theta=['Legal', 'Economic', 'Tech'],
    fill='toself'
))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=300)

st.metric("Final Value (Vcp)", f"{v_cp:.2f}")
st.plotly_chart(fig)