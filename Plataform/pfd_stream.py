import streamlit as st
import fitz  # PyMuPDF
import pdfplumber

# Title of the Streamlit app
st.title("PDF Viewer and Search")

# File uploader for PDF
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Load the PDF
    with pdfplumber.open(uploaded_file) as pdf:
        # Display the PDF with page numbers
        page_number = st.number_input("Page number", 1, len(pdf.pages), 1)
        page = pdf.pages[page_number - 1]
        text = page.extract_text()

        # Display the text content of the page
        if text:
            st.text_area("Page content", text, height=300)
        else:
            st.warning("No text found on this page")

    # Search functionality
    search_term = st.text_input("Enter a term to search in the PDF")

    if search_term:
        search_results = []
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if search_term.lower() in page_text.lower():
                search_results.append((i + 1, page_text))

        if search_results:
            st.write(f"Found {len(search_results)} result(s) for '{search_term}':")
            for page_num, result_text in search_results:
                st.write(f"**Page {page_num}**")
                st.text_area(f"Result from page {page_num}", result_text, height=200)
        else:
            st.warning(f"No results found for '{search_term}'")
