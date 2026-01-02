import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="3D-PVE | Home",
    page_icon="💎",
    layout="wide"
)

# Custom CSS to make the landing page look like a website
st.markdown("""
<style>
    .main-header {
        font-size: 50px;
        font-weight: 700;
        color: #00CC96;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 24px;
        color: #B0B3D6;
        text-align: center;
        margin-bottom: 50px;
    }
    .feature-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown('<div class="main-header">3D-PVE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">The Future of Patent Valuation & Risk Assessment</div>', unsafe_allow_html=True)

st.divider()

# --- Value Proposition ---
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

# --- Call to Action ---
st.markdown("### ready to start?")
st.info("👈 **Select 'Valuation Engine' from the sidebar** to launch the dashboard.")

# --- Optional: Add an image if you have one ---
st.image("https://source.unsplash.com/random/1200x400/?technology")