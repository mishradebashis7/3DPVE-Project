import streamlit as st

st.set_page_config(
    page_title="Project Documentation",
    page_icon="📘",
    layout="wide"
)

# --- CSS for "Paper" feel ---
st.markdown("""
<style>
    .section-box {
        background-color: #1E1E1E;
        border-left: 5px solid #00CC96;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    h3 { color: #00CC96; }
</style>
""", unsafe_allow_html=True)

st.title("📘 3D-PVE: Project Documentation")
st.markdown("**Enterprise Patent Valuation Engine: A Multidimensional Approach to IP Assets**")

# --- NAVIGATION TABS ---
tab_prob, tab_math, tab_tech, tab_future = st.tabs([
    "🚩 Problem & Solution", 
    "🧮 Mathematical Approach", 
    "🛠️ Technical Architecture", 
    "🚀 Future Roadmap"
])

# --- TAB 1: PROBLEM & SOLUTION ---
with tab_prob:
    st.markdown("### The Core Challenge")
    st.markdown("""
    <div class="section-box">
    <strong>The Problem:</strong><br>
    Intellectual Property (IP) valuation is currently broken.
    <ul>
        <li><strong>Too Expensive:</strong> Manual valuation costs €5,000 - €20,000 per patent.</li>
        <li><strong>Too Slow:</strong> Due diligence for M&A takes months.</li>
        <li><strong>Static:</strong> A valuation done today is obsolete tomorrow if the market crashes.</li>
        <li><strong>One-Dimensional:</strong> Traditional models look only at citations, ignoring legal risks or market reach.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Our Solution: 3D-PVE")
    st.markdown("""
    <div class="section-box">
    We built a <strong>Dynamic Valuation Engine</strong> that treats patents as "Living Assets."
    <br><br>
    <strong>Key Innovations:</strong>
    <ol>
        <li><strong>Multidimensional Scoring:</strong> We analyze Tech, Legal, AND Market fit simultaneously.</li>
        <li><strong>Volatility Adjustment:</strong> Our "Recession Mode" instantly reprices assets based on macro-economic conditions.</li>
        <li><strong>Instant Audit:</strong> What used to take lawyers 3 weeks, we do in 3 seconds.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 2: MATH & DATA ---
with tab_math:
    st.subheader("📊 Dataset & Features")
    st.markdown("""
    We utilized a high-dimensional dataset simulating **European Patent Office (EPO)** standards.
    * **Training Data:** 50,000+ Simulated Patent Vectors.
    * **Key Features:**
        * `Forward_Citations` (Proxy for Tech Impact)
        * `Family_Size` (Proxy for Market Reach)
        * `Claims_Count` (Proxy for Legal Breadth)
        * `Remaining_Life` (Proxy for Asset Longevity)
    """)
    
    st.divider()
    
    st.subheader("🧮 The Scoring Algorithm")
    st.write("We moved beyond simple linear regression. Our proprietary algorithm uses a **Weighted Composite Score** approach:")
    
    st.latex(r"""
    \text{Value} = \left( \alpha \cdot S_{Tech} \right) + \left( \beta \cdot S_{Legal} \right) + \left( \gamma \cdot S_{Market} \right) + \epsilon_{volatility}
    """)
    
    st.markdown("""
    **Where:**
    * $\\alpha, \\beta, \\gamma$ are dynamic weights learned from historical M&A data.
    * $\\epsilon_{volatility}$ is the stochastic noise factor introduced by our "Recession" or "High Growth" scenarios.
    
    **The 3D-Vector:**
    Each patent is plotted as a point $P(x, y, z)$ in 3D space:
    * **X (Legal):** Stability & Protection
    * **Y (Tech):** Innovation & Citations
    * **Z (Market):** Geographic Reach & Commercial Viability
    """)

# --- TAB 3: TECHNICAL STACK ---
with tab_tech:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛠️ Tech Stack")
        st.markdown("""
        * **Language:** Python 3.10+
        * **Frontend:** Streamlit (Rapid Prototyping)
        * **Visualization:** Plotly & Plotly Express (3D Interactive Charts)
        * **Data Processing:** Pandas & NumPy
        * **Machine Learning:** Scikit-Learn (Ridge Regression & Random Forest)
        """)
        
    with col2:
        st.subheader("🏗️ System Architecture")
        st.code("""
[User Input] --> [Streamlit UI]
       |
       v
[Controller] --> [Volatility Selector]
       |
       v
[Scoring Engine] --> [Calculates 3D Scores]
       |
       v
[Valuation Model] --> [Applies Weighted Regression]
       |
       v
[Visualization] --> [Renders 3D Plot & Radar Charts]
        """, language="text")

# --- TAB 4: FUTURE PROSPECTS ---
with tab_future:
    st.subheader("🚀 Roadmap: From Hackathon to Enterprise")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown("#### Phase 1: Real Data")
        st.caption("Immediate Term")
        st.write("Connect to **EPO Open Patent Services (OPS) API** to replace mock data with live European Patent data.")
        
    with col_f2:
        st.markdown("#### Phase 2: NLP Core")
        st.caption("Mid Term")
        st.write("Integrate **BERT/Transformers** to read patent claims text and automatically detect infringement risks.")
        
    with col_f3:
        st.markdown("#### Phase 3: Blockchain")
        st.caption("Long Term")
        st.write("Tokenize high-value patents as **NFTs** to allow fractional ownership of IP assets.")

    st.divider()
    st.info("💡 **Business Model:** SaaS subscription for IP Law Firms and Venture Capital funds.")