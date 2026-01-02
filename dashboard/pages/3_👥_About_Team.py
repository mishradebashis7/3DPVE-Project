import streamlit as st

st.set_page_config(page_title="Team", page_icon="👥")

st.title("👥 The Team Behind 3D-PVE")
st.markdown("### Built for the [Hackathon Name] 2026")

st.divider()

# --- Team Member 1 ---
col1, col2 = st.columns([1, 3])
with col1:
    # You can replace this URL with your actual LinkedIn profile picture URL
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=150)
with col2:
    st.subheader("Your Name")
    st.markdown("**Lead Developer & AI Architect**")
    st.write("""
    Responsible for the machine learning pipeline, 3D visualization integration, 
    and backend architecture. Passionate about applying AI to legal-tech problems.
    """)
    st.markdown("[GitHub](https://github.com/mishradebashis7) | [LinkedIn](#)")

st.divider()

# --- Team Member 2 ---
col3, col4 = st.columns([1, 3])
with col3:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140037.png", width=150)
with col4:
    st.subheader("Teammate Name")
    st.markdown("**Data Scientist / UI Designer**")
    st.write("""
    Focused on the user experience (UX) and financial modeling. ensured the 
    dashboard meets the needs of enterprise IP lawyers.
    """)
    st.markdown("[GitHub](#) | [LinkedIn](#)")

st.divider()

# --- Team Member 3  ---
col3, col4 = st.columns([1, 3])
with col3:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140037.png", width=150)
with col4:
    st.subheader("Teammate Name")
    st.markdown("**Data Scientist / UI Designer**")
    st.write("""
    Focused on the user experience (UX) and financial modeling. ensured the 
    dashboard meets the needs of enterprise IP lawyers.
    """)
    st.markdown("[GitHub](#) | [LinkedIn](#)")

st.divider()


# --- Project Goals ---
st.subheader("🏆 Project Mission")
st.info("""
**Our Goal:** To democratize patent valuation by replacing expensive, subjective 
human audits with transparent, data-driven AI models.
""")

st.subheader("🛠 Tech Stack")
st.markdown("""
* **Frontend:** Streamlit (Python)
* **Visualization:** Plotly & Plotly Express (3D Engine)
* **Machine Learning:** Scikit-Learn (Ridge Regression)
* **Data Processing:** Pandas & NumPy
""")