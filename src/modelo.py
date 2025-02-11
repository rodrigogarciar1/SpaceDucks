from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

def entrenar_modelo(data, columnas_entrada, columna_salida):
    """
    Entrena el modelo de regresión lineal, calcula métricas y muestra el gráfico de ajuste.
    
    Argumentos:
    - data: DataFrame que contiene los datos.
    - columnas_entrada: lista de nombres de columnas de entrada.
    - columna_salida: nombre de la columna de salida.
    """
    # Extraer los datos de entrada y salida
    X = data[columnas_entrada].values  # Convertir a formato 2D si es necesario
    y = data[columna_salida].values

    # Crear el modelo de regresión lineal y ajustarlo a los datos
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Obtener los coeficientes y la fórmula de la regresión
    coeficientes = modelo.coef_
    intercepto = modelo.intercept_
    formula = f"{columna_salida} = " + " + ".join([f"{coef:.2f} * {col}" for coef, col in zip(coeficientes, columnas_entrada)]) + f" + {intercepto:.2f}"

    # Predicciones y métricas
    y_pred = modelo.predict(X)
    r2 = r2_score(y, y_pred)
    ecm = mean_squared_error(y, y_pred)
    
    # Imprimir la fórmula y las métricas
    print(formula)
    print(f"Coeficiente de determinación (R²): {r2}")
    print(f"Error Cuadrático Medio (ECM): {ecm}")

    return formula, r2, ecm, modelo, y_pred

def hacer_predicciones(modelo, nro_a_predecir:int):
    """Realiza una predicción de un valor dado teniendo un modelo entrenado"""
    try:
        if modelo is None:
            raise ValueError("El modelo no está entrenado.")
        
        input_data = [[nro_a_predecir]]

        # Hacer la predicción
        prediction = modelo.predict(input_data)
        
        # Retornar la predicción
        return prediction[0]
    
    except Exception as e:
        return str(e)