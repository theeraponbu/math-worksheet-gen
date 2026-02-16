import streamlit as st
import random
import pandas as pd

def run_app():
    st.title("⚡ Speed Math Drills")
    
    with st.expander("⚙️ Worksheet Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            op = st.selectbox("Operation", ["Addition", "Subtraction", "Multiplication", "Division"])
            count = st.slider("Number of Problems", 10, 50, 20)
        with col2:
            level = st.select_slider("Difficulty", options=["Basic", "Intermediate", "Advanced"])

    if st.button("Generate Worksheet"):
        # Logic for random numbers based on level
        st.write("---")
        st.subheader("Preview: Math Drill Worksheet")
        # Example Table
        data = [{"No.": i+1, "Problem": "Check Pro Version", "Answer": ""} for i in range(5)]
        st.table(pd.DataFrame(data))
        st.warning("⚠️ Upgrade to Pro to download the full PDF version.")
