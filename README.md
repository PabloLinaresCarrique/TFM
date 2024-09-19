# TFM

# Entremaiento_modelo

- ModeloXGboost.ipynb es el notebook con el entrenamiento del modelo de machine learningn XGBoost que se productivizará
- ModeloRandomForest.ipynb es un notebook que contiene uno de los modelos con el que se ha comparado ModeloXGboost.ipynb
- LabelEncodersCreacion.ipynb es el archivo con el que se crean los label encoders para los modelos

# Útiles

- Datasets: contiene el link de descarga de los datasets utilizados
- Label Encoders: contiene los label encoders usados en el modelo comprimidos
- Modelo (carpeta) : contiene el archivo pickle comprimido del modelo que se utiliza para la productivización del modelo 


# Productivización

- Docker (carpeta): contiene los archivos para la creación del Docker:
  - model (carpeta): contiene los archivos pickle del modelo y los label encoders del modelo
  - Dockerfile (IMPORTATE que el archivo sea sin formato, es decir, sin .txt) es el dockerfile usado en la creación del Docker
  - Flask.functions.py realiza predicciones transformando datos de entrada, devolviendo etiquetas y probabilidades, y guarda el historial de predicciones en un archivo JSON.
  - Flask_launch.py: Configura la API web, definiendo rutas para información, estado y predicciones, y arranca el servidor.
  - Flask_start.py: Carga el modelo y los codificadores con joblib, proporcionando funciones para acceder a ellos sin recargarlos constantemente.
  - requirements.txt contiene las librerías necesarias para la creación del Docker (incluida gunicorn)
    
- predictions_history.json es el archivo en el que se han guardado las predicciones realizadas al Docker, no al Flask directamente. (No está en la carpeta Docker para separarlo del directorio de la creación del Docker). "label:positive" significa que es un caso probable de Laundering (equivaldría a "Is_Laundering : 1)
- data.json es el archivo de datos de entrada con el que se hace la peticion y que se guardan en predictions_history.json
- Códigos_Docker.txt contiene los códigos para crear y usar los endpoints de nuestro docker en consola
  
- Flask (carpeta): contiene los archivos para hacer la predicción mediante Flask:
  - Flask_launch.ipynb es para crear el servidor local de Flask. Es necesario mantenerlo activo en jupyter notebook para hacer las peticiones
  - Flask_predicción.ipynb es para realizar las peticiones en otra instancia de jupyter notebook


# Notebook_de_predicciones

- Notebook_Predicciones.ipynb es el notebook que realiza las predicciones para la plataforma que sustituye a la productivización del modelo mediante Flask y Docker

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

Anti-Money Laundering (AML) Case Management System
This project is an Anti-Money Laundering (AML) case management system with various components to help analysts manage, review, and resolve AML cases efficiently.

Table of Contents
Main Application (app.py)
User Authentication (login.py)
Dashboard (dashboard.py)
Alert Details (alert_details.py)
Entities Management (entities.py)
OSINT Search (osint_search.py)
Narrative Component (narrative_component.py)
MongoDB Case Management (mongodb_case_management.py)
Enhanced Entity Graph (enhanced_entity_graph.html)
PDF Viewer (pdf_viewer.py)
Chatbot (chatbot.py)
Database Utilities (utils.py)
Technologies Used
Main Application (app.py)
The main entry point of the application is app.py. It sets up the Streamlit interface and manages the overall flow of the application. Key features include:

User authentication (login/logout)
Navigation between different sections (Dashboard, Alert Details, Virtual Assistant)
Personalized welcome message
User Authentication (login.py)
This module handles user registration and login functionalities. It includes:

User registration with fields for username, password, first name, last name, and team
Password hashing for security
User verification against a database
Dashboard (dashboard.py)
The dashboard provides an overview of AML cases that need review. Key features:

Fetches alerts from the database
Displays a list of cases to be reviewed
Allows selection of a specific case for a detailed view
Alert Details (alert_details.py)
This module shows detailed information about a selected alert. Features include:

Transaction details
Client information
Enhanced entity relations graph
Case review functionality (start review, resolve case)
Document upload capability
Entities Management (entities.py)
Handles the display and management of entities related to a case. Key features:

Adding new entity tabs
Displaying entity information
OSINT (Open Source Intelligence) search functionality
OSINT Search (osint_search.py)
Provides open-source intelligence search capabilities for entities. Includes:

Google search
LinkedIn search
Adverse media search
Company registry search
Sanctions search
Narrative Component (narrative_component.py)
Allows users to create and edit narratives for cases. Features include:

A rich text editor (Quill)
AI-assisted risk factor generation using OpenAI's GPT model
MongoDB Case Management (mongodb_case_management.py)
Handles interactions with MongoDB for case management. It includes:

Creating, updating, and retrieving cases
Adding entities and documents to cases
Updating narratives
Closing cases
Enhanced Entity Graph (enhanced_entity_graph.html)
Visualizes relationships between entities in a graph format.

PDF Viewer (pdf_viewer.py)
Allows viewing of PDF documents within the application.

Chatbot (chatbot.py)
Mentioned in the main app, but specific details are not provided in the given files.

Database Utilities (utils.py)
Provides database connection functionality for MySQL.

Technologies Used
The project utilizes several technologies and libraries:

Streamlit for the web interface
MySQL for storing user data and transactions
MongoDB for case management
OpenAI API for generating risk factor analyses
Various Python libraries for data manipulation, visualization, and PDF handling
Feel free to explore each module to understand its full functionality and how it integrates into the AML case management workflow.








