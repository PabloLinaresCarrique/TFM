import streamlit as st
import pandas as pd
from utils import get_db_connection

# Function to fetch alerts based on review status and assigned team
def fetch_alerts(team_name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Updated query to fetch all necessary fields including laundering flags and priority
            cursor.execute(
                """
                SELECT id, from_bank, from_account, to_bank, to_account, amount_received, receiving_currency, 
                       amount_paid, payment_currency, payment_format, predicted_is_laundering, 
                       sql_is_laundering, priority, review_status, assigned_team
                FROM transactions 
                WHERE review_status = 'Assigned to Analyst' AND assigned_team = %s
                """, 
                (team_name,)
            )
            transactions = cursor.fetchall()
            # Ensure that the new columns are reflected in the DataFrame
            df = pd.DataFrame(transactions, columns=[desc[0] for desc in cursor.description])
            return df
    finally:
        connection.close()

# Function to run the AML Case Dashboard
def run_aml_dashboard():
    st.title('AML Case Dashboard')

    # Debugging: Display user team from session state
    st.write(f"User Team: {st.session_state.get('user_team')}")

    # Assuming the user's team is stored in session state
    user_team = st.session_state.get('user_team', None)  # Replace with actual logic to fetch user's team

    if user_team:
        alerts_df = fetch_alerts(user_team)
        st.write("### Cases to be Reviewed")

        if not alerts_df.empty:
            # Select only relevant columns for display, including new columns like priority and laundering flags
            relevant_columns = ['id', 'from_bank', 'from_account', 'to_bank', 'to_account', 
                                'amount_received', 'receiving_currency', 'amount_paid', 'payment_currency', 
                                'payment_format', 'predicted_is_laundering', 'sql_is_laundering', 
                                'priority', 'review_status', 'assigned_team']
            display_df = alerts_df[relevant_columns]

            # Display the relevant data in a streamlined layout
            st.dataframe(display_df)
            
            # Capture the previously selected alert ID to detect change
            previous_selected_alert_id = st.session_state.get('selected_alert_id', None)

            # Dropdown to select an alert
            selected_alert_id = st.selectbox('Select Case to View Details', display_df['id'].tolist())
            
            if selected_alert_id:
                # Detect if a new case is selected
                if 'selected_alert_id' not in st.session_state or st.session_state['selected_alert_id'] != selected_alert_id:
                    # Set new selected alert ID
                    st.session_state['selected_alert_id'] = selected_alert_id
                    
                    # Reset narrative content for the new case
                    st.session_state.pop('narrative_content', None)  # Remove previous narrative content from session state

                # Display case details or direct user to the details page
                st.write(f"View details for Case {selected_alert_id} in the Alert Details page.")
    else:
        st.write("No cases to review at the moment.")

# Ensure this function is called correctly when the user logs in
if __name__ == "__main__":
    run_aml_dashboard()
