import streamlit as st
import pandas as pd
import json
from utils import get_db_connection

# Function to generate a unique identifier for each transaction
def generate_transaction_id(row):
    transaction_id = f"{row['from_account']}_{row['to_account']}_{row['amount_paid']}"
    return transaction_id

# Function to process and normalize data
def process_data(json_data):
    # Directly load the JSON data into a DataFrame
    df = pd.DataFrame(json_data)

    # Add additional required columns
    df['review_status'] = 'Pending'
    df['closure_type'] = 'Unresolved'
    df['assigned_team'] = 'Unassigned'
    df['rule_flagged'] = 'ML Detection'

    # Generate unique transaction ID
    df['transaction_id'] = df.apply(generate_transaction_id, axis=1)

    return df

# Function to load JSON data into the transactions table
def load_json_to_db(json_data):
    processed_df = process_data(json_data)
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM transactions;")
            connection.commit()
            st.write("All existing transactions deleted.")

            # Prepare batch insert data
            insert_data = []
            for _, row in processed_df.iterrows():
                insert_data.append((
                    row["transaction_id"],
                    row["from_bank"],
                    str(row["from_account"]),
                    row["to_bank"],
                    str(row["to_account"]),
                    float(row["amount_received"]) if pd.notna(row["amount_received"]) else 0.0,
                    row["receiving_currency"],
                    float(row["amount_paid"]) if pd.notna(row["amount_paid"]) else 0.0,
                    row["payment_currency"],
                    row["payment_format"],
                    int(row["predicted_is_laundering"]) if pd.notna(row["predicted_is_laundering"]) else 0,
                    int(row["sql_is_laundering"]) if pd.notna(row["sql_is_laundering"]) else 0,
                    row["priority"],  # Ensure priority is included
                    row["review_status"],
                    row["closure_type"],
                    row["assigned_team"],
                    row["rule_flagged"]
                ))

            # Updated insert statement
            cursor.executemany(
                """
                INSERT INTO transactions (transaction_id, from_bank, from_account, to_bank, to_account, 
                                          amount_received, receiving_currency, amount_paid, 
                                          payment_currency, payment_format, predicted_is_laundering, sql_is_laundering,
                                          priority, review_status, closure_type, assigned_team, rule_flagged)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                insert_data
            )
            connection.commit()
            st.success("JSON data loaded into the database successfully, replacing old cases.")
    except Exception as e:
        st.error(f"Error loading JSON to DB: {e}")
    finally:
        connection.close()


# Function to fetch all alerts (including reviewed ones) for admin view
def fetch_all_alerts():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions")
            transactions = cursor.fetchall()
            df = pd.DataFrame(transactions, columns=[desc[0] for desc in cursor.description])
            return df
    finally:
        connection.close()

# Function to fetch all predefined team names
def fetch_teams():
    return ["Team Spain", "Team US", "Team UK", "Team Portugal", "Team Iberia"]

# Function to assign or reassign a case to a team
# Function to assign or reassign a case to a team
def assign_case_to_team(case_id, team_name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE transactions SET assigned_team = %s, review_status = 'Assigned to Analyst' WHERE transaction_id = %s",
                (team_name, case_id)
            )
            connection.commit()
    finally:
        connection.close()
# Function to assign or reassign a case to a team
def assign_case_to_team(case_id, team_name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE transactions SET assigned_team = %s, review_status = 'Assigned to Analyst' WHERE transaction_id = %s",
                (team_name, case_id)
            )
            connection.commit()
    finally:
        connection.close()

# Function to assign cases based on priority, team, and the number of cases to assign
def assign_cases_based_on_priority(priority, team_name, num_cases, df):
    """
    Assigns a specified number of cases to a team based on their priority level.
    :param priority: The priority level to filter by (e.g., 'High Priority', 'Medium Priority').
    :param team_name: The team to assign cases to.
    :param num_cases: Number of cases to assign.
    :param df: The dataframe containing the transactions.
    """
    # Filter cases based on the selected priority
    cases_to_assign = df[df['priority'] == priority]
    
    # If num_cases is greater than available cases, adjust it
    if num_cases > len(cases_to_assign):
        num_cases = len(cases_to_assign)
        st.warning(f"Only {num_cases} cases available with priority: {priority}. Assigning all available cases.")
    
    # Assign only the number of cases specified
    cases_to_assign = cases_to_assign.head(num_cases)
    
    for index, row in cases_to_assign.iterrows():
        assign_case_to_team(row['transaction_id'], team_name)
    
    st.success(f"Assigned {num_cases} cases to {team_name} based on priority: {priority}")

# Function to run the inventory management tab (modified for priority-based and number-based assignment)
def run_inventory_management():
    st.header("Inventory Management")

    # Load JSON data into the database
    uploaded_file = st.file_uploader("Upload JSON File", type=["json"])
    if uploaded_file is not None:
        if st.button("Load Document"):
            json_data = json.load(uploaded_file)
            load_json_to_db(json_data)
            st.success("JSON data loaded into the database successfully.")

    # Fetch and display all cases
    alerts_df = fetch_all_alerts()
    st.write("### All Cases")

    if not alerts_df.empty:
        # Display the dataframe in a simple table format
        st.dataframe(alerts_df)

        # Dynamically get unique priority types from the 'priority' column
        unique_priorities = alerts_df['priority'].dropna().unique().tolist()

        # Select a priority and team for assignment
        if unique_priorities:  # Check if there are any priorities available
            priority = st.selectbox('Select Priority for Assignment', unique_priorities)
            team = st.selectbox('Select Team to Assign', fetch_teams())

            # Input for the number of cases to assign
            num_cases = st.number_input('Number of Cases to Assign', min_value=1, max_value=len(alerts_df), value=1)

            # Button to assign cases based on priority and number
            if st.button('Assign Cases by Priority'):
                # Assign cases based on the chosen priority, team, and number of cases
                assign_cases_based_on_priority(priority, team, num_cases, alerts_df)
                st.rerun()  # Refresh the dashboard to reflect changes
        else:
            st.warning("No available priorities found in the data for assignment.")
