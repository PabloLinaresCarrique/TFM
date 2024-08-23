import streamlit as st
import pandas as pd
from utils import get_db_connection

def fetch_alerts():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions WHERE review_status = 'to_be_reviewed'")
            transactions = cursor.fetchall()
            df = pd.DataFrame(transactions, columns=[desc[0] for desc in cursor.description])
            return df
    finally:
        connection.close()

def run_aml_dashboard():
    st.title('AML Case Dashboard')

    alerts_df = fetch_alerts()
    st.write("### Cases to be Reviewed")

    if not alerts_df.empty:
        st.dataframe(alerts_df)
        selected_alert_id = st.selectbox('Select Case to View Details', alerts_df['id'].tolist())
        if selected_alert_id:
            st.session_state['selected_alert_id'] = selected_alert_id
            st.write(f"View details for Case {selected_alert_id} in the Alert Details page.")
    else:
        st.write("No cases to review at the moment.")