# admin_settings.py
import streamlit as st
from utils import get_db_connection

# Function to fetch all users (no longer needed for display but retained for any future use)
def fetch_users():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username, admin FROM users")
            users = cursor.fetchall()
            return pd.DataFrame(users, columns=[desc[0] for desc in cursor.description])
    finally:
        connection.close()

# Function to update admin privileges for a user
def update_admin_privileges(username, is_admin):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET admin = %s WHERE username = %s", (is_admin, username))
            connection.commit()
    finally:
        connection.close()

# Function to run the admin settings tab
def run_admin_settings():
    st.header("Admin Settings")

    # Input for user ID to manage admin privileges
    user_id = st.text_input('Enter User ID to Manage Admin Privileges')

    # Dropdown to select new admin status
    new_admin_status = st.selectbox('Select Admin Status', ['Grant Admin', 'Revoke Admin'])

    # Button to update admin privileges
    if st.button('Update Admin Privileges'):
        if user_id.strip() == "":
            st.error("Please enter a valid User ID.")
        else:
            is_admin = True if new_admin_status == 'Grant Admin' else False
            update_admin_privileges(user_id, is_admin)
            st.success(f"Admin privileges updated for user: {user_id}")
            st.experimental_rerun()  # Refresh the dashboard to reflect changes
