import streamlit as st
from hashlib import sha256  # Library for hashing passwords securely
import os
from utils import get_db_connection, get_image_from_s3  # Utility functions to handle DB connection and S3 image retrieval

# Retrieve database credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "us-cluster-east-01.k8s.cleardb.net")  # Default host value for DB connection
DB_USER = os.getenv("DB_USER", "b65d4df2f590b8")  # Default DB username
DB_PASSWORD = os.getenv("DB_PASSWORD", "c275d9fd")  # Default DB password
DB_NAME = os.getenv("DB_NAME", "heroku_86ba7e4ebd286bc")  # Default DB name

# Function to hash passwords using SHA-256
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Function to save a new user to the database
def save_user(username, password, team, first_name, last_name):
    """
    Save a new user to the database.
    """
    conn = get_db_connection()  # Establish database connection
    if conn is None:
        return  # Return if the connection failed
    
    try:
        cursor = conn.cursor()
        # Insert new user data into the 'users' table
        cursor.execute('INSERT INTO users (username, password, team, first_name, last_name, admin) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (username, password, team, first_name, last_name, False))  # By default, new users are not admins
        conn.commit()  # Commit changes to the database
    except mysql.connector.Error as err:
        st.error(f"Error saving user: {err}")  # Display error if the user could not be saved
    finally:
        conn.close()  # Ensure the database connection is closed

# Function to verify user credentials during login
def verify_user(username, password):
    """
    Verify user credentials against the database.
    """
    conn = get_db_connection()  # Establish database connection
    if conn is None:
        return None  # Return None if the connection failed
    
    try:
        cursor = conn.cursor()
        # Query to check if the username and password match a user in the 'users' table
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()  # Fetch user data if credentials are valid
        return user
    except mysql.connector.Error as err:
        st.error(f"Error verifying user: {err}")  # Display error if there was an issue verifying the user
        return None
    finally:
        conn.close()  # Ensure the database connection is closed

# Main function to handle user login or registration
def login_or_register():
    # Retrieve the logo image from S3 and display it
    logo_image_data = get_image_from_s3('cortexneural-platform-images', 'cortexlogo.jpg')  # Replace 'cortexlogo.jpg' with your actual image key
    if logo_image_data:
        st.image(logo_image_data, use_column_width=True)  # Display the logo image

    # Initialize session state variables if not already done
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False  # Tracks whether the user is logged in
    if 'username' not in st.session_state:
        st.session_state.username = ""  # Stores the logged-in username
    if 'first_name' not in st.session_state:
        st.session_state.first_name = ""  # Stores the user's first name
    if 'last_name' not in st.session_state:
        st.session_state.last_name = ""  # Stores the user's last name
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False  # Tracks whether the user is an admin
    if 'user_team' not in st.session_state:  
        st.session_state.user_team = ""  # Stores the user's team

    # Create two tabs for logging in and registering
    tab1, tab2 = st.tabs(["Log-in to existing account", "Register new user"])

    # Login tab
    with tab1:
        st.subheader("Login with your username")
        username = st.text_input("Username", key="login_username")  # Input for the username
        password = st.text_input("Password", type='password', key="login_password")  # Input for the password (hidden)

        if st.button("Login"):
            hashed_password = hash_password(password)  # Hash the entered password
            user = verify_user(username, hashed_password)  # Verify the user credentials
            if user:
                # If valid user, set session state variables
                st.session_state.logged_in = True
                st.session_state.username = user[0]  # Retrieve username
                st.session_state.first_name = user[3]  # Retrieve first name
                st.session_state.last_name = user[4]  # Retrieve last name
                st.session_state.is_admin = user[5]  # Check if the user is an admin
                st.session_state.user_team = user[2]  # Retrieve user's team
                st.success(f"Logged in as {user[0]} from team {user[2]}")  # Show success message
                st.rerun()  # Rerun the app to reflect the login state
            else:
                st.warning("Incorrect Username/Password")  # Show warning if login fails

    # Registration tab
    with tab2:
        st.subheader("Create a unique username")
        first_name = st.text_input("First Name", key="first_name")  # Input for first name
        last_name = st.text_input("Last Name", key="last_name")  # Input for last name
        username = st.text_input("Username", key="create_username")  # Input for new username
        password = st.text_input("Password", type='password', key="create_password")  # Input for new password
        confirm_password = st.text_input("Confirm Password", type='password', key="create_confirm_password")  # Input to confirm password
        team = st.selectbox("Select your Team", 
                            options=["Team Spain", "Team US", "Team UK", "Team Portugal", "Team Iberia"], 
                            key="team_selection")  # Dropdown to select user's team

        # Button to create a new account
        if st.button("Create account"):
            if password == confirm_password:
                hashed_password = hash_password(password)  # Hash the password
                save_user(username, hashed_password, team, first_name, last_name)  # Save the new user in the database
                st.success("Account created! Please log in.")  # Show success message
            else:
                st.warning("Passwords do not match")  # Show warning if passwords don't match

# Entry point to run the app
if __name__ == "__main__":
    login_or_register()  # Call the main function
