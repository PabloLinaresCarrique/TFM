import streamlit as st
import base64
from utils import get_s3_client  # Import S3 client setup

def load_pdf_from_s3(bucket_name, pdf_key):
    """Load a PDF file from S3 and return its base64 encoded string."""
    s3_client = get_s3_client()
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=pdf_key)
        pdf_data = response['Body'].read()
        return base64.b64encode(pdf_data).decode('utf-8')
    except Exception as e:
        st.error(f"Error retrieving PDF from S3: {e}")
        return None

def run_pdf_viewer_module(bucket_name, pdf_key):
    # Initialize session state to track whether the PDF viewer is open
    if 'viewer_open' not in st.session_state:
        st.session_state.viewer_open = False

    # Display the PDF icon (as a clickable button)
    if st.button('📄 Toggle Document Viewer'):
        # Toggle the state
        st.session_state.viewer_open = not st.session_state.viewer_open

    # Conditionally render the PDF viewer based on the toggle state
    if st.session_state.viewer_open:
        # Load the PDF from S3
        pdf_base64 = load_pdf_from_s3(bucket_name, pdf_key)
        if pdf_base64:
            pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="100%" height="600" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.error("Failed to load the PDF from S3.")
