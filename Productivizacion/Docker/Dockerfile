# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
EXPOSE 8000
CMD ["python", "flask_launch.py"]