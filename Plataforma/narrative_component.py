import streamlit as st
from streamlit_quill import st_quill
from openai import OpenAI
from dotenv import load_dotenv
import os
from mongodb_case_management import update_narrative

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_narrative_template(alert_details, client_details):
    """
    Generates a narrative template pre-loaded with transaction and client details.
    """
    # Ensure alert_details and client_details are not None
    if not alert_details or not client_details:
        return "Error: Missing transaction or client details."

    # Extract necessary details for pre-loading
    transaction_details = f"""
<h2><b>Transaction Details</b></h2>
<br>
<br>
<p><b>From Bank:</b> {alert_details[1] if len(alert_details) > 2 else 'N/A'}</p>
<p><b>From Account:</b> {alert_details[2] if len(alert_details) > 3 else 'N/A'}</p>
<p><b>To Bank:</b> {alert_details[3] if len(alert_details) > 4 else 'N/A'}</p>
<p><b>To Account:</b> {alert_details[4] if len(alert_details) > 5 else 'N/A'}</p>
<p><b>Amount Received:</b> {alert_details[5] if len(alert_details) > 6 else 'N/A'} {alert_details[6] if len(alert_details) > 7 else ''}</p>
<p><b>Amount Paid:</b> {alert_details[7] if len(alert_details) > 8 else 'N/A'} {alert_details[8] if len(alert_details) > 9 else ''}</p>
<p><b>Payment Format:</b> {alert_details[9] if len(alert_details) > 10 else 'N/A'}</p>
<br>
"""

    client_info = f"""
<h2><b>Client Details</b></h2>
<br>
<br>
<p><b>Name:</b> {client_details[5] if len(client_details) > 5 else 'N/A'}</p>
<p><b>Age:</b> {client_details[1] if len(client_details) > 1 else 'N/A'}</p>
<p><b>Job:</b> {client_details[2] if len(client_details) > 2 else 'N/A'}</p>
<p><b>Marital Status:</b> {client_details[3] if len(client_details) > 3 else 'N/A'}</p>
<p><b>Education:</b> {client_details[4] if len(client_details) > 4 else 'N/A'}</p>
<br>
<br>
"""

    # Make sure the user's name is in the session state
    first_name = st.session_state.get("first_name", "User")  # Default to "User" if not set

    # Combine sections into the narrative template
    narrative_template = f"""
<h1><b>Transaction Monitoring Report</b></h1>
<br>
<br>
{transaction_details}
{client_info}
<h2><b>Risk Factors</b></h2>
<br>
<p>[Press the "Run Risk Analysis" button to generate an Analysis]</p>
<br>
<h2><b>2nd Level Analyst Review & Conclusion</b></h2>
<br>
<br>
<div style="text-align: center;">
  <p>Report generated using Automation and LLM Technology, Reviewed and Validated by {first_name}</p>
</div>
"""

    return narrative_template

def generate_risk_factors_paragraph(alert_details, client_details):
    """
    Generate a paragraph outlining the main risk factors identified using OpenAI API.
    """
    # Prepare the new prompt for the OpenAI API
    prompt = f"""
Generate a well-structured paragraph that outlines the main risk factors identified based on the provided transaction and client details. The output should be clear, concise, and formatted consistently according to the following guidelines:

1. Begin with an introductory sentence that provides context, such as, "The analysis of the following transaction and client details reveals several key risk factors."
   
2. Continue with a cohesive paragraph that describes the risk factors identified. For each risk factor, write one or two sentences explaining what the risk factor is and why it is considered significant. Ensure that the explanation flows naturally and maintains a logical progression between the different risk factors. Avoid listing the risk factors; instead, integrate them seamlessly into the narrative (e.g., "One significant risk factor is the high transaction volume relative to the client's average, which could indicate potential money laundering activity. Another concern is the presence of multiple transactions to high-risk jurisdictions...").

3. Conclude the paragraph with a sentence that summarizes the overall risk level or provides a recommendation based on the identified factors, such as, "Overall, these factors suggest a heightened level of risk that warrants further investigation."

4. Add a new section titled "Suggested Steps" at the end of the analysis. This section should provide specific, actionable steps or recommendations that could be taken in response to the identified risk factors. The steps should be practical and directly related to the risk factors discussed in the paragraph. For example, "Suggested Steps: 1. Conduct enhanced due diligence on the client's recent transactions to identify any patterns of suspicious activity. 2. Monitor future transactions involving high-risk jurisdictions closely. 3. Consider filing a Suspicious Activity Report (SAR) if the activity continues to raise concerns."

Ensure that the paragraph is between 100 to 150 words and maintains a formal and analytical tone throughout.

Transaction and Client Details:
{create_narrative_template(alert_details, client_details)}

Risk Factors and Suggested Steps:
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial analyst specializing in risk assessment."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=350,  
            temperature=0.7  
        )

        # Extract the generated text
        risk_factors_paragraph = response.choices[0].message.content.strip()
        return risk_factors_paragraph

    except Exception as e:
        st.error(f"Error generating risk factors: {e}")
        return ""

def create_narrative_component(alert_details, client_details):
    st.title("Transaction Monitoring Report - Narrative")

    # Generate the narrative template for the selected case
    narrative_template = create_narrative_template(alert_details, client_details)

    # Check if the narrative content is initialized for the selected case
    if "narrative_content" not in st.session_state:
        st.session_state["narrative_content"] = narrative_template  # Pre-load the template for the selected case

    # Add a button to generate risk factors using OpenAI API
    if st.button("Run Risk Analysis", key="generate_risk_factors"):
        with st.spinner("Generating risk factors..."):
            risk_factors = generate_risk_factors_paragraph(alert_details, client_details)
            if risk_factors:
                # Replace placeholder text with generated risk factors
                updated_content = st.session_state["narrative_content"].replace(
                    "[Press the \"Run Risk Analysis\" button to generate an Analysis]", risk_factors
                )
                st.session_state["narrative_content"] = updated_content  
                st.success("Risk factors generated and added to the narrative!")

    # Re-render the Quill editor with the current content
    narrative = st_quill(
        value=st.session_state["narrative_content"],
        placeholder="Write your narrative here...",
        html=True,
        readonly=False,
        key="quill_editor"
    )

    # Update the session state with the current editor content
    if narrative is not None and narrative != st.session_state["narrative_content"]:
        st.session_state["narrative_content"] = narrative  # Update session state

    # Add a save button to save the content
    if st.button("Save Narrative", key="save_narrative"):
        if st.session_state["narrative_content"]:
            if update_narrative(st.session_state.case_id, st.session_state["narrative_content"]):
                st.success("Narrative saved successfully!")
            else:
                st.error("Failed to save narrative.")
        else:
            st.warning("No content to save.")

def show_narrative_tab(alert_details, client_details):
    # Call the narrative component function with the necessary data
    create_narrative_component(alert_details, client_details)
