import os
import pymysql
import streamlit as st

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('34.175.239.169'),         # IP pública o nombre del host
        user=os.getenv('root'),         # Nombre de usuario de la base de datos
        password=os.getenv('cortexTFM'), # Contraseña de la base de datos
        database=os.getenv('aml_system'),     # Nombre de la base de datos
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_users():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
    finally:
        conn.close()
    return users

def main():
    st.title("Usuarios de la Base de Datos")

    # Consultar usuarios de la base de datos
    users = fetch_users()

    # Mostrar los datos en la aplicación de Streamlit
    if users:
        st.write("Usuarios encontrados:")
        st.dataframe(users)  # Muestra los datos en una tabla interactiva
    else:
        st.write("No se encontraron usuarios.")

if __name__ == "__main__":
    main()
