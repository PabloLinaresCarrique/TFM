import streamlit as st
from osint_search import perform_osint_search
from mongodb_case_management import add_entity_to_case, update_entity_to_case

def show_entities_section(client_details):
    st.write("## Entities")

    # Initialize session state for entity tabs if not already done
    if "entity_tabs" not in st.session_state:
        st.session_state.entity_tabs = ["Main Client"]
        st.session_state.entity_data = {
            "Main Client": {
                "name": client_details[5] if client_details else "",
                "age": client_details[1] if client_details else "",
                "job": client_details[2] if client_details else "",
                "marital_status": client_details[3] if client_details else "",
                "education": client_details[4] if client_details else "",
            }
        }

    # Button to add new entity tab
    if st.button("+ Add Entity Tab", key="add_entity_tab"):
        new_tab_name = f"Entity {len(st.session_state.entity_tabs) + 1}"
        st.session_state.entity_tabs.append(new_tab_name)
        st.session_state.entity_data[new_tab_name] = {
            "name": "",
            "age": "",
            "job": "",
            "marital_status": "",
            "education": ""
        }

        # Add entity to the case if a case review has started
        if st.session_state.case_id:
            entity_data = {
                "name": "",
                "age": "",
                "job": "",
                "marital_status": "",
                "education": ""
            }
            if add_entity_to_case(st.session_state.case_id, new_tab_name, entity_data):
                st.success(f"New entity '{new_tab_name}' added successfully!")
            else:
                st.error(f"Failed to add new entity '{new_tab_name}'.")

    # Create tabs for each entity
    entity_tabs = st.tabs(st.session_state.entity_tabs)

    # Loop through each entity tab to handle its contents
    for i, tab_name in enumerate(st.session_state.entity_tabs):
        with entity_tabs[i]:
            # Retrieve existing data from session state
            entity_data = st.session_state.entity_data[tab_name]

            # Button to perform OSINT search for each entity
            if st.button("OSINT Search", key=f"osint_button_{i}"):
                name = entity_data.get("name", "")
                job = entity_data.get("job", "")
                country = st.session_state.get(f"client_country_{i}", "")
                perform_osint_search(name, job, country)

            st.write("#### Internal Records")

            # Show input fields for the main client or additional entities
            name = st.text_input("Name", entity_data.get("name", ""), key=f"client_name_{i}")
            age = st.text_input("Age", entity_data.get("age", ""), key=f"client_age_{i}")
            job = st.text_input("Job", entity_data.get("job", ""), key=f"client_job_{i}")
            marital_status = st.text_input("Marital Status", entity_data.get("marital_status", ""), key=f"client_marital_status_{i}")
            education = st.text_input("Education", entity_data.get("education", ""), key=f"client_education_{i}")

            # Save changes to entity data
            if st.button(f"Save Entity Data", key=f"save_entity_data_{tab_name}_{i}"):
                # Update the entity data in session state
                st.session_state.entity_data[tab_name] = {
                    "name": name,
                    "age": age,
                    "job": job,
                    "marital_status": marital_status,
                    "education": education
                }

                # Prepare the updated entity data for MongoDB
                entity_data = {
                    "name": name,
                    "age": age,
                    "job": job,
                    "marital_status": marital_status,
                    "education": education
                }

                # Update or add entity data in MongoDB
                if st.session_state.case_id:
                    if update_entity_to_case(st.session_state.case_id, tab_name, entity_data):
                        st.success("Entity data saved successfully!")
                    else:
                        st.error("Failed to save entity data.")
                else:
                    st.warning("No active case. Please start a case review first.")
