import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def draw_graph(function_type, a, b, c):
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Create grid system
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#cbd5e1')
    ax.axhline(y=0, color='#1e293b', linewidth=1.5)
    ax.axvline(x=0, color='#1e293b', linewidth=1.5)
    
    x = np.linspace(-10, 10, 400)
    
    if function_type == "Linear (y = mx + c)":
        # y = ax + b
        y = a * x + b
        label = f"y = {a}x + {b}"
    else:
        # y = ax^2 + bx + c
        y = a * (x**2) + b * x + c
        label = f"y = {a}x² + {b}x + {c}"
        
    ax.plot(x, y, color='#3b82f6', label=label, linewidth=2)
    ax.legend()
    return fig

def run_app():
    st.title("📉 Graphing Notebook")
    st.write("Professional coordinate planes and function plotting for secondary education.")

    with st.sidebar.expander("📊 Function Settings", expanded=True):
        f_type = st.selectbox("Function Type", ["Linear (y = mx + c)", "Quadratic (y = ax² + bx + c)"])
        
        if f_type == "Linear (y = mx + c)":
            val_a = st.number_input("Slope (m)", value=1.0)
            val_b = st.number_input("Intercept (c)", value=0.0)
            val_c = 0
        else:
            val_a = st.number_input("Coefficient (a)", value=1.0)
            val_b = st.number_input("Coefficient (b)", value=0.0)
            val_c = st.number_input("Constant (c)", value=0.0)

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("Graph Preview")
        fig = draw_graph(f_type, val_a, val_b, val_c)
        st.pyplot(fig)

    with col2:
        st.subheader("Table of Values")
        # Generate simple x, y points for the table
        x_points = np.array([-2, -1, 0, 1, 2])
        if f_type == "Linear (y = mx + c)":
            y_points = val_a * x_points + val_b
        else:
            y_points = val_a * (x_points**2) + val_b * x_points + val_c
        
        df = {"x": x_points, "y": y_points}
        st.dataframe(df, use_container_width=True)
        st.info("💡 Use these points to teach students how to plot coordinates.")

    st.markdown("---")
    if st.button("Export Graph to PDF Worksheet (Pro)"):
        st.warning("Downloadable high-resolution grids are available for Pro Members.")
