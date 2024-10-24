import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
# Función para limpiar los datos
def clean_data(data):
    # Eliminar todas las columnas no numéricas
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
    return model
if __name__ == "__main__":
    # ejemplo
    data = pd.DataFrame({
        'col1': [1.0, 2.0, 3.0, 4.0, 5.0],
        'col2': [2.5, 3.5, 4.5, 5.5, 6.5],
        'target': [1.1, 1.9, 3.0, 4.1, 4.9]
    })
    
    # Definir las columnas de características y la columna objetivo
    feature_columns = ['col1', 'col2']
    target_column = 'target'
    
    # Entrenar el modelo con los datos de ejemplo
    trained_model = train_linear_model(data, feature_columns, target_column)
