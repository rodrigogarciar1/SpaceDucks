from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

def entrenar_y_graficar_modelo(data, columnas_entrada, columna_salida):
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

    # Crear el gráfico si hay solo una columna de entrada
    if len(columnas_entrada) == 1:
        plt.figure(figsize=(10, 6))
        plt.scatter(X, y, color='blue', label='Datos Reales')
        plt.plot(X, y_pred, color='red', label='Recta de Ajuste')
        plt.title('Datos y Recta de Ajuste')
        plt.xlabel(columnas_entrada[0])
        plt.ylabel(columna_salida)
        plt.legend()
        plt.grid()
        plt.show()

    return formula, r2, ecm
