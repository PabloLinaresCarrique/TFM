import pymysql
import os
import boto3  # AWS S3 library
from botocore.exceptions import NoCredentialsError
from pymongo import MongoClient, errors  # MongoDB Client and Errors
import streamlit as st

# Retrieve database credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Retrieve AWS credentials and S3 bucket name from environment variables
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_REGION = os.getenv('S3_REGION', 'us-east-1')  # Default region if not specified

# Retrieve MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")  # Ensure the MONGO_URI is set in your environment variables

def get_db_connection():
    """
    Establishes a connection to the MySQL database using credentials from environment variables.
    """
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Database connection successful.")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None

def init_db():
    """
    Initializes the database by creating necessary tables if they do not exist.
    """
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(255) PRIMARY KEY,
                    password VARCHAR(255) NOT NULL
                )
            ''')
            conn.commit()
            print("Database initialized successfully.")
    except pymysql.MySQLError as e:
        print(f"Error initializing the database: {e}")
    finally:
        conn.close()

def get_s3_client():
    """
    Establishes a connection to the Amazon S3 service using credentials from environment variables.
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=S3_REGION
        )
        print("S3 client connection successful.")
        return s3_client
    except NoCredentialsError as e:
        print(f"Error connecting to S3: {e}")
        return None

def get_image_from_s3(bucket_name, image_key):
    """
    Retrieves an image from an S3 bucket.

    :param bucket_name: Name of the S3 bucket
    :param image_key: The key (file name) of the image in the bucket
    :return: Image data in bytes, or None if retrieval fails
    """
    s3_client = get_s3_client()
    if s3_client is None:
        print("Failed to create S3 client.")
        return None

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=image_key)
        print(f"Image '{image_key}' retrieved successfully from bucket '{bucket_name}'.")
        return response['Body'].read()
    except Exception as e:
        print(f"Error retrieving image from S3: {e}")
        return None

def get_mongo_connection():
    """
    Establishes a connection to the MongoDB database using the provided URI from environment variables.
    """
    if not MONGO_URI:
        st.error("MONGO_URI environment variable is not set. Please set it in your environment.")
        return None
    else:
        try:
            # Connect to MongoDB using the provided URI
            client = MongoClient(MONGO_URI)
            db_name = "cortex"  # Replace with your actual database name
            db = client[db_name]  # Use the database name explicitly
            print("MongoDB connection successful.")
            return db
        except errors.PyMongoError as e:
            st.error(f"Failed to connect to MongoDB: {e}")
            return None

if __name__ == "__main__":
    init_db()
