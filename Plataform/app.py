import streamlit as st
from login import login_or_register
from dashboard import run_aml_dashboard
from chatbot import run_chatbot
from alert_details import show_alert_details  # Import the new function

st.set_page_config(layout="wide")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_or_register()
    else:
        st.sidebar.image("/Users/tiagomiguelrebelomirotes/Desktop/aml_structured/images/cortexlogo_sidebar.png", use_column_width=True, width = 250)
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Dashboard", "Alert Details", "Chatbot"])

        if page == "Dashboard":
            run_aml_dashboard()
        elif page == "Alert Details":
            if 'selected_alert_id' in st.session_state:
                show_alert_details(st.session_state.selected_alert_id)
            else:
                st.write("No alert selected. Please select an alert from the Dashboard.")
        elif page == "Chatbot":
            run_chatbot()

        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

if __name__ == '__main__':
    main()