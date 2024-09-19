import streamlit as st
from utils import get_db_connection
from enhanced_entity_graph import show_entity_graph
from narrative_component import show_narrative_tab
from osint_search import perform_osint_search
from mongodb_case_management import (
    create_case,
    get_case,
    update_narrative,
    add_document_to_case,
    close_case,
    update_entity_to_case,
    add_entity_to_case
)
import base64

def show_entities_section(client_details):
    st.write("## Entities")

    if "entity_tabs" not in st.session_state:
        st.session_state.entity_tabs = ["Main Client"]
        st.session_state.additional_info_fields = {"Main Client": []}

    if st.button("+ Add Entity Tab", key="add_entity_tab_button"):
        new_tab_name = f"Entity {len(st.session_state.entity_tabs) + 1}"
        st.session_state.entity_tabs.append(new_tab_name)
        st.session_state.additional_info_fields[new_tab_name] = []
        st.experimental_rerun()

    entity_tabs = st.tabs(st.session_state.entity_tabs)

    for i, tab_name in enumerate(st.session_state.entity_tabs):
        with entity_tabs[i]:
            if st.button("OSINT Search", key=f"osint_button_{tab_name}_{i}"):
                name = st.session_state.get(f"client_name_{tab_name}_{i}", "")
                job = st.session_state.get(f"client_job_{tab_name}_{i}", "")
                country = st.session_state.get(f"client_country_{tab_name}_{i}", "")
                perform_osint_search(name, job, country)

            st.write("#### Internal Records")

            if tab_name == "Main Client" and client_details:
                name = st.text_input("Name", client_details[5], key=f"client_name_{tab_name}_{i}")
                age = st.text_input("Age", str(client_details[1]), key=f"client_age_{tab_name}_{i}")
                job = st.text_input("Job", client_details[2], key=f"client_job_{tab_name}_{i}")
                marital_status = st.text_input("Marital Status", client_details[3], key=f"client_marital_status_{tab_name}_{i}")
                education = st.text_input("Education", client_details[4], key=f"client_education_{tab_name}_{i}")
                from_account = st.text_input("From Account", client_details[6], key=f"client_from_account_{tab_name}_{i}")
            else:
                name = st.text_input("Name", "", key=f"client_name_{tab_name}_{i}")
                age = st.text_input("Age", "", key=f"client_age_{tab_name}_{i}")
                job = st.text_input("Job", "", key=f"client_job_{tab_name}_{i}")
                marital_status = st.text_input("Marital Status", "", key=f"client_marital_status_{tab_name}_{i}")
                education = st.text_input("Education", "", key=f"client_education_{tab_name}_{i}")
                from_account = st.text_input("From Account", "", key=f"client_from_account_{tab_name}_{i}")

            for j, _ in enumerate(st.session_state.additional_info_fields[tab_name]):
                st.text_input(f"Additional Info Title {j+1}", key=f"additional_info_title_{tab_name}_{i}_{j}")
                st.text_area(f"Additional Info Content {j+1}", key=f"additional_info_content_{tab_name}_{i}_{j}")

            if st.button("Add Additional Info", key=f"add_additional_info_{tab_name}_{i}"):
                st.session_state.additional_info_fields[tab_name].append({})
                st.experimental_rerun()

            if st.button("Save Changes", key=f"save_changes_{tab_name}_{i}"):
                entity_data = {
                    "name": name,
                    "age": age,
                    "job": job,
                    "marital_status": marital_status,
                    "education": education,
                    "from_account": from_account,
                    "additional_info": []
                }
                
                for j, _ in enumerate(st.session_state.additional_info_fields[tab_name]):
                    title_key = f"additional_info_title_{tab_name}_{i}_{j}"
                    content_key = f"additional_info_content_{tab_name}_{i}_{j}"
                    title = st.session_state.get(title_key, "")
                    content = st.session_state.get(content_key, "")
                    if title and content:
                        entity_data["additional_info"].append({title: content})
                
                if 'case_id' in st.session_state and st.session_state.case_id:
                    if update_entity_to_case(st.session_state.case_id, tab_name, entity_data):
                        st.success("Changes saved successfully!")
                    else:
                        st.error("Failed to save changes.")
                else:
                    st.warning("No active case. Please start a case review first.")

def show_alert_details(alert_id):
    alert_details = fetch_alert_details(alert_id)

    if not alert_details:
        st.error("No details found for the selected alert. Please check the alert ID and try again.")
        return

    from_account = alert_details[2]
    client_details = fetch_client_details(from_account)

    st.subheader(f"Case Identifier: {alert_id}")

    tab1, tab2, tab3 = st.tabs(["Alert Overview", "Entities", "Narrative"])

    with tab1:
        st.write("## Alert Overview")

        if 'case_id' not in st.session_state:
            st.session_state.case_id = None

        if st.session_state.case_id is None and st.button("Start Case Review", key="start_case_review"):
            case_id = create_case(alert_id, alert_details, client_details)
            if case_id:
                st.session_state.case_id = case_id
                st.success(f"Case review started. Case ID: {case_id}")

        current_case = get_case(st.session_state.case_id) if st.session_state.case_id else None

        if current_case and current_case.get('status') != 'closed':
            closure_options = [
                "Select closure type",
                "False-Positive - Not suspicious activity",
                "Suspicious Activity Reported",
                "Legitimate Transaction - No further action",
                "Insufficient Information - More data needed",
                "Referred to Law Enforcement",
                "Regulatory Violation - Internal action taken",
                "Account Closure Recommended"
            ]

            selected_closure = st.selectbox(
                "Select Case Closure Type",
                options=closure_options,
                key="case_closure_type"
            )

            if st.button('Resolve Selected Case', key="resolve_case"):
                if st.session_state.case_id:
                    if selected_closure != "Select closure type":
                        if close_case(st.session_state.case_id, selected_closure):
                            connection = get_db_connection()
                            try:
                                with connection.cursor() as cursor:
                                    cursor.execute(
                                        "UPDATE transactions SET review_status = %s, closure_type = %s WHERE id = %s",
                                        ("reviewed", selected_closure, alert_id)
                                    )
                                    connection.commit()
                                st.success('Case resolved and closed successfully.')
                                del st.session_state['selected_alert_id']
                            finally:
                                connection.close()
                        else:
                            st.error("Failed to close the case in MongoDB. Please try again.")
                    else:
                        st.warning("Please select a valid closure type before resolving the case.")
                else:
                    st.warning("Please start a case review before resolving the case.")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.write("## Case Details")
            st.write(f"**From Bank:** {alert_details[1]}")
            st.write(f"**From Account:** {alert_details[2]}")
            st.write(f"**To Bank:** {alert_details[3]}")
            st.write(f"**To Account:** {alert_details[4]}")
            st.write(f"**Amount Received:** {alert_details[5]} {alert_details[6]}")
            st.write(f"**Amount Paid:** {alert_details[7]} {alert_details[8]}")
        with col2:
            st.write("### Enhanced Entity Relations Graph")
            show_entity_graph(alert_id, from_account)

        st.write("## Documents")
        uploaded_file = st.file_uploader("Upload Document", key="document_uploader")
        if uploaded_file is not None:
            if st.session_state.case_id:
                document_data = {
                    "name": uploaded_file.name,
                    "content": base64.b64encode(uploaded_file.getvalue()).decode('utf-8'),
                    "type": uploaded_file.type
                }
                if add_document_to_case(st.session_state.case_id, document_data):
                    st.success(f"Document '{uploaded_file.name}' uploaded successfully!")
                else:
                    st.error("Failed to upload document.")
            else:
                st.error("No active case. Please start a case review first.")

    with tab2:
        if client_details:
            show_entities_section(client_details)
        else:
            st.error("No client details found for this alert.")

    with tab3:
        narrative_content = show_narrative_tab(alert_details, client_details)
        if narrative_content:
            if update_narrative(st.session_state.case_id, narrative_content):
                st.success("Narrative updated successfully.")
            else:
                st.error("Failed to update narrative.")

def fetch_alert_details(alert_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM transactions WHERE id = %s"
            cursor.execute(query, (alert_id,))
            alert_details = cursor.fetchone()
            return alert_details
    finally:
        connection.close()

def fetch_client_details(from_account):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM client_kyc WHERE from_account = %s"
            cursor.execute(query, (from_account,))
            client_details = cursor.fetchone()
            return client_details
    except Exception as e:
        st.error(f"Error fetching client details: {e}")
        return None
    finally:
        connection.close()