import streamlit as st
from utils import get_db_connection

def fetch_alert_details(alert_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions WHERE id = %s", (alert_id,))
            alert_details = cursor.fetchone()
            return alert_details
    finally:
        connection.close()

def show_alert_details(alert_id):
    alert_details = fetch_alert_details(alert_id)
    st.title(f"Case {alert_id}")

    tab1, tab2, tab3 = st.tabs(["Alert Overview", "Documents", "Narrative"])

    with tab1:
        st.write("## Alert Overview")
        st.write(f"**Timestamp:** {alert_details[1]}")
        st.write(f"**From Bank:** {alert_details[2]}")
        st.write(f"**From Account:** {alert_details[3]}")
        st.write(f"**To Bank:** {alert_details[4]}")
        st.write(f"**To Account:** {alert_details[5]}")
        st.write(f"**Amount Received:** {alert_details[6]} {alert_details[7]}")
        st.write(f"**Amount Paid:** {alert_details[8]} {alert_details[9]}")
        st.write(f"**Payment Format:** {alert_details[10]}")
        st.write(f"**Is Laundering:** {'Yes' if alert_details[11] else 'No'}")

    with tab2:
        st.write("## Documents")
        st.write("No documents available for this case.")

    with tab3:
        st.write("## Narrative")
        st.write("No narrative provided for this case.")

    if st.button('Resolve Selected Case'):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE transactions SET review_status = 'reviewed' WHERE id = %s", (alert_id,))
                connection.commit()
            st.success('Selected case resolved.')
            del st.session_state['selected_alert_id']
            st.experimental_rerun()
        finally:
            connection.close()