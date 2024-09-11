#!/usr/bin/env python
# coding: utf-8
# prompt: necesito cargar datos de un csv que se llama export.csv de drive

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

# Carga de los datasets
hi_small = pd.read_csv('HI-Small_Trans.csv')
low_small = pd.read_csv('LI-Small_Trans.csv')
#low_medium = pd.read_csv('/content/drive/MyDrive/Modelo 4 Septiembre/HI-Medium_Trans.csv')
hi_small1 = hi_small.copy()
low_small1 = low_small.copy()

hi_small = hi_small1.copy()
low_small = low_small1.copy()
#low_medium = low_medium1.copy()
total_datos = low_small.shape[0]
print("Total de datos en low_small:", total_datos)
hi_small.head()
hi_small.rename(columns={'Account': 'Account2', 'Account.1': 'Account4'}, inplace=True)
low_small.rename(columns={'Account': 'Account2', 'Account.1': 'Account4'}, inplace=True)
#low_medium.rename(columns={'Account': 'Account2', 'Account.1': 'Account4'}, inplace=True)
# Filtrar el DataFrame para obtener registros donde "Is Laundering" == 1
filtered_df = hi_small[hi_small['Is Laundering'] == 1]

# Obtener solo los primeros dos registros
two_records_df = filtered_df.head(2)

print(two_records_df)
df_unido =  pd.concat([hi_small, low_small], ignore_index=True)
#df_unido =  pd.concat([hi_small, low_small, low_medium], ignore_index=True)
porcentaje_ones = df_unido['Is Laundering'].value_counts(normalize=True).get(1, 0) * 100
porcentaje_zeros = df_unido['Is Laundering'].value_counts(normalize=True).get(0, 0) * 100

print(f"Porcentaje de 1s: {porcentaje_ones:.2f}%")
print(f"Porcentaje de 0s: {porcentaje_zeros:.2f}%")
num_ones = df_unido['Is Laundering'].value_counts().get(1, 0)
num_zeros = df_unido['Is Laundering'].value_counts().get(0, 0)

print(f"Número de 1s: {num_ones}")
print(f"Número de 0s: {num_zeros}")
# Asegúrate de que la columna 'Timestamp' esté en formato datetime
df_unido['Timestamp'] = pd.to_datetime(df_unido['Timestamp'])

# Extraer Year, Month, Day, Hour, Minute
df_unido['Year'] = df_unido['Timestamp'].dt.year
df_unido['Month'] = df_unido['Timestamp'].dt.month
df_unido['Day'] = df_unido['Timestamp'].dt.day
df_unido['Hour'] = df_unido['Timestamp'].dt.hour
df_unido['Minute'] = df_unido['Timestamp'].dt.minute

df_unido.drop(columns=['Timestamp'], inplace=True)
categorical_columns = ['From Bank', 'To Bank', 'Receiving Currency', 'Payment Currency', 'Payment Format', 'Account2', 'Account4']

from sklearn.preprocessing import LabelEncoder
import pickle

# Suponiendo que tienes columnas categóricas que necesitas codificar
label_encoders = {}
categorical_columns = ['From Bank', 'To Bank', 'Receiving Currency', 'Payment Currency', 'Payment Format', 'Account2', 'Account4']

for col in categorical_columns:
    le = LabelEncoder()
    df_unido[col] = le.fit_transform(df_unido[col])
    label_encoders[col] = le

import pickle

# Guardar los LabelEncoders en un archivo local
with open('label_encoders1.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

#Pruebas del modelo
#Modelo: Se va a entrenar el modelo con el dataframe de Li Small y luego se hara un test sobre HI Small

num_ones = low_small['Is Laundering'].value_counts().get(1, 0)
num_zeros = low_small['Is Laundering'].value_counts().get(0, 0)

print(f"Número de 1s: {num_ones}")
print(f"Número de 0s: {num_zeros}")
low_small['Timestamp'] = pd.to_datetime(low_small['Timestamp'])

# Extraer Year, Month, Day, Hour, Minute
low_small['Year'] = low_small['Timestamp'].dt.year
low_small['Month'] = low_small['Timestamp'].dt.month
low_small['Day'] = low_small['Timestamp'].dt.day
low_small['Hour'] = low_small['Timestamp'].dt.hour
low_small['Minute'] = low_small['Timestamp'].dt.minute
low_small.drop(columns=['Timestamp'], inplace=True)
low_small.rename(columns={'Account': 'Account2', 'Account.1': 'Account4'}, inplace=True)
low_small.head()
# Ruta al archivo local con los LabelEncoders guardados
path_to_encoders = 'label_encoders1.pkl'

# Cargar los LabelEncoders guardados
with open(path_to_encoders, 'rb') as f:
    label_encoders = pickle.load(f)

# Aplicar los LabelEncoders al dataset "low_small"
for col, le in label_encoders.items():
    if col in low_small.columns:
        low_small[col] = le.transform(low_small[col])

print("LabelEncoders aplicados correctamente.")

#por alguna razón no he corrido la parte del notebook que unía los 3 datasets y he probado a cargar lo labelencoders y daba error de cosas no vistas, después de crear el archivo nuevo de label encoders "label_encoders1" corriendo todo otra vez pero en este caso cargándolos directamente desde el drive si que ha funcionado, no entiendo muy bien el porqué. SI VUELVE A DAR ERROR LO MEJOR VA A SER GUARDARLOS POR SEPARADO LOS LABEL_ENCODER Y NO EN EL MISMO ARCHIVO QUE IGUAL ES POR ES0.

#A PARTIR DE AQUÍ ES MÍO NUEVO
#Separamos el 70/30

# Separar las filas con 1s y 0s
fraudes = low_small[low_small['Is Laundering'] == 1]
no_fraudes = low_small[low_small['Is Laundering'] == 0]

# Calcular el número de 0s necesarios para lograr un 70% de 0s y 30% de 1s
num_zeros_requeridos = int(len(fraudes) * (70 / 30))

# Seleccionar aleatoriamente los 0s requeridos
no_fraudes_submuestreado = no_fraudes.sample(n=num_zeros_requeridos, random_state=42)

# Combinar los 1s con los 0s seleccionados
low_small_balanceado = pd.concat([fraudes, no_fraudes_submuestreado])

# Mezclar aleatoriamente el dataframe resultante
low_small = low_small_balanceado.sample(frac=1, random_state=42).reset_index(drop=True)


# 7. Volver a nombrar el dataset como low_small
low_small = low_small_balanceado.copy()
#Hacemos uno de validación y otro de prueba según recomendaban

# Supongamos que low_small es tu nuevo dataset

X = low_small.drop('Is Laundering', axis=1)  # Características
y = low_small['Is Laundering']  # Variable objetivo

# Dividir en entrenamiento (60%), validación (20%) y prueba (20%)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.40, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42)
# Entrenar el modelo ajustando el peso de la clase

model = RandomForestClassifier(class_weight={0: 1, 1: 10}, random_state=42)  # Ajuste de pesos
model.fit(X_train, y_train)
#aunque ponga lo del ajuste de pesos no he tocado nada ahí del peso

#Validación

# Evaluar el modelo en el conjunto de validación
y_val_pred = model.predict(X_val)

# Reporte de clasificación para validación
print("Reporte de clasificación en el conjunto de validación:")
print(classification_report(y_val, y_val_pred))
y_val_pred
Test

# Predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print("Matriz de Confusión:")
print(cm)
# Evaluación del modelo
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
#Ajustes en los umbrales
#umbral de 0,2

# Asegúrate de calcular las probabilidades
y_probs = model.predict_proba(X_test)[:, 1]  # Obtén las probabilidades para la clase positiva

# Ajustar el umbral de decisión
threshold = 0.2  # Ajusta este valor según sea necesario
y_pred_adjusted = (y_probs >= threshold).astype(int)

# Evaluar el modelo con el umbral ajustado
print("Accuracy with adjusted threshold:", accuracy_score(y_test, y_pred_adjusted))
print("Classification Report with adjusted threshold:\n", classification_report(y_test, y_pred_adjusted))

# Generar la matriz de confusión
conf_matrix = confusion_matrix(y_test, y_pred_adjusted)

# Visualizar la matriz de confusión
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix with Adjusted Threshold')
plt.show()

#Ajuste de pesos
# Ajustar los pesos de las clases (poniendo más peso en la clase 1)
model_weighted = RandomForestClassifier(class_weight={0: 1, 1: 20}, random_state=42)

# Entrenar el modelo con los nuevos pesos
model_weighted.fit(X_train, y_train)

# Predecir con el modelo entrenado
y_pred_weighted = model_weighted.predict(X_test)

# Evaluar el modelo
print("Accuracy with class weights:", accuracy_score(y_test, y_pred_weighted))
print("Classification Report with class weights:\n", classification_report(y_test, y_pred_weighted))

# Generar la matriz de confusión
conf_matrix_weighted = confusion_matrix(y_test, y_pred_weighted)

# Visualizar la matriz de confusión
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_weighted, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix with Class Weights')
plt.show()

#Umbral ajustado a 0,25

# Obtener las probabilidades de la clase positiva (1)
y_probs = model_weighted.predict_proba(X_test)[:, 1]

# Ajustar el umbral de decisión
threshold = 0.25  # Puedes ajustar este valor según sea necesario

y_pred_adjusted = (y_probs >= threshold).astype(int)


# Evaluar el modelo con el umbral ajustado
print("Accuracy with adjusted threshold:", accuracy_score(y_test, y_pred_adjusted))
print("Classification Report with adjusted threshold:\n", classification_report(y_test, y_pred_adjusted))

# Generar la matriz de confusión
conf_matrix_adjusted = confusion_matrix(y_test, y_pred_adjusted)

# Visualizar la matriz de confusión
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_adjusted, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix with Adjusted Threshold')
plt.show()

#Umbral ajustado a 0,15

# Obtener las probabilidades de la clase positiva (1)
y_probs = model_weighted.predict_proba(X_test)[:, 1]

# Ajustar el umbral de decisión
threshold = 0.15  # Puedes ajustar este valor según sea necesario

y_pred_adjusted = (y_probs >= threshold).astype(int)
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Evaluar el modelo con el umbral ajustado
print("Accuracy with adjusted threshold:", accuracy_score(y_test, y_pred_adjusted))
print("Classification Report with adjusted threshold:\n", classification_report(y_test, y_pred_adjusted))

# Generar la matriz de confusión
conf_matrix_adjusted = confusion_matrix(y_test, y_pred_adjusted)

# Visualizar la matriz de confusión
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_adjusted, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix with Adjusted Threshold')
plt.show()

#Ajuste con el umbral de 0,15 y un peso de 30 al 1

# Ajustar los pesos de las clases de forma más agresiva
model_weighted_30 = RandomForestClassifier(class_weight={0: 1, 1: 30}, random_state=42)
model_weighted_30.fit(X_train, y_train)

# Evaluar el modelo con el umbral que funcionó mejor (por ejemplo, 0.15)
y_probs_weighted = model_weighted_30.predict_proba(X_test)[:, 1]
threshold = 0.15
y_pred_adjusted_weighted = (y_probs_weighted >= threshold).astype(int)

# Evaluar los resultados
print("Accuracy with adjusted class weights and threshold:", accuracy_score(y_test, y_pred_adjusted_weighted))
print("Classification Report:\n", classification_report(y_test, y_pred_adjusted_weighted))

# Mostrar la matriz de confusión
conf_matrix_weighted = confusion_matrix(y_test, y_pred_adjusted_weighted)
sns.heatmap(conf_matrix_weighted, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix with Adjusted Class Weights and Threshold')
plt.show()

#Con esto anterior hemos alcanzado lo maximo en cuanto a ajuste de psos y umbrales.

#Prueba del modelo en HI-Small
hi_small['Timestamp'] = pd.to_datetime(hi_small['Timestamp'])

# Extraer Year, Month, Day, Hour, Minute
hi_small['Year'] = hi_small['Timestamp'].dt.year
hi_small['Month'] = hi_small['Timestamp'].dt.month
hi_small['Day'] = hi_small['Timestamp'].dt.day
hi_small['Hour'] = hi_small['Timestamp'].dt.hour
hi_small['Minute'] = hi_small['Timestamp'].dt.minute
hi_small.drop(columns=['Timestamp'], inplace=True)
hi_small.rename(columns={'Account': 'Account2', 'Account.1': 'Account4'}, inplace=True)
hi_small.head()
for col, le in label_encoders.items():
    if col in hi_small.columns:
        hi_small[col] = le.transform(hi_small[col])
X_hi = hi_small.drop('Is Laundering', axis=1)
y_hi = hi_small['Is Laundering']
hi_small.head()
y_hi_pred = model.predict(X_hi)

# Evaluar el modelo
print("Accuracy on HI-Small:", accuracy_score(y_hi, y_hi_pred))
print("Classification Report on HI-Small:\n", classification_report(y_hi, y_hi_pred))

# Calcular la matriz de confusión
conf_matrix_hi = confusion_matrix(y_hi, y_hi_pred)

# Mostrar la matriz de confusión
print("Matriz de Confusión:\n", conf_matrix_hi)
#Prueba con modelo_weighetd_30 de peso en calse 1.
y_hi_pred = model_weighted_30.predict(X_hi)

# Evaluar el modelo
print("Accuracy on HI-Small:", accuracy_score(y_hi, y_hi_pred))
print("Classification Report on HI-Small:\n", classification_report(y_hi, y_hi_pred))

# Calcular la matriz de confusión
conf_matrix_hi = confusion_matrix(y_hi, y_hi_pred)

# Mostrar la matriz de confusión
print("Matriz de Confusión:\n", conf_matrix_hi)
#Entrenamiento de XBGOOST
#pip install xgboost

# Separar características (X) y la variable objetivo (y)
X = low_small.drop('Is Laundering', axis=1)
y = low_small['Is Laundering']

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train
# Inicializar el modelo XGBoost
model_xgb = xgb.XGBClassifier(random_state=42, scale_pos_weight=len(y_train) / sum(y_train))

# Entrenar el modelo
model_xgb.fit(X_train, y_train)
#Prueba en el modelo con el xgboost basico

# Predicciones en el conjunto de prueba
y_pred = model_xgb.predict(X_test)

# Calcular las probabilidades de la clase positiva
y_probs = model_xgb.predict_proba(X_test)[:, 1]

# Ajustar el umbral de decisión si es necesario
threshold = 0.5  # Puedes ajustar este valor si es necesario
y_pred_adjusted = (y_probs >= threshold).astype(int)

# Evaluar el rendimiento del modelo
print("Accuracy:", accuracy_score(y_test, y_pred_adjusted))
print("Classification Report:\n", classification_report(y_test, y_pred_adjusted))

# Mostrar la matriz de confusión
conf_matrix = confusion_matrix(y_test, y_pred_adjusted)
print("Confusion Matrix:\n", conf_matrix)

#Prueba de modelos ajustando hiperparámetros y umbrales

#Definir los hiperparámetros y el rango de búsqueda
param_grid = { 'scale_pos_weight': [10, 20, 30, 40], 'max_depth': [4, 6, 8], 'learning_rate': [0.01, 0.1, 0.2], 'n_estimators': [100, 200, 300] }

#Crear el modelo base
xgb_model = xgb.XGBClassifier(random_state=42)

#Usar GridSearchCV para encontrar la mejor combinación de hiperparámetros
#grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, cv=3, scoring='recall', verbose=2, n_jobs=-1) grid_search.fit(X_train, y_train)

#Obtener el mejor modelo encontrado por GridSearchCV
best_model = grid_search.best_estimator_

#Predecir usando el mejor modelo
y_probs = best_model.predict_proba(X_test)[:, 1]

#Ajustar el umbral y predecir
threshold = 0.3 # Puedes ajustar este valor y_pred_adjusted = (y_probs >= threshold).astype(int)

#Evaluar los resultados
accuracy = accuracy_score(y_test, y_pred_adjusted)
class_report = classification_report(y_test, y_pred_adjusted)
conf_matrix = confusion_matrix(y_test, y_pred_adjusted)

print(f"Best Parameters: {grid_search.best_params_}")
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(class_report)
print("Confusion Matrix:")
print(conf_matrix)

#El resultado obtenido, no ha sido el esperado por lo que procedo a cambiar el Umbral

# Probar con un umbral más bajo
threshold = 0.25
y_pred_adjusted = (y_probs >= threshold).astype(int)

# Evaluar de nuevo
accuracy = accuracy_score(y_test, y_pred_adjusted)
class_report = classification_report(y_test, y_pred_adjusted)
conf_matrix = confusion_matrix(y_test, y_pred_adjusted)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(class_report)
print("Confusion Matrix:")
print(conf_matrix)
#Los resultados han mejorado un poco tras los ajustes del umbral, el problema que estamos perdiendo mas datos que en el modelo donde no tocabamos los umbrales.

#En este tenemos menos falsos positivos pero perdemos mas datos y tenemos menos positivos

#Pruebo a hacer un nuevo ajuste con RandomizedSearchCV para hacer una busqueda nueva de valores, el objetivo es encontrar un equilibrio entre precision y recall

# Definir los hiperparámetros y el rango de búsqueda
param_dist = {
    'scale_pos_weight': [30, 40, 50, 60, 70],
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.05, 0.1, 0.15],
    'n_estimators': [200, 300, 400]
}

# Crear el modelo base
xgb_model = xgb.XGBClassifier(random_state=42)

# Configurar RandomizedSearchCV
random_search = RandomizedSearchCV(estimator=xgb_model, param_distributions=param_dist,
                                   n_iter=20, scoring='recall', cv=3, verbose=2, n_jobs=-1, random_state=42)

# Ajustar el modelo
random_search.fit(X_train, y_train)

# Obtener el mejor modelo encontrado por RandomizedSearchCV
best_model = random_search.best_estimator_

# Predecir usando el mejor modelo
y_probs = best_model.predict_proba(X_test)[:, 1]

# Ajustar el umbral y predecir
threshold = 0.25  # Ajusta este valor según sea necesario
y_pred_adjusted = (y_probs >= threshold).astype(int)

# Evaluar los resultados
accuracy = accuracy_score(y_test, y_pred_adjusted)
class_report = classification_report(y_test, y_pred_adjusted)
conf_matrix = confusion_matrix(y_test, y_pred_adjusted)

print(f"Best Parameters: {random_search.best_params_}")
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(class_report)
print("Confusion Matrix:")
print(conf_matrix)
# Crear el modelo XGBoost con los mejores parámetros encontrados
model_xgb_optimized = xgb.XGBClassifier(
    scale_pos_weight=70,
    n_estimators=400,
    max_depth=5,
    learning_rate=0.05,
    random_state=42  # Mantén el mismo random_state para reproducibilidad
)

# Entrenar el modelo con los datos de entrenamiento
model_xgb_optimized.fit(X_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = model_xgb_optimized.predict(X_test)

# Evaluar el rendimiento del modelo
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Mostrar los resultados
print("Accuracy:", accuracy)
print("Classification Report:\n", class_report)
print("Confusion Matrix:\n", conf_matrix)
# Crear el modelo XGBoost con los mejores parámetros encontrados
model_xgb_optimized = xgb.XGBClassifier(
    scale_pos_weight=70,
    n_estimators=400,
    max_depth=5,
    learning_rate=0.05,
    random_state=42  # Mantén el mismo random_state para reproducibilidad
)

# Entrenar el modelo con los datos de entrenamiento
model_xgb_optimized.fit(X_train, y_train)

# Hacer predicciones en el conjunto de prueba utilizando el umbral predeterminado de 0.5
y_pred = model_xgb_optimized.predict(X_test)

# Evaluar el rendimiento del modelo con el umbral predeterminado
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Mostrar los resultados con el umbral predeterminado
print("Accuracy with default threshold:", accuracy)
print("Classification Report with default threshold:\n", class_report)
print("Confusion Matrix with default threshold:\n", conf_matrix)
# Hacer predicciones en el conjunto de prueba utilizando el umbral predeterminado de 0.5
y_pred = model_xgb_optimized.predict(X_test)

# Evaluar el rendimiento del modelo con el umbral predeterminado
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Mostrar los resultados con el umbral predeterminado
print("Accuracy with default threshold:", accuracy)
print("Classification Report with default threshold:\n", class_report)
print("Confusion Matrix with default threshold:\n", conf_matrix)
#Comparativa con el modelo original:

#Si priorizamos maximizar el recall y puedes manejar un alto número de falsos positivos: El modelo sin ajustes es mejor.

#Si priorizamos reducir falsos positivos para no sobrecargar a los analistas, aunque eso signifique perder algunos verdaderos positivos: El modelo ajustado es la mejor opción.

#A nivel numerico:

#Resumen de Diferencias Numéricas

#Precisión: Aumentó en 0.01 (de 0.01 a 0.02).

#Recall: Disminuyó en 0.20 (de 0.74 a 0.54).

#F1-Score: Aumentó en 0.02 (de 0.01 a 0.03).

#True Negatives: Aumentaron en 71,519 (más instancias clasificadas correctamente como 0).

#False Positives: Disminuyeron en 71,519 (menos instancias clasificadas incorrectamente como 1).

#False Negatives: Aumentaron en 144 (más instancias clasificadas incorrectamente como 0).

#True Positives: Disminuyeron en 144 (menos instancias clasificadas correctamente como 1)

#Precisión Mejorada y Menos Falsos Positivos: El modelo ajustado mejora la precisión y reduce significativamente los falsos positivos, lo cual es beneficioso si los recursos para revisar estos casos son limitados.

#Compromiso en el Recall: Sin embargo, este modelo logra una menor detección de casos verdaderamente positivos (recall menor) y un aumento en los falsos negativos.

#Guardado del modelo

with open('model_xgb.pkl', 'wb') as file:
    pickle.dump(model_xgb_optimized, file)
#Test del XBGOOST sobre el HI_SMALL
#Modelo Xgboost normal

y_hi_pred = model_xgb.predict(X_hi)

# Evaluar el modelo
print("Accuracy on HI-Small:", accuracy_score(y_hi, y_hi_pred))
print("Classification Report on HI-Small:\n", classification_report(y_hi, y_hi_pred))

# Calcular la matriz de confusión
conf_matrix_hi = confusion_matrix(y_hi, y_hi_pred)

# Mostrar la matriz de confusión
print("Matriz de Confusión:\n", conf_matrix_hi)
#Test de xgboost con randomized --> Modelo modificado

# Predicciones con el mejor modelo ajustado sobre HI-Small
y_hi_pred = model_xgb_optimized.predict(X_hi)

# Evaluar el modelo ajustado en el conjunto completo HI-Small
print("Accuracy on HI-Small:", accuracy_score(y_hi, y_hi_pred))
print("Classification Report on HI-Small:\n", classification_report(y_hi, y_hi_pred))

# Calcular la matriz de confusión
conf_matrix_hi = confusion_matrix(y_hi, y_hi_pred)

# Mostrar la matriz de confusión
print("Matriz de Confusión:\n", conf_matrix_hi)
#El modelo está diseñado para apoyar a los analistas en la detección de lavado de dinero, y considerando la necesidad de no sobrecargar al equipo con demasiados falsos positivos, la opción más adecuada parece ser el XGBoost Modificado

#Resumen

#Modelo XGBoost Normal: Mejor si la prioridad es maximizar el recall y se pueden manejar grandes volúmenes de falsos positivos.

#Modelo XGBoost Modificado: Mejor si la prioridad es reducir falsos positivos, mejorar la precisión, y optimizar la eficiencia del equipo de analistas.texto en cursiva

# Suponiendo que X_hi y y_hi contienen el conjunto completo de datos HI-Small

# Calcular las probabilidades con el mejor modelo ajustado sobre HI-Small
y_hi_probs = model_xgb_optimized.predict_proba(X_hi)[:, 1]

# Ajustar el umbral de decisión a 0.25
threshold = 0.25
y_hi_pred_adjusted = (y_hi_probs >= threshold).astype(int)

# Evaluar el modelo ajustado en el conjunto completo HI-Small
print("Accuracy on HI-Small:", accuracy_score(y_hi, y_hi_pred_adjusted))
print("Classification Report on HI-Small:\n", classification_report(y_hi, y_hi_pred_adjusted))

# Calcular la matriz de confusión
conf_matrix_hi = confusion_matrix(y_hi, y_hi_pred_adjusted)

# Mostrar la matriz de confusión
print("Matriz de Confusión:\n", conf_matrix_hi)

#Prueba de que el modelo funciona correctamente
modelo_path = '/content/drive/MyDrive/Modelo 4 Septiembre/model_xgb_optimized.pkl'
with open(modelo_path, 'rb') as file:
    model = pickle.load(file)
X = hi_small.drop(columns=['Is Laundering'])

# Aplicar el modelo al dataset
predicciones = model.predict(X)

# Mostrar las predicciones
print(predicciones)
