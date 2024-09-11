import pandas as pd
import json
from datetime import datetime
import os
from flask_start import get_label_encoder, get_model


def make_prediction(data):
    """Realiza una predicción con los datos proporcionados y devuelve la etiqueta y la probabilidad."""
    label_encoder = get_label_encoder()
    model = get_model()

    # Convertir datos JSON a DataFrame
    df = pd.DataFrame([data])

    # Eliminar la columna 'Is Laundering' si está presente en los datos de entrada
    if 'Is Laundering' in df.columns:
        df = df.drop(columns=['Is Laundering'])

    # Transformaciones de 'Timestamp'
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df['Year'] = df['Timestamp'].dt.year
        df['Month'] = df['Timestamp'].dt.month
        df['Day'] = df['Timestamp'].dt.day
        df['Hour'] = df['Timestamp'].dt.hour
        df['Minute'] = df['Timestamp'].dt.minute
        df = df.drop(columns=['Timestamp'])

    # Transformar con label_encoder
    categorical_columns = ['Account2', 'Account4', 'Receiving Currency', 'Payment Currency', 'Payment Format']
    for col in categorical_columns:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = safe_transform(label_encoder, df[col], col)

    # Transformaciones a "Account4" individuales
    if 'Account4' in df.columns:
        try:
            df['Account4'] = df['Account4'].astype(float)
            df['Account4'] = df['Account4'].fillna(df['Account4'].mean())
        except Exception as e:
            print(f"Error al transformar 'Account4': {e}")

    # Convertir a numpy array, excluyendo las columnas que no sean numéricas
    numeric_df = df.select_dtypes(include=[float, int])

    # Convertir todos los datos a tipos estándar de Python (para evitar errores de conversión a JSON)
    data_to_numpy = numeric_df.apply(pd.to_numeric, errors='coerce').fillna(0).values.astype(float)

    # Hacer la predicción
    prediction = model.predict(data_to_numpy)
    probabilities = model.predict_proba(data_to_numpy)

    # Convertir predicciones a tipos nativos de Python
    prob_laundering = round(float(probabilities[0][1]), 4)  # Convertir a float estándar con 4 decimales
    prob_not_laundering = round(float(probabilities[0][0]), 4)  # Convertir a float estándar con 4 decimales

    # Determinar la etiqueta y la probabilidad a mostrar
    if prob_laundering >= 0.5:
        label = "Positive"
        probability = prob_laundering
    else:
        label = "Negative"
        probability = prob_not_laundering

    # Preparar las predicciones para guardar en JSON
    predictions = [{
        'label': label,
        'probability': probability
    }]

    # Guardar el historial
    save_to_json(predictions, data)

    return {
        'label': label,
        'probability': probability
    }


def save_to_json(predictions, input_data):
    """Guarda las predicciones en un archivo JSON, actualizando el historial."""
    file_path = 'predictions_history.json'

    # Cargar el historial existente si el archivo ya existe
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
    else:
        data = []

    # Agregar la nueva entrada al historial
    entry = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        "input_data": input_data,
        "results": predictions
    }
    data.append(entry)

    # Guardar el historial completo en el archivo
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def safe_transform(encoder_dict, series, column_name):
    """Transformar categorías con un encoder, manejando valores desconocidos."""
    if column_name not in encoder_dict:
        raise ValueError(f"No hay codificador para la columna {column_name}")

    encoder = encoder_dict[column_name]

    # Transformar valores usando el encoder y manejar valores desconocidos
    transformed_series = series.map(lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1)

    return transformed_series
