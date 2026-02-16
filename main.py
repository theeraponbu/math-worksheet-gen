import streamlit as st
import speed_math
import fraction_factory

# UI Configuration
st.set_page_config(page_title="MathPrepAI Workspace", layout="wide", page_icon="🎓")

# Professional Sidebar
st.sidebar.title("🎓 MathPrepAI Global")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "SELECT TOOL:",
    ["🏠 Home", "⚡ Speed Math Drills", "🧩 Fraction Factory", "📐 Shape Master"]
)

if menu == "🏠 Home":
    st.title("Welcome to MathPrepAI Pro Workspace")
    st.markdown("""
    ### Empowering Educators Globally
    Select a module from the sidebar to begin generating professional math resources.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("#### ⚡ Speed Math Drills\nCreate timed arithmetic worksheets with customizable difficulty levels.")
    with col2:
        st.success("#### 🧩 Fraction Factory\nGenerate visual fraction models (Circle & Bar) for conceptual teaching.")

elif menu == "⚡ Speed Math Drills":
    speed_math.run_app()

elif menu == "🧩 Fraction Factory":
    fraction_factory.run_app()

elif menu == "📐 Shape Master":
    import shape_master
    shape_master.run_app()
