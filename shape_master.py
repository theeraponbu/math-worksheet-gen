import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

def draw_geometry(shape_type, val1, val2=None):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_aspect('equal')
    plt.axis('off')

    if shape_type == "Rectangle":
        # Draw Rectangle (val1=width, val2=height)
        rect = patches.Rectangle((0.1, 0.3), 0.8, 0.4, linewidth=2, edgecolor='#1e293b', facecolor='#f8fafc')
        ax.add_patch(rect)
        ax.text(0.5, 0.25, f"w = {val1}", ha='center', fontsize=12)
        ax.text(0.05, 0.5, f"h = {val2}", va='center', rotation='vertical', fontsize=12)
        
    elif shape_type == "Triangle":
        # Draw Right Triangle (val1=base, val2=height)
        points = [[0.2, 0.2], [0.8, 0.2], [0.2, 0.8]]
        tri = patches.Polygon(points, linewidth=2, edgecolor='#1e293b', facecolor='#f8fafc')
        ax.add_patch(tri)
        ax.text(0.5, 0.15, f"b = {val1}", ha='center', fontsize=12)
        ax.text(0.15, 0.5, f"h = {val2}", va='center', rotation='vertical', fontsize=12)

    elif shape_type == "Circle":
        # Draw Circle (val1=radius)
        circle = patches.Circle((0.5, 0.5), 0.3, linewidth=2, edgecolor='#1e293b', facecolor='#f8fafc')
        ax.add_patch(circle)
        ax.plot([0.5, 0.8], [0.5, 0.5], color='#1e293b', linestyle='--') # Radius line
        ax.text(0.65, 0.55, f"r = {val1}", ha='center', fontsize=12)

    return fig

def run_app():
    st.title("📐 Shape Master")
    st.write("Generate geometric shapes for Area and Perimeter problems.")

    with st.sidebar.expander("🛠️ Shape Configuration", expanded=True):
        shape = st.selectbox("Select Shape", ["Rectangle", "Triangle", "Circle"])
        
        if shape in ["Rectangle", "Triangle"]:
            v1 = st.number_input("Dimension 1 (Base/Width)", 1, 100, 10)
            v2 = st.number_input("Dimension 2 (Height)", 1, 100, 5)
        else:
            v1 = st.number_input("Radius", 1, 100, 7)
            v2 = None

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Visual Preview")
        fig = draw_geometry(shape, v1, v2)
        st.pyplot(fig)

    with col2:
        st.subheader("Calculated Answer (Hidden)")
        if shape == "Rectangle":
            area = v1 * v2
            peri = 2 * (v1 + v2)
        elif shape == "Triangle":
            area = 0.5 * v1 * v2
            peri = "Calculated in Pro version"
        else:
            import math
            area = round(math.pi * (v1**2), 2)
            peri = round(2 * math.pi * v1, 2)
            
        st.write(f"**Area:** {area}")
        st.write(f"**Perimeter:** {peri}")

    st.markdown("---")
    if st.button("Generate Random Problem Set (Pro)"):
        st.warning("This feature requires a Pro Subscription.")
