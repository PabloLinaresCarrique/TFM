
# AML Case Management Tool

## Overview
The AML (Anti-Money Laundering) Case Management Tool is a comprehensive application designed to help financial institutions manage and analyze suspicious activities efficiently. The tool incorporates various features like alert management, rule-based detection, aml assitant, and a user-friendly dashboard.

## Features
- **Alert Management**: Track, view, and manage AML alerts through the `alert_details.py` module.
- **Rule-Based Detection**: Connecting directly to SQL, Implement and apply AML rules to detect suspicious activities using `aml_rules.py`.
- **Interactive Dashboard**: Visualize alerts and data through an intuitive dashboard created in `dashboard.py`.
- **Chatbot Interaction**: A virtual AML Assitant to answer questions based on AML PEP & Sanctions Procedures.
- **User Authentication**: Secure login and authentication managed by `login.py`.
- **Utility Functions**: Connection to DBS and common utility functions are centralized in `utils.py` for reusability and cleaner code.

## Installation

1. Install the dependencies: 
- pip install -r requirements.txt

2. Run the app via streamlit
- streamlit run app.py

3. Access the dashboard via Local server 
- Typically : http://localhost:8501).
