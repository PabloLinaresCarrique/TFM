import streamlit as st
from hashlib import sha256
import os
from utils import get_db_connection, get_image_from_s3  # Import from utils

# Retrieve database credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "us-cluster-east-01.k8s.cleardb.net")
DB_USER = os.getenv("DB_USER", "b65d4df2f590b8")
DB_PASSWORD = os.getenv("DB_PASSWORD", "c275d9fd")
DB_NAME = os.getenv("DB_NAME", "heroku_86ba7e4ebd286bc")  # Correct database name from CLEARDB_DATABASE_URL

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def save_user(username, password, team, first_name, last_name):
    """
    Save a new user to the database.
    """
    conn = get_db_connection()
    if conn is None:
        return  # Return if the connection failed
    
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, team, first_name, last_name, admin) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (username, password, team, first_name, last_name, False))  # By default, new users are not admins
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Error saving user: {err}")
    finally:
        conn.close()

def verify_user(username, password):
    """
    Verify user credentials against the database.
    """
    conn = get_db_connection()
    if conn is None:
        return None  # Return if the connection failed
    
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        st.error(f"Error verifying user: {err}")
        return None
    finally:
        conn.close()

def login_or_register():
    # Retrieve the image from S3 instead of MongoDB
    logo_image_data = get_image_from_s3('cortexneural-platform-images', 'cortexlogo.jpg')  # Replace 'cortexlogo.png' with your actual image key
    if logo_image_data:
        st.image(logo_image_data, use_column_width=True)

    # Initialize session state if not already done
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'first_name' not in st.session_state:
        st.session_state.first_name = ""
    if 'last_name' not in st.session_state:
        st.session_state.last_name = ""
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    if 'user_team' not in st.session_state:  # Initialize user_team in session state
        st.session_state.user_team = ""

    # Create two tabs for login and registration
    tab1, tab2 = st.tabs(["Log-in to existing account", "Register new user"])

    with tab1:
        st.subheader("Login with your username")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type='password', key="login_password")

        if st.button("Login"):
            hashed_password = hash_password(password)
            user = verify_user(username, hashed_password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user[0]  # Assuming username is the first column
                st.session_state.first_name = user[3]  # Assuming first name is the fourth column
                st.session_state.last_name = user[4]  # Assuming last name is the fifth column
                st.session_state.is_admin = user[5]  # Assuming admin status is the sixth column
                st.session_state.user_team = user[2]  # Assuming team is the third column
                st.success(f"Logged in as {user[0]} from team {user[2]}")
                st.rerun()
            else:
                st.warning("Incorrect Username/Password")

    with tab2:
        st.subheader("Create a unique username")
        first_name = st.text_input("First Name", key="first_name")
        last_name = st.text_input("Last Name", key="last_name")
        username = st.text_input("Username", key="create_username")
        password = st.text_input("Password", type='password', key="create_password")
        confirm_password = st.text_input("Confirm Password", type='password', key="create_confirm_password")
        team = st.selectbox("Select your Team", 
                            options=["Team Spain", "Team US", "Team UK", "Team Portugal", "Team Iberia"], 
                            key="team_selection")

        if st.button("Create account"):
            if password == confirm_password:
                hashed_password = hash_password(password)
                save_user(username, hashed_password, team, first_name, last_name)
                st.success("Account created! Please log in.")
            else:
                st.warning("Passwords do not match")

if __name__ == "__main__":
    login_or_register()
