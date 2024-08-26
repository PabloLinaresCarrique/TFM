# TFM

# Modelos

- La página de Modelo Random Forest Correcto --> Hace referencia al modelo balanceado y entrenado de Random forest
- La página de PipeLine --> Hace referencia a la prueba del modelo anterior entrenado y guardado en una Pipeline para poder productivizar el modelo
- La página de Prueba_de_Pipiline --> Hace referencia a la prueba del modelo anterior pero con otro dataset
- - La carpeta de Modelo,  Modelo_Random_Forest_Analizado --> Hace referencia al modelo tras el análisis y con gráficos
- Model.pkl  es el archivo pickle del modelo que se carga en Flask para la productivización del modelo
- label_encoder.pkl es el archivo con los encoders usados en el modelo que se carga en Flask para la productivización del modelo. Necesario pata transformar automáticamente nuevos datos cuando se hacen peticiones

# Productivización

- Flask_launch es para crear el servidor local de Flask. Es necesario mantenerlo activo en jupyter notebook para hacer las peticiones (aparece el símbolo de cargando en la página)
- Flask_predicción es para realizar las peticiones en otra instancia de jupyter notebook

# Platform

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
