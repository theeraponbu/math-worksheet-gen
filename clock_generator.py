import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def draw_clock(hour, minute, show_hands=True):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_aspect('equal')
    
    # Draw Clock Face
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=2, color='#1e293b')
    ax.add_patch(circle)
    
    # Draw Numbers 1-12
    for i in range(1, 13):
        angle = np.deg2rad(90 - i * 30)
        x = 0.85 * np.cos(angle)
        y = 0.85 * np.sin(angle)
        ax.text(x, y, str(i), ha='center', va='center', fontsize=12, fontweight='bold')
        
    # Draw Ticks (Minutes)
    for i in range(60):
        angle = np.deg2rad(i * 6)
        x1, y1 = np.cos(angle), np.sin(angle)
        x2, y2 = 0.95 * np.cos(angle), 0.95 * np.sin(angle)
        ax.plot([x1, x2], [y1, y2], color='#1e293b', linewidth=1)

    if show_hands:
        # Minute Hand
        m_angle = np.deg2rad(90 - minute * 6)
        ax.plot([0, 0.75 * np.cos(m_angle)], [0, 0.75 * np.sin(m_angle)], color='#3b82f6', linewidth=3)
        
        # Hour Hand (Includes minute offset)
        h_angle = np.deg2rad(90 - (hour * 30 + minute * 0.5))
        ax.plot([0, 0.5 * np.cos(h_angle)], [0, 0.5 * np.sin(h_angle)], color='#1e293b', linewidth=5)
        
    # Center Point
    ax.add_patch(plt.Circle((0, 0), 0.03, color='black'))
    
    plt.axis('off')
    return fig

def run_app():
    st.title("🕒 Time & Clock Generator")
    st.write("Create professional clock faces for telling time activities.")

    with st.sidebar.expander("⏱️ Clock Settings", expanded=True):
        mode = st.radio("Activity Mode", ["Tell the Time (Show Hands)", "Draw the Hands (Empty Face)"])
        st.markdown("---")
        hour = st.slider("Hour", 1, 12, 10)
        minute = st.slider("Minute", 0, 59, 10)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Clock Preview")
        show_h = True if "Tell the Time" in mode else False
        fig = draw_clock(hour, minute, show_h)
        st.pyplot(fig)

    with col2:
        st.subheader("Worksheet Info")
        st.write(f"**Target Time:** {hour:02d}:{minute:02d}")
        if not show_h:
            st.info("💡 Student will see an empty clock and must draw hands for the time above.")
        else:
            st.success("💡 Student must look at the hands and write the correct time.")

    st.markdown("---")
    if st.button("Generate Randomized Worksheet (Pro)"):
        st.warning("Bulk worksheet generation with multiple clocks is a Pro feature.")
