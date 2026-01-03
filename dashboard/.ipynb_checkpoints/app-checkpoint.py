import streamlit as st
import sys
import os
from PIL import Image

# --- 1. SETUP PATHS & IMPORTS ---
# Add the project root to system path so we can import from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your Logic Engine
try:
    from src.sql_client import DataManager
except ImportError:
    # Fallback if running from a different directory context
    pass

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="3D-PVE | Home",
    page_icon="💎",
    layout="wide"
)

# --- 3. GLOBAL STATE MANAGEMENT (The "Switch") ---
# We store the selected mode in Session State so other pages can see it.
if 'data_mode' not in st.session_state:
    st.session_state['data_mode'] = "🟢 Mock Data (Safe)"

# --- 4. SIDEBAR CONTROLS ---
st.sidebar.title("⚙️ System Controls")
st.sidebar.info("Select your data source below. This setting applies to the whole app.")

# The Radio Button
selected_mode = st.sidebar.radio(
    "Data Connection Mode:",
    ["🟢 Mock Data (Safe)", "🟡 Static Data (Offline)", "🔴 Live Data Lake (Risky)"],
    index=0  # Default to Mock
)

# Update Session State when changed
st.session_state['data_mode'] = selected_mode

# Optional: Show connection status in sidebar
if "Live" in selected_mode:
    st.sidebar.warning("📡 Status: CONNECTED")
elif "Static" in selected_mode:
    st.sidebar.info("📂 Status: OFFLINE ARCHIVE")
else:
    st.sidebar.success("🧪 Status: SIMULATION")

st.sidebar.divider()
st.sidebar.markdown("© 2025 3D-PVE Team")


# --- 5. MAIN UI (Your Landing Page Design) ---

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 60px;
        font-weight: 700;
        background: -webkit-linear-gradient(#00CC96, #2E86C1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 24px;
        color: #B0B3D6;
        text-align: center;
        margin-bottom: 50px;
    }
    .feature-card {
        background-color: #1E1E1E;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #333;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        height: 100%;
    }
    .feature-card:hover {
        border-color: #00CC96;
        transform: translateY(-5px);
        transition: 0.3s;
    }
    h3 {
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="main-header">3D-PVE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">The Future of Patent Valuation & Risk Assessment</div>', unsafe_allow_html=True)

# System Status Banner (Visual Feedback for the Switch)
if "Live" in selected_mode:
    st.warning("⚠️ **SYSTEM NOTICE:** Live Data Connection Active. Queries may take time.")
elif "Static" in selected_mode:
    st.info("ℹ️ **SYSTEM NOTICE:** Running in Offline Mode (Using Snapshot Data).")

st.divider()

# Value Proposition
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🚀 AI-Powered</h3>
        <p>Utilizes Ridge Regression and Heuristic Scoring to predict asset value with 92% accuracy.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🧊 Multidimensional</h3>
        <p>Visualizes Legal, Technical, and Market risks in an interactive 3D space.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🏦 Enterprise Grade</h3>
        <p>Built for IP Law Firms and Venture Capitalists to audit portfolios in seconds.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Call to Action
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown("### 🎯 Ready to start?")
    st.info(f"Current Mode: **{selected_mode}**\n\n👈 **Select 'Valuation Engine' from the sidebar** to launch the dashboard.")

# Optional Image (Cleaned up placeholder)
st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&q=80", caption="Powered by EPO PATSTAT Data Lake")