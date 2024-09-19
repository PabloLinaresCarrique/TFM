# main.py
import streamlit as st
from admin_settings import run_admin_settings
from data_normalization import run_inventory_management

# Admin dashboard function
def run_admin_dashboard():
    if st.session_state.get('is_admin', False):
        st.title('Admin Dashboard')

        # Create tabs
        tab1, tab2 = st.tabs(["Inventory Management", "Admin Settings"])

        # Inventory Management Tab
        with tab1:
            run_inventory_management()

        # Admin Settings Tab
        with tab2:
            run_admin_settings()
    else:
        st.error("Access Denied: You do not have permission to access this page.")

# Run the admin dashboard
if __name__ == "__main__":
    run_admin_dashboard()
