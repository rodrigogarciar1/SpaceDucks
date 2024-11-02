import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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

    return formula, r2, ecm
