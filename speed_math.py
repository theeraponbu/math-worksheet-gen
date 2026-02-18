import streamlit as st
import streamlit.components.v1 as components
import random
from fpdf import FPDF
import io
import os

# --- 1. MATH LOGIC ENGINE (UNIQUE & REGROUPING CONTROL) ---
def check_regrouping(a, b):
    """Check if addition of a and b requires regrouping (carrying)."""
    temp_a, temp_b = a, b
    while temp_a > 0 or temp_b > 0:
        if (temp_a % 10) + (temp_b % 10) >= 10:
            return True
        temp_a //= 10
        temp_b //= 10
    return False

def generate_math_data(num_probs, difficulty, mode):
    """Generate unique problems based on level and regrouping mode."""
    problems = []
    seen = set()
    
    if difficulty == "Easy":
        low, high = 1, 9
    elif difficulty == "Medium":
        low, high = 10, 99
    else: # Hard
        low, high = 100, 999

    # Safety break to avoid infinite loop
    max_possibilities = (high - low + 1)**2
    target_num = min(num_probs, max_possibilities)

    while len(problems) < target_num:
        a = random.randint(low, high)
        b = random.randint(low, high)
        
        if (a, b) in seen:
            continue
            
        has_regrouping = check_regrouping(a, b)
        
        # Mode Logic: "Always", "Never", or "Mixed"
        should_add = False
        if mode == "Always Regrouping" and has_regrouping:
            should_add = True
        elif mode == "Never Regrouping" and not has_regrouping:
            should_add = True
        elif mode == "Mixed (Both)":
            should_add = True
            
        if should_add:
            problems.append({"a": a, "b": b})
            seen.add((a, b))
            
    return problems

# --- 2. PDF ENGINE (MULTI-FILE EXPORT) ---
class MathWorksheetPDF(FPDF):
    def __init__(self, paper_format='Letter'):
        super().__init__(orientation='P', unit='mm', format=paper_format)
        self.set_auto_page_break(auto=True, margin=15)

    def generate_content(self, problems, title, school, teacher, f_size, is_key=False):
        self.add_page()
        
        # Header Section
        self.set_font('Courier', 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font('Courier', 'B', f_size + 2)
        self.cell(0, 15, f"{title}{' (Answer Key)' if is_key else ''}", ln=True, align='C')
        
        # Info Section
        self.set_font('Courier', '', 11)
        self.cell(90, 10, f"Teacher: {teacher}")
        self.cell(0, 10, "Name: ________________ Score: ____", align='R', ln=True)
        self.line(10, 50, self.w - 10, 50)

        # Grid Settings
        x_start, y_start = 20, 65
        col_w, row_h = (self.w - 40)/4, 35
        
        for idx, p in enumerate(problems):
            col = idx % 4
            row = (idx // 4) % 6 # Reset row position per page (approx 6 rows per page)
            
            # Auto Page Break Handling
            if idx > 0 and idx % 24 == 0:
                self.add_page()
                # Re-draw line on new page for professional look
                self.line(10, 20, self.w - 10, 20)
                y_start = 30 
            
            x = x_start + (col * col_w)
            y = y_start + (row * row_h) if idx < 24 else 30 + (row * row_h)
            
            self.set_xy(x, y)
            self.set_font('Courier', '', 9); self.cell(5, 5, f"{idx+1})")
            self.set_font('Courier', 'B', f_size)
            self.set_xy(x+5, y); self.cell(20, 10, f"{p['a']:>3}", align='R', ln=True)
            self.set_xy(x+5, y+8); self.cell(20, 10, f"+ {p['b']:>2}", align='R', ln=True)
            self.set_line_width(0.6)
            self.line(x+10, y+19, x+25, y+19)
            
            if is_key:
                self.set_text_color(220, 0, 0)
                self.set_xy(x+5, y+21); self.cell(20, 10, f"{p['a']+p['b']:>3}", align='R')
                self.set_text_color(0, 0, 0)

# --- 3. STREAMLIT APP UI ---
def run_app():
    st.set_page_config(page_title="MathPrepAI Pro", layout="wide")
    st.title("⚡ MathPrepAI: Professional Worksheet Builder")

    with st.sidebar:
        st.header("📏 Layout Configuration")
        paper = st.selectbox("Paper Format", ["Letter", "A4"])
        f_size = st.slider("Problem Font Size", 16, 32, 24)
        
        st.header("🔢 Math Logic")
        diff = st.radio("Difficulty Level", ["Easy (1-Digit)", "Medium (2-Digits)", "Hard (3-Digits)"])
        # Updated regrouping options
        regroup_mode = st.selectbox("Regrouping Mode", 
                                  ["Mixed (Both)", "Never Regrouping", "Always Regrouping"])
        
        num_probs = st.number_input("Total Problems", 12, 120, 48, step=12)
        
        st.header("🏫 Branding & Label")
        school = st.text_input("School Name", "Global Math Academy")
        teacher = st.text_input("Teacher Name", "Mr. Smith")
        title = st.text_input("Worksheet Title", "Vertical Addition")

    # Generate or Reshuffle
    if 'current_problems' not in st.session_state or st.button("🔀 Generate New Problems"):
        level = diff.split(" ")[0]
        st.session_state.current_problems = generate_math_data(num_probs, level, regroup_mode)

    # --- Smart Layout Check ---
    probs_per_page = 24
    total_pages = (len(st.session_state.current_problems) - 1) // probs_per_page + 1
    st.sidebar.info(f"📊 Layout Status: {total_pages} Page(s) will be generated.")

    # --- Preview Section ---
    st.subheader("📄 Live Worksheet Preview")
    
    # Simple CSS for Preview
    aspect = 1.29 if paper == "Letter" else 1.41
    items_html = "".join([f"""
        <div style="width: 20%; padding: 15px; font-family: monospace; font-size: {f_size}px; font-weight: bold; text-align: right;">
            <div style="font-size: 10px; color: gray; text-align: left;">{i+1})</div>
            {p['a']}<br>+ {p['b']}<br><hr style="border: 2px solid black; margin: 2px 0;">
        </div>
    """ for i, p in enumerate(st.session_state.current_problems[:12])]) # Show only first 12 for preview

    preview_html = f"""
    <div style="background: white; padding: 40px; border: 1px solid #ccc; width: 100%; min-height: 400px; color: black;">
        <div style="text-align: center; border-bottom: 2px solid black; margin-bottom: 20px;">
            <h2 style="margin: 0;">{school.upper()}</h2>
            <h3 style="margin: 5px 0;">{title}</h3>
        </div>
        <div style="display: flex; flex-wrap: wrap; justify-content: space-around;">{items_html}</div>
        <div style="margin-top: 20px; text-align: center; color: #888; font-style: italic;">... Previewing first 12 problems ...</div>
    </div>
    """
    st.components.v1.html(preview_html, height=500, scrolling=True)

    # --- Export Section ---
    st.markdown("---")
    st.subheader("📥 Export Final Files")
    col1, col2 = st.columns(2)
    
    with col1:
        # Worksheet Export
        pdf_ws = MathWorksheetPDF(paper_format=paper)
        pdf_ws.generate_content(st.session_state.current_problems, title, school, teacher, f_size, is_key=False)
        st.download_button(
            label="📝 Download Worksheet (PDF)",
            data=bytes(pdf_ws.output()),
            file_name=f"{title.replace(' ', '_')}_Worksheet.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with col2:
        # Answer Key Export
        pdf_key = MathWorksheetPDF(paper_format=paper)
        pdf_key.generate_content(st.session_state.current_problems, title, school, teacher, f_size, is_key=True)
        st.download_button(
            label="🔑 Download Answer Key (PDF)",
            data=bytes(pdf_key.output()),
            file_name=f"{title.replace(' ', '_')}_Answer_Key.pdf",
            mime="application/pdf",
            use_container_width=True
        )

if __name__ == "__main__":
    run_app()
