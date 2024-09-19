import streamlit as st
import pandas as pd
from utils import get_db_connection

# Function to fetch alerts based on review status and assigned team
def fetch_alerts(team_name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Query to fetch all necessary fields including laundering flags and priority
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
            df = pd.DataFrame(transactions, columns=[desc[0] for desc in cursor.description])
            return df
    finally:
        connection.close()

# Function to add priority emojis
def format_priority(priority):
    if priority == 'High Priority':
        return '🔴'
    elif priority == 'Medium Priority':
        return '🟠'
    else:
        return '🟢'

# Function to run the AML Case Dashboard
def run_aml_dashboard():
    st.title('AML Case Dashboard')

    # Display user team from session state
    st.write(f"User Team: {st.session_state.get('user_team')}")

    user_team = st.session_state.get('user_team', None)

    if user_team:
        alerts_df = fetch_alerts(user_team)
        st.write("### Cases to be Reviewed")

        if not alerts_df.empty:
            # Rename columns for display purposes
            renamed_columns = {
                'id': 'Case ID',
                'from_bank': 'From Bank',
                'from_account': 'From Account',
                'to_bank': 'To Bank',
                'to_account': 'To Account',
                'amount_received': 'Amount Received',
                'receiving_currency': 'Receiving Currency',
                'amount_paid': 'Amount Paid',
                'payment_currency': 'Payment Currency',
                'payment_format': 'Payment Format',
                'predicted_is_laundering': 'Predicted Laundering',
                'sql_is_laundering': 'SQL Laundering',
                'priority': 'Priority',
                'review_status': 'Review Status',
                'assigned_team': 'Assigned Team'
            }

            # Apply renaming and add priority emojis
            alerts_df = alerts_df.rename(columns=renamed_columns)
            alerts_df['Priority'] = alerts_df['Priority'].apply(format_priority)

            # Reorder columns with 'Priority' at the front
            column_order = ['Priority', 'Case ID', 'From Bank', 'From Account', 'To Bank', 'To Account',
                            'Amount Received', 'Receiving Currency', 'Amount Paid', 'Payment Currency', 
                            'Payment Format', 'Predicted Laundering', 'SQL Laundering', 'Review Status', 
                            'Assigned Team']
            display_df = alerts_df[column_order]

            # Display the relevant data in a streamlined layout
            st.dataframe(display_df)
            
            # Capture the previously selected alert ID to detect changes
            previous_selected_alert_id = st.session_state.get('selected_alert_id', None)

            # Dropdown to select an alert
            selected_alert_id = st.selectbox('Select Case to View Details', display_df['Case ID'].tolist())
            
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

if __name__ == "__main__":
    run_aml_dashboard()
