from flask import Flask, request, jsonify
from flask_start import app
from flask_functions import make_prediction

model_name = "Laundering Investigation Model"
version = "v2.1.1"

@app.route('/info', methods=['GET'])
def info():
    """Mostrar información del modelo"""
    result = {
        "name": model_name,
        "version": version
    }
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    """Informar sobre la salud del servicio"""
    return "ok"

@app.route('/prediccion', methods=['POST'])
def prediccion():
    try:
        data = request.get_json(force=True)

        if not isinstance(data, list):
            return jsonify({"error": "Input data should be a list of objects"}), 400

        predictions = []
        for entry in data:
            prediction = make_prediction(entry)
            predictions.append(prediction)

        # Asegurarte de que todo lo que va en el JSON es serializable
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
