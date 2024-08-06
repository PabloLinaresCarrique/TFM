import streamlit as st
import pymysql
import pandas as pd

# Function to connect to the database
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Banana22!',
        database='aml_system'
    )

# Fetch transactions to be reviewed
def fetch_alerts():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions WHERE review_status = 'to_be_reviewed'")
            transactions = cursor.fetchall()
            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(transactions, columns=[desc[0] for desc in cursor.description])
            return df
    finally:
        connection.close()

# Streamlit App Layout
st.title('AML Alert Dashboard')

# Fetch and display alerts
alerts_df = fetch_alerts()
st.write(alerts_df)

# Allow users to update alert status
if st.button('Resolve Selected Alerts'):
    selected_alerts = st.multiselect('Select Alerts to Resolve', alerts_df['id'])
    if selected_alerts:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                for alert_id in selected_alerts:
                    cursor.execute("UPDATE transactions SET review_status = 'reviewed' WHERE id = %s", (alert_id,))
                connection.commit()
            st.success('Selected alerts resolved.')
        finally:
            connection.close()

