import streamlit as st

st.sidebar.title("MathPrepAI Menu")
choice = st.sidebar.radio("เลือกเครื่องมือ:", ["หน้าแรก", "🧩 Fraction Factory", "เครื่องมือเดิม"])

if choice == "🧩 Fraction Factory":
    import fraction_factory
    # เรียกใช้ฟังก์ชันหลักจากไฟล์เศษส่วน
elif choice == "หน้าแรก":
    st.title("ยินดีต้อนรับสู่ MathPrepAI Pro")
    st.write("กรุณาเลือกเครื่องมือที่ด้านซ้ายมือครับ")
