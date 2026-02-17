import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def draw_clock(hour, minute, show_hands=True, theme_color='#1e293b', style="Classic"):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_aspect('equal')
    
    # Draw Clock Face based on Style
    if style == "Modern Minimal":
        circle = plt.Circle((0, 0), 1, fill=True, color='#f8fafc', linewidth=2, edgecolor=theme_color)
    else:
        circle = plt.Circle((0, 0), 1, fill=False, linewidth=2, color=theme_color)
    ax.add_patch(circle)
    
    # Draw Numbers
    for i in range(1, 13):
        angle = np.deg2rad(90 - i * 30)
        x, y = 0.85 * np.cos(angle), 0.85 * np.sin(angle)
        ax.text(x, y, str(i), ha='center', va='center', fontsize=12, fontweight='bold', color=theme_color)

    if show_hands:
        m_angle = np.deg2rad(90 - minute * 6)
        h_angle = np.deg2rad(90 - (hour * 30 + minute * 0.5))
        # Minute Hand
        ax.plot([0, 0.75 * np.cos(m_angle)], [0, 0.75 * np.sin(m_angle)], color='#3b82f6', linewidth=3)
        # Hour Hand
        ax.plot([0, 0.5 * np.cos(h_angle)], [0, 0.5 * np.sin(h_angle)], color=theme_color, linewidth=5)
    
    ax.add_patch(plt.Circle((0, 0), 0.03, color='black'))
    plt.axis('off')
    return fig

def run_app():
    st.title("🕒 Time & Clock Master")
    is_pro = st.session_state.get('is_pro', False)

    # --- TEMPLATE SELECTION ---
    st.subheader("🎨 Select Template Style")
    tpl_choice = st.selectbox("Template Library:", [
        "Basic Practice (Free)", 
        "⭐ Pro: Exam Layout (2-Column)", 
        "⭐ Pro: Colorful Classroom (Credit)", 
        "⭐ Pro: Minimalist Designer (Credit)"
    ])

    is_locked = "Pro" in tpl_choice and not is_pro

    if is_locked:
        st.warning("🔒 This Premium Template requires a Pro membership or 1 Credit.")
        st.image("https://via.placeholder.com/500x250?text=Premium+Clock+Template+Preview", caption="Unlock to access high-quality layout")
    else:
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.subheader("Clock Config")
            hour = st.slider("Hour", 1, 12, 10)
            minute = st.slider("Minute", 0, 59, 15)
            style = "Modern Minimal" if "Minimalist" in tpl_choice else "Classic"
            color = st.color_picker("Clock Theme Color", "#1e293b") if is_pro else "#1e293b"

        with col2:
            st.subheader("Worksheet Preview")
            # --- Layout Engine based on Template ---
            if "Basic" in tpl_choice:
                st.write("### Telling Time Practice")
                st.pyplot(draw_clock(hour, minute, True, color, style))
                st.write("Write the time: ________________")
            
            elif "Exam Layout" in tpl_choice:
                st.write("### UNIT TEST: TIME")
                c1, c2 = st.columns(2)
                with c1: st.pyplot(draw_clock(hour, minute, True, color, style))
                with c2: st.pyplot(draw_clock((hour+2)%12, (minute+15)%60, True, color, style))
                st.write("---")
                st.caption("Pro Feature: Automatic Answer Key generation included.")

    st.markdown("---")
    if st.button("Download as PDF"):
        if is_pro:
            st.success("Preparing your high-quality PDF...")
        else:
            st.error("Access Denied: Please upgrade to Pro or use Credits to download.")
