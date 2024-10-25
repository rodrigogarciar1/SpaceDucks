import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
from data_manager import DataManager


# Función para limpiar los datos
def clean_data(data):
    # Eliminar todas las columnas que no sean numéricas
    data = data.select_dtypes(include=['float64', 'int64'])

    # Rellenar o eliminar valores faltantes
    data = data.replace('', pd.NA)  # Convertir cadenas vacías en NaN
    
    # Eliminar filas con valores faltantes
    data = data.dropna().infer_objects(copy=False)
    
    return data

# Función para entrenar un modelo de regresión lineal
def train_linear_model(data, feature_cols, target_col):
    # Limpiar los datos primero
    data = clean_data(data)

    # Mostrar las primeras 5 filas
    print(data.head())

    # Separar los datos en variables independientes (X) y dependientes (y)
    X = data[feature_cols]
    y = data[target_col]

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear el modelo de regresión lineal
    model = LinearRegression()

    # Entrenar el modelo
    model.fit(X_train, y_train)

    # Predecir los valores en el conjunto de prueba
    y_pred = model.predict(X_test)

    # Calcular el error cuadrático medio (MSE)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # Mostrar el coeficiente de determinación (R²)
    r2 = model.score(X_test, y_test)
    print(f"Coeficiente de determinación (R²): {r2}")
    
    # Devolver el modelo ya entrenado, haciendo model.predict ya obtienes las predicciones
    return model, mse, r2
if __name__ == "__main__":
    # ejemplo
    tk.Tk().withdraw()  # Ocultar ventana principal de tkinter
    fn = askopenfilename()

    # Crear una instancia de DataManager
    dm = DataManager()
    
    # Leer los datos desde un archivo
    dm.read(fn)  # Cargar los datos en el DataFrame interno de DataManager
    
    # Definir la columna objetivo
    target_column = 'longitude'  # Cambia al nombre de tu columna objetivo

    # Verificar que la columna objetivo exista en los datos
    if target_column not in dm.data.columns:
        raise ValueError(f"La columna objetivo '{target_column}' no existe en los datos.")

    # Seleccionar automáticamente las columnas numéricas, excluyendo la columna objetivo
    feature_columns = dm.data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    feature_columns.remove(target_column)  # Excluir la columna objetivo

    # Entrenar el modelo usando los datos de DataManager
    trained_model, mse, r2 = train_linear_model(dm.data, feature_columns, target_column)