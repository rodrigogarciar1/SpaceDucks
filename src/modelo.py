import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def entrenar_modelo(df, columnas_entrada, columna_salida):
    X = df[columnas_entrada]
    y = df[columna_salida]

    modelo = LinearRegression()
    modelo.fit(X, y)

    # Coeficientes y fórmula
    coeficientes = modelo.coef_
    intercepto = modelo.intercept_
    formula = f"{columna_salida} = " + " + ".join([f"{coef:.2f} * {col}" for coef, col in zip(coeficientes, columnas_entrada)]) + f" + {intercepto:.2f}"

    # Predicciones y métricas
    y_pred = modelo.predict(X)
    r2 = r2_score(y, y_pred)
    ecm = mean_squared_error(y, y_pred)
    print(formula)
    print(r2)
    print(ecm)

    return formula, r2, ecm


def plot_regression(df, entry_column, target_column):
        """Genera un gráfico de los datos y la recta de ajuste."""
        # Extraer los datos de entrada y salida
        X = df[entry_column][:].values.reshape(-1, 1)  # Convertir a formato 2D
        y = df[target_column][:].values

        # Crear el modelo de regresión lineal y ajustarlo a los datos
        model = LinearRegression()
        model.fit(X, y)

        # Predecir valores
        y_pred = model.predict(X)

        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.scatter(X, y, color='blue', label='Datos Reales')  # Puntos de datos
        plt.plot(X, y_pred, color='red', label='Recta de Ajuste')  # Recta de ajuste
        plt.title('Datos y Recta de Ajuste')
        plt.xlabel(entry_column)
        plt.ylabel(target_column)
        plt.legend()
        plt.grid()
        plt.show()


