import streamlit as st
import matplotlib.pyplot as plt

def draw_circle_fraction(num, den):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie([1]*den, colors=['#3b82f6' if i < num else '#ffffff' for i in range(den)], 
           startangle=90, wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    return fig

def run_app():
    st.title("🧩 Fraction Factory")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("Settings")
        model = st.radio("Model Type", ["Circle Model", "Bar Model"])
        den = st.number_input("Denominator", 1, 20, 4)
        num = st.number_input("Numerator", 0, den, 1)
        
    with col2:
        st.subheader("Visual Preview")
        fig = draw_circle_fraction(num, den)
        st.pyplot(fig)
        
    st.markdown("---")
    if st.button("Add to PDF Worksheet"):
        st.info("Feature available for Pro Subscribers.")
