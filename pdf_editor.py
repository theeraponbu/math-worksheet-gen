import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import io

def run_app():
    st.title("📑 PDF Editor & Merger")
    st.write("Professional tools to manage and combine your educational worksheets.")

    tabs = st.tabs(["🔗 Merge PDFs", "✂️ Split PDF", "🛡️ Add Watermark"])

    # --- Tab 1: Merge PDFs ---
    with tabs[0]:
        st.subheader("Merge Multiple Worksheets")
        uploaded_files = st.file_uploader("Upload PDF files to merge", type="pdf", accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("Merge & Download (Pro)"):
                merger = PdfWriter()
                for pdf in uploaded_files:
                    merger.append(pdf)
                
                output = io.BytesIO()
                merger.write(output)
                st.download_button(
                    label="📥 Download Merged PDF",
                    data=output.getvalue(),
                    file_name="combined_worksheets.pdf",
                    mime="application/pdf"
                )

    # --- Tab 2: Split PDF ---
    with tabs[1]:
        st.subheader("Split PDF into Pages")
        split_file = st.file_uploader("Upload PDF to split", type="pdf", key="split")
        if split_file:
            st.info("Select pages to extract in the Pro version.")
            st.button("Extract Pages (Pro)", disabled=True)

    # --- Tab 3: Watermark ---
    with tabs[2]:
        st.subheader("Protect Your Work")
        st.write("Add your name or school logo to the footer of every page.")
        watermark_text = st.text_input("Enter Watermark Text (e.g., 'Property of Ms. Smith')")
        if st.button("Apply Watermark (Pro)"):
            st.warning("Watermarking is a Pro-only feature to prevent unauthorized distribution.")

    st.markdown("---")
    st.info("💡 **Pro Tip:** Use the Merger to combine ⚡ Speed Math and 🧩 Fraction Factory results into one complete lesson pack!")
