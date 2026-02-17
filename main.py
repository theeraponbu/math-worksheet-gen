if menu == "🏠 Home":
    st.title("Welcome to MathPrepAI Pro")
    st.write("Select a tool to start creating your materials.")

    # สร้าง Grid 3 คอลัมน์ สำหรับ 6 เครื่องมือ
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("### ⚡ Speed Math\nArithmetic drills generator.")
        if st.button("Launch Speed Math", key="btn1"):
            st.session_state.menu_choice = "⚡ Speed Math Drills"
            st.rerun()

    with col2:
        st.success("### 🧩 Fraction Factory\nVisual fraction models.")
        if st.button("Launch Fraction Factory", key="btn2"):
            st.session_state.menu_choice = "🧩 Fraction Factory"
            st.rerun()

    with col3:
        st.warning("### 📐 Shape Master\nGeometry & area tools.")
        if st.button("Launch Shape Master", key="btn3"):
            st.session_state.menu_choice = "📐 Shape Master"
            st.rerun()

    # แถวที่ 2
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    with row2_col1:
        st.error("### 📉 Graphing\nCoordinate plane plotter.")
        if st.button("Launch Graphing", key="btn4"):
            st.session_state.menu_choice = "📉 Graphing Notebook"
            st.rerun()

    with row2_col2:
        st.help("### 🕒 Time & Clock\nAnalog clock generator.")
        if st.button("Launch Clock", key="btn5"):
            st.session_state.menu_choice = "🕒 Time & Clock"
            st.rerun()

    with row2_col3:
        st.write("### 📑 PDF Editor\nMerge & Split tools.")
        st.button("Upgrade to Pro", key="btn6", disabled=True)
