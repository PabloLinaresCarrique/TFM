import streamlit as st
import base64
from utils import get_s3_client  

def load_pdf_from_s3(bucket_name, pdf_key):
    """
    Load a PDF file from an S3 bucket and return its base64 encoded string.
    This will be used to embed the PDF in a Streamlit app.
    
    Args:
        bucket_name (str): Name of the S3 bucket.
        pdf_key (str): Key (path) to the PDF file in the S3 bucket.

    Returns:
        str: Base64 encoded string of the PDF file if successful, else None.
    """
    s3_client = get_s3_client()  # Get the S3 client
    try:
        # Fetch the PDF object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=pdf_key)
        pdf_data = response['Body'].read()  # Read the PDF file content
        return base64.b64encode(pdf_data).decode('utf-8')  # Encode to base64 and return
    except Exception as e:
        st.error(f"Error retrieving PDF from S3: {e}")  # Display error if fetching fails
        return None  # Return None if an error occurred

def run_pdf_viewer_module(bucket_name, pdf_key):
    """
    Display a PDF viewer module in the Streamlit app. Allows toggling the PDF viewer on and off.
    
    Args:
        bucket_name (str): Name of the S3 bucket.
        pdf_key (str): Key (path) to the PDF file in the S3 bucket.
    """
    # Initialize session state to track whether the PDF viewer is open
    if 'viewer_open' not in st.session_state:
        st.session_state.viewer_open = False  # Set default state as closed

    # Display a button to toggle the PDF viewer
    if st.button('📄 Toggle Document Viewer'):
        st.session_state.viewer_open = not st.session_state.viewer_open  # Toggle the viewer state

    # Conditionally render the PDF viewer based on the toggle state
    if st.session_state.viewer_open:
        # Load the PDF from S3
        pdf_base64 = load_pdf_from_s3(bucket_name, pdf_key)
        if pdf_base64:
            # Display the PDF using an iframe (HTML embedded object)
            pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="100%" height="600" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)  # Render the PDF in the Streamlit app
        else:
            st.error("Failed to load the PDF from S3.")  # Display an error if the PDF could not be loaded
