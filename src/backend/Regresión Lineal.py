import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
from backend.data_manager import DataManager


# Función para limpiar los datos
def clean_data(data):
    """
    Limpia la tabla de datos, borrando cadenas no numéricas y remplazando valorea vacíons por Nan
    (Posible mejora: Reemplazar los valores no numéricos con equivalentes numéricos para que la regresión
    lineal tambien se pueda aplicar en ellos)
    """
    data = data.select_dtypes(include=['float64', 'int64'])     # Eliminar todas las columnas que no sean numéricas

    data = data.replace('', pd.NA)  # Convertir cadenas vacías en NaN
    
    data = data.dropna().infer_objects(copy=False) # Eliminar filas con valores faltantes

    columnas_numericas = data.columns.tolist()    # Obtener los nombres de las columnas que quedan después de la limpieza
    
    return data, columnas_numericas

def train_linear_model(data, feature_cols, target_col):
    """
    Entrena el modelo de regresión lineal, y devuelve el modelo entrenado, el error cuadrático medio (ECM)
    y el coeficiente de determinación (R**2)
    """
    data, columnas = clean_data(data)     # Limpiar los datos primero

    print(data.head())    # Mostrar las primeras 5 filas

    # Separar los datos en variables independientes (X) y dependientes (y)
    X = data[feature_cols]
    y = data[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)    # Dividir los datos en conjuntos de entrenamiento y prueba
    # 80% de los valores se usan para entrenar el modelo, y el 20% restantes para medir la eficacia del entrenamiento

    model = LinearRegression()    # Crea el modelo de regresión lineal

    model.fit(X_train, y_train)    # Entrenar el modelo

    y_pred = model.predict(X_test)    # Predecir los valores en el conjunto de prueba


    ecm = mean_squared_error(y_test, y_pred)    # Calcular el error  medio cuadrátic o(ECM)

    print(f"Mean Squared Error: {ecm}")

    r2 = model.score(X_test, y_test)    # Mostrar el coeficiente de determinación (R²)
    print(f"Coeficiente de determinación (R²): {r2}")
    
    return model, ecm, r2, columnas

def obtain_model_formula(trained_model:LinearRegression, columnas):
    # Extraer los coeficientes e intercepto
    coeficientes = trained_model.coef_
    intercepto = trained_model.intercept_

    # Generar la fórmula del modelo en texto
    formula = f"Salida = {intercepto:.2f}"
    for coef, columna in zip(coeficientes, columnas):
        formula += f" + ({coef:.2f} * {columna})"

    print("Fórmula del modelo:", formula)
    return formula

if __name__ == "__main__":
    # ejemplo
    tk.Tk().withdraw()  # Ocultar ventana principal de tkinter
    fn = askopenfilename()

    dm = DataManager()
    
    dm.read(fn)  # Cargar los datos en el DataFrame interno de DataManager
    
    # Definir la columna objetivo
    target_column = 'longitude'  

    if target_column not in dm.data.columns:
        raise ValueError(f"La columna objetivo '{target_column}' no existe en los datos.")

    # Seleccionar automáticamente las columnas numéricas, excluyendo la columna objetivo
    feature_columns = dm.data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    feature_columns.remove(target_column)  # Excluir la columna objetivo

    # Entrenar el modelo usando los datos de DataManager
    trained_model, ecm, r2, columnas = train_linear_model(dm.data, feature_columns, target_column)
    obtain_model_formula(trained_model, columnas)