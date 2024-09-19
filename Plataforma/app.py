import streamlit as st
from login import login_or_register
from dashboard import run_aml_dashboard
from chatbot import run_chatbot
from alert_details import show_alert_details
from utils import get_image_from_s3
from admin_dashboard import run_admin_dashboard  # Import the admin dashboard function

st.set_page_config(layout="wide")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if 'first_name' not in st.session_state:
        st.session_state.first_name = ""

    if 'last_name' not in st.session_state:
        st.session_state.last_name = ""

    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False  # Initialize admin status in session state

    if not st.session_state.logged_in:
        login_or_register()
    else:
        # Create three sections in the sidebar
        sidebar_top = st.sidebar.container()
        sidebar_middle = st.sidebar.container()
        sidebar_bottom = st.sidebar.container()

        with sidebar_top:
            # Retrieve the logo image from S3
            logo_image = get_image_from_s3('cortexneural-platform-images', 'cortexlogo_sidebar.png')  # Replace with your bucket name and image key
            if logo_image:
                st.image(logo_image, use_column_width=True, width=250)
            
            # Display personalized welcome message with first name and last name
            st.title(f"Welcome, {st.session_state.first_name} {st.session_state.last_name}")

        with sidebar_middle:
            # Initialize the current page in session state if it doesn't exist
            if 'current_page' not in st.session_state:
                st.session_state.current_page = "Dashboard"

            # Create buttons for navigation
            if st.button("Dashboard"):
                st.session_state.current_page = "Dashboard"
            if st.button("Alert Details"):
                st.session_state.current_page = "Alert Details"
            if st.button("Virtual Assistant"):
                st.session_state.current_page = "Chatbot"

            # Admin dashboard button (only for admins)
            if st.session_state.is_admin and st.button("Admin Dashboard"):
                st.session_state.current_page = "Admin Dashboard"

        with sidebar_bottom:
            # Add some vertical space to push the logout button to the bottom
            st.markdown('<div style="flex: 1;"></div>', unsafe_allow_html=True)
            
            # Logout button
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.first_name = ""
                st.session_state.last_name = ""
                st.session_state.is_admin = False  # Reset admin status on logout
                st.rerun()

        # Main content area
        if st.session_state.current_page == "Dashboard":
            run_aml_dashboard()
        elif st.session_state.current_page == "Alert Details":
            if 'selected_alert_id' in st.session_state:
                show_alert_details(st.session_state.selected_alert_id)
            else:
                st.write("No alert selected. Please select an alert from the Dashboard.")
        elif st.session_state.current_page == "Chatbot":
            run_chatbot()
        elif st.session_state.current_page == "Admin Dashboard":
            run_admin_dashboard()  # Load the admin dashboard page

if __name__ == '__main__':
    main()
