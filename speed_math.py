import streamlit as st
import random
import pandas as pd

def run_app():
    st.title("⚡ Speed Math Drills")
    st.subheader("สร้างโจทย์คิดเลขเร็วแบบสุ่ม (บวก ลบ คูณ หาร)")

    # --- ส่วนการตั้งค่าโจทย์ ---
    with st.expander("⚙️ ตั้งค่าระดับความยาก", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            operation = st.selectbox("เลือกเครื่องหมาย", ["+", "-", "×", "÷", "ระคน (สุ่ม)"])
            num_questions = st.slider("จำนวนข้อ", 10, 50, 20)
        with col2:
            difficulty = st.select_slider("ระดับความยาก", options=["ง่าย (1-9)", "กลาง (10-99)", "ยาก (100-999)"])

    # --- ตรรกะการสุ่มเลขตามระดับความยาก ---
    if difficulty == "ง่าย (1-9)":
        range_min, range_max = 1, 9
    elif difficulty == "กลาง (10-99)":
        range_min, range_max = 10, 99
    else:
        range_min, range_max = 100, 999

    # --- ปุ่มสร้างโจทย์ ---
    if st.button("🚀 Generate โจทย์ใหม่"):
        questions = []
        ops_map = {"+": "+", "-": "-", "×": "×", "÷": "÷"}
        
        for i in range(1, num_questions + 1):
            a = random.randint(range_min, range_max)
            b = random.randint(range_min, range_max)
            
            # เลือกเครื่องหมาย
            current_op = operation
            if operation == "ระคน (สุ่ม)":
                current_op = random.choice(["+", "-", "×", "÷"])
            
            # ปรับแต่งโจทย์ให้เหมาะสม
            if current_op == "-": # ป้องกันติดลบ (สำหรับเด็กประถม)
                a, b = max(a, b), min(a, b)
            elif current_op == "÷": # ป้องกันหารไม่ลงตัว
                b = random.randint(2, 9)
                a = b * random.randint(range_min, 10 if difficulty == "ง่าย (1-9)" else 50)
            
            questions.append({"ข้อที่": i, "โจทย์": f"{a} {current_op} {b} =", "คำตอบ": ""})
        
        # แสดงผลเป็นตารางในหน้าเว็บ
        df = pd.DataFrame(questions)
        st.table(df[["ข้อที่", "โจทย์"]])
        
        st.success("✨ สร้างโจทย์สำเร็จ! อาจารย์สามารถคัดลอกไปวางใน Word หรือจดบนกระดานได้เลยครับ")

# เรียกใช้แอป
if __name__ == "__main__":
    run_app()
