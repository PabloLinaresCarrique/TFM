# TFM

# ENTRENAMIENTO_MODELO

- ModeloXGBoost.ipynb es el notebook con el entrenamiento del modelo de machine learning XGBoost que se productivizará.
- ModeloRandomForest.ipynb es un notebook que contiene uno de los modelos con los que se ha comparado ModeloXGBoost.ipynb.
- LabelEncodersCreacion.ipynb es el archivo con el que se crean los label encoders para los modelos.

# ÚTILES

- Datasets: contiene el enlace de descarga de los datasets utilizados.
- Label Encoders: contiene los label encoders usados en el modelo, comprimidos.
- Modelo (carpeta): contiene el archivo pickle comprimido del modelo que se utiliza para la productivización del mismo.


# PRODUCTIVIZACIÓN

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

# NOTEBOOK_DE_PREDICCIONES

- Notebook_Predicciones.ipynb es el notebook que realiza las predicciones para la plataforma que sustituye a la productivización del modelo mediante Flask y Docker


# PLATAFORMA

CortexNeural AML Platform es una solución integral de Anti-Lavado de Dinero (AML) diseñada para ayudar a las instituciones financieras a detectar, analizar y reportar actividades sospechosas. Esta plataforma integra técnicas avanzadas de machine learning con sistemas basados en reglas tradicionales para proporcionar un marco sólido de AML.

-Demo en vivo
La plataforma está desplegada y accesible en: www.cortexplatforms.com

## Características

- **Autenticación de Usuario**: Sistema de inicio de sesión y registro seguro para miembros del equipo.
- **Panel de Casos AML**: Panel interactivo para revisar y gestionar casos de AML.
- **Detalles de Alertas**: Vista detallada de alertas individuales con gráficos mejorados de relaciones entre entidades.
- **Asistente Virtual**: Chatbot con IA para responder preguntas sobre procedimientos de AML.
- **Panel de Administración**: Herramientas administrativas para la gestión de inventario y control de privilegios de usuarios.
- **Búsqueda OSINT**: Capacidades de búsqueda de inteligencia de fuentes abiertas para una debida diligencia mejorada.
- **Visor de PDF**: Visor integrado para documentos relacionados con AML almacenados en Amazon S3.

## Stack Tecnológico

- **Frontend**: Streamlit
- **Backend**: Python
- **Bases de Datos**: MySQL, MongoDB
- **Servicios en la Nube**: Amazon S3
- **Machine Learning**: OpenAI GPT, FAISS para almacenamiento vectorial
- **Visualización**: NetworkX, PyVis
- **Bibliotecas Adicionales**: pandas, PyPDF2, langchain, pymongo, boto3
- **Despliegue**: Heroku

## Configuración e Instalación (para desarrollo local)

1. Clonar el repositorio.
2. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Configurar variables de entorno:

Credenciales de la base de datos (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
Credenciales de AWS (AWS_ACCESS_KEY, AWS_SECRET_KEY)
URI de MongoDB (MONGO_URI)
Clave de API de OpenAI (OPENAI_API_KEY)

4.Inicializar la base de datos:
   ```
   python utils.py
   ```
5. Ejecutar la aplicación localmente:
   ```
   streamlit run app.py
   ```
## Estructura del Proyecto:

- `app.py`: Punto de entrada principal de la aplicación.
- `login.py`: Módulo de autenticación de usuarios.
- `dashboard.py`: Panel de casos AML.
- `alert_details.py`: Vista detallada de alertas individuales.
- `chatbot.py`: Implementación del asistente virtual.
- `admin_dashboard.py`: Funcionalidades de administración.
- `osint_search.py`: Módulo de búsqueda de inteligencia de fuentes abiertas.
- `pdf_viewer.py`: Módulo de visualización de PDF.
- `utils.py`: Funciones de utilidad para conexiones a bases de datos y S3.
- `requirements.txt`: Lista de dependencias del proyecto.

## Uso
1. Acceder a la plataforma en [www.cortexplatforms.com](https://www.cortexplatforms.com)
2. Iniciar sesión o registrar una nueva cuenta de usuario.
3. Navegar por el panel para revisar casos de AML.
4. Utilizar el asistente virtual para obtener orientación sobre procedimientos de AML.
5. Los administradores pueden acceder a funciones adicionales a través del Panel de Administración.

- Notas de Seguridad
Asegurarse de que toda la información sensible esté almacenada de forma segura y no expuesta en el código fuente.
Actualizar regularmente las dependencias para corregir vulnerabilidades de seguridad.
Implementar controles de acceso adecuados y prácticas de cifrado de datos.

Despliegue
La aplicación está desplegada en Heroku. Para obtener información sobre el despliegue de aplicaciones Streamlit en Heroku, consulta la guía de despliegue de Streamlit. [Streamlit deployment guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/heroku).






