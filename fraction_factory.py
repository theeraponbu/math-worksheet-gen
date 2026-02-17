import streamlit as st
import matplotlib.pyplot as plt

def draw_worksheet(title, school_name, teacher_name, num_probs, color, font_family):
    # สร้าง Figure ขนาด A4 (สัดส่วน 8.27 x 11.69 นิ้ว)
    fig = plt.figure(figsize=(8.27, 11.69))
    
    # 1. วาดส่วนหัว (Header)
    plt.text(0.5, 0.95, school_name, ha='center', va='center', fontsize=14, fontweight='bold', family=font_family)
    plt.text(0.5, 0.92, title, ha='center', va='center', fontsize=20, color=color, family=font_family)
    plt.text(0.1, 0.88, f"Teacher: {teacher_name}", ha='left', va='center', fontsize=10)
    plt.text(0.9, 0.88, "Name:____________________", ha='right', va='center', fontsize=10)
    plt.plot([0.05, 0.95], [0.86, 0.86], color='gray', lw=1) # เส้นคั่น

    # 2. วาดโจทย์ (Grid 4x3 = 12 ข้อ)
    rows, cols = 4, 3
    for i in range(num_probs):
        ax = fig.add_axes([0.1 + (i%cols)*0.3, 0.65 - (i//cols)*0.2, 0.2, 0.15])
        # สุ่มเศษส่วน (ในระบบจริงจะใช้ค่าที่กำหนดหรือสุ่ม)
        import random
        d = random.randint(2, 10)
        n = random.randint(1, d)
        
        ax.pie([1]*d, colors=[color if j < n else '#ffffff' for j in range(d)], 
               startangle=90, wedgeprops={'edgecolor': 'black'})
        ax.set_title(f"Q{i+1}: ____ / ____", fontsize=10, pad=0)
        ax.axis('off')

    plt.axis('off')
    return fig

def run_app():
    st.title("🧩 Fraction Factory: Pro Designer")
    
    # ดึงค่าสิทธิ์มาจาก main.py (เดี๋ยวเราใช้ฟังก์ชันเปิด/ปิดคุมทีหลัง)
    is_pro = True 

    with st.sidebar:
        st.header("📄 Worksheet Config")
        school = st.text_input("School Name", "My International School")
        teacher = st.text_input("Teacher Name", "Ms. Jane Doe")
        title = st.text_input("Worksheet Title", "Fraction Visuals")
        num_probs = st.slider("Number of Problems", 1, 12, 6)
        main_color = st.color_picker("Theme Color", "#3b82f6")

    # ส่วนแสดงผล
    st.subheader("📄 Full Page Preview (Ready to Print)")
    
    # เรียกฟังก์ชันวาดใบงาน
    fig = draw_worksheet(title, school, teacher, num_probs, main_color, 'sans-serif')
    
    # แสดงรูปใน Streamlit ให้เต็มความกว้าง
    st.pyplot(fig, use_container_width=True)

    # ปุ่มดาวน์โหลด
    st.button("📥 Download PDF (Pro Only)")
