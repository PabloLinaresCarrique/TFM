# TFM

# Entrenamiento_modelo

- ModeloXGBoost.ipynb es el notebook con el entrenamiento del modelo de machine learning XGBoost que se productivizará.
- ModeloRandomForest.ipynb es un notebook que contiene uno de los modelos con los que se ha comparado ModeloXGBoost.ipynb.
- LabelEncodersCreacion.ipynb es el archivo con el que se crean los label encoders para los modelos.

# Útiles

- Datasets: contiene el enlace de descarga de los datasets utilizados.
- Label Encoders: contiene los label encoders usados en el modelo, comprimidos.
- Modelo (carpeta): contiene el archivo pickle comprimido del modelo que se utiliza para la productivización del mismo.


# Productivización

- Docker (carpeta): contiene los archivos para la creación del Docker:
  - model (carpeta): contiene los archivos pickle del modelo y los label encoders.
  - Dockerfile (IMPORTANTE: el archivo debe estar sin formato, es decir, sin extensión .txt), es el dockerfile usado en la creación del Docker.
  - Flask.functions.py: realiza predicciones transformando los datos de entrada, devolviendo etiquetas y probabilidades, y guarda el historial de predicciones en un archivo JSON.
  - Flask_launch.py: configura la API web, definiendo rutas para información, estado y predicciones, y arranca el servidor.
  - Flask_start.py: carga el modelo y los codificadores con joblib, proporcionando funciones para acceder a ellos sin recargarlos constantemente.
  - requirements.txt: contiene las librerías necesarias para la creación del Docker (incluida gunicorn).

- predictions_history.json es el archivo en el que se han guardado las predicciones realizadas al Docker, no directamente en Flask. (No está en la carpeta Docker para separarlo del directorio de creación del Docker). "label:positive" significa que es un caso probable de "Laundering" (equivaldría a "Is_Laundering: 1").
- data.json es el archivo de datos de entrada con el que se hace la petición y se guardan en predictions_history.json.
- Códigos_Docker.txt contiene los códigos para crear y usar los endpoints de nuestro Docker en consola.
  
- Flask (carpeta): contiene los archivos para hacer la predicción mediante Flask:
  - Flask_launch.ipynb: para crear el servidor local de Flask. Es necesario mantenerlo activo en Jupyter Notebook para hacer las peticiones.
  - Flask_predicción.ipynb: para realizar las peticiones en otra instancia de Jupyter Notebook.
  - 

# Notebook_de_predicciones

- Notebook_Predicciones.ipynb es el notebook que realiza las predicciones para la plataforma que sustituye a la productivización del modelo mediante Flask y Docker


# CortexNeural AML Platform

## Overview
CortexNeural AML Platform is a comprehensive Anti-Money Laundering (AML) solution designed to assist financial institutions in detecting, analyzing, and reporting suspicious activities. This platform integrates advanced machine learning techniques with traditional rule-based systems to provide a robust AML framework.

## Live Demo
The platform is deployed and accessible at: [www.cortexplatforms.com](https://www.cortexplatforms.com)

## Features
- **User Authentication**: Secure login and registration system for team members.
- **AML Case Dashboard**: Interactive dashboard for reviewing and managing AML cases.
- **Alert Details**: Detailed view of individual alerts with enhanced entity relationship graphs.
- **Virtual Assistant**: AI-powered chatbot for answering questions about AML procedures.
- **Admin Dashboard**: Administrative tools for inventory management and user privilege control.
- **OSINT Search**: Open-source intelligence search capabilities for enhanced due diligence.
- **PDF Viewer**: Integrated viewer for AML-related documents stored in Amazon S3.

## Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Databases**: MySQL, MongoDB
- **Cloud Services**: Amazon S3
- **Machine Learning**: OpenAI GPT, FAISS for vector storage
- **Visualization**: NetworkX, PyVis
- **Additional Libraries**: pandas, PyPDF2, langchain, pymongo, boto3
- **Deployment**: Heroku

## Setup and Installation (for local development)
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Database credentials (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
   - AWS credentials (AWS_ACCESS_KEY, AWS_SECRET_KEY)
   - MongoDB URI (MONGO_URI)
   - OpenAI API key (OPENAI_API_KEY)

4. Initialize the database:
   ```
   python utils.py
   ```

5. Run the application locally:
   ```
   streamlit run app.py
   ```

## Project Structure
- `app.py`: Main application entry point
- `login.py`: User authentication module
- `dashboard.py`: AML case dashboard
- `alert_details.py`: Detailed view of individual alerts
- `chatbot.py`: Virtual assistant implementation
- `admin_dashboard.py`: Admin functionalities
- `osint_search.py`: Open-source intelligence search module
- `pdf_viewer.py`: PDF viewing module
- `utils.py`: Utility functions for database and S3 connections
- `requirements.txt`: List of project dependencies

## Usage
1. Access the platform at [www.cortexplatforms.com](https://www.cortexplatforms.com)
2. Log in or register a new user account.
3. Navigate through the dashboard to review AML cases.
4. Use the virtual assistant for guidance on AML procedures.
5. Administrators can access additional features through the Admin Dashboard.

## Security Notes
- Ensure all sensitive information is stored securely and not exposed in the codebase.
- Regularly update dependencies to patch any security vulnerabilities.
- Implement proper access controls and data encryption practices.

## Deployment
The application is deployed on Heroku. For information on deploying Streamlit apps on Heroku, refer to the [Streamlit deployment guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/heroku).






