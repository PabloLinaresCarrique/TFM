import streamlit as st
from hashlib import sha256
from utils import get_db_connection

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def save_user(username, password, team):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, team) VALUES (%s, %s, %s)', (username, password, team))  # Add team to the query
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))  # Using 'username'
    user = cursor.fetchone()
    conn.close()
    return user

def login_or_register():
    st.image('images/cortexlogo.jpg')

    tab1, tab2 = st.tabs(["Log-in to existing account", "Register new user"])

    with tab1:
        st.subheader("Login with your username")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type='password', key="login_password")

        if st.button("Login"):
            hashed_password = hash_password(password)
            if verify_user(username, hashed_password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.warning("Incorrect Username/Password")

    with tab2:
        st.subheader("Create a unique username")
        username = st.text_input("Username", key="create_username")
        password = st.text_input("Password", type='password', key="create_password")
        confirm_password = st.text_input("Confirm Password", type='password', key="create_confirm_password")
        team = st.selectbox("Select your Team", 
                        options=["Team Spain", "Team US", "Team UK", "Team Portugal", "Team Iberia"], 
                        key="team_selection")

        if st.button("Create account"):
            if password == confirm_password:
                hashed_password = hash_password(password)
                save_user(username, hashed_password, team)  # Pass team to save_user function
                st.success("Account created! Please log in.")
            else:
                st.warning("Passwords do not match")
