import streamlit as st

st.set_page_config(page_title="AI Logic", page_icon="🧠")

st.title("🧠 Under the Hood: The AI Architecture")

st.markdown("""
### How 3D-PVE calculates value
Unlike traditional linear models, we use a **Composite Scoring System**:

1.  **The Inputs:**
    * *Forward Citations:* Measures technological impact.
    * *Claim Count:* Measures legal breadth.
    * *Family Size:* Measures market reach.

2.  **The Algorithm:**
    We treat the valuation as a regression problem:
""")

# FIX: Added 'r' before the string to handle \epsilon correctly
st.latex(r"Value = \alpha (Tech) + \beta (Legal) + \gamma (Market) + \epsilon")

st.markdown("""
    * **Tech Score:** Citations × 2 + Claims
    * **Legal Score:** RemainingLife × 4
    * **Market Score:** FamilySize × 5

3.  **The Output:**
    A unified financial metric (in Euros) used for M&A due diligence.
""")

st.info("This modular architecture allows us to swap in Deep Learning models (like BERT for text analysis) in future versions.")