import sqlite3 as sq
import pandas as pd
from csv_reader import ProcesadorCSV
import PySide6.QtWidgets as ps
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class DataManager():
    def __init__(self) -> None:
        self.data = pd.DataFrame()

    def read(self, fn):

        if fn.endswith('.xlsx') or fn.endswith('.xls'):
            self.read_xlsx(fn)

        elif fn.endswith('.csv'):
            self.read_csv(fn)

        elif fn.endswith('.db') or fn.endswith('.sqlite'):
            self.read_db(fn)
        else:
            raise ValueError('The chosen file has an invalid extension.')

    def read_xlsx(self, file):
        data = pd.read_excel(file, sheet_name=None)  # Carga todas las hojas
        print(f"Archivo '{file}' cargado exitosamente.")

        # Verifica si hay hojas en el archivo
        if not data:
            print("La tabla no existe o el archivo está vacío.")
            return

        # Si el archivo tiene múltiples hojas, selecciona la primera por defecto
        first_sheet_name = list(data.keys())[0]
        self.data = data[first_sheet_name]

        # Muestra las primeras filas del DataFrame
        print(f"Mostrando las primeras filas de la hoja: {first_sheet_name}")
        print(self.data.head())

    def read_csv(self, file):
        a = open(file)
        csv_data = ProcesadorCSV(a.read())
        csv_data.procesar_csv()
        self.data = pd.DataFrame(
            csv_data.matriz_procesada[1:], columns=csv_data.matriz_procesada[0])

        # Muestra las primeras filas del DataFrame
        print(f"Mostrando las primeras filas de la hoja:")
        print(self.data.head())

        del csv_data

    def read_db(self, file):
        # Conexión a la base de datos SQLite
        conexion = sq.connect(file)

        # Crear un cursor para ejecutar consultas SQL
        cursor = conexion.cursor()

        # Ejecutar una consulta (por ejemplo, para leer todas las tablas)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # Obtener los nombres de las tablas
        tablas = cursor.fetchall()
        print("Tablas en la base de datos:", tablas)

        # Suponiendo que queremos leer datos de una tabla en particular
        nombre_tabla = tablas[0][0]  # Selecciona la primera tabla encontrada
        print(f"Leyendo datos de la tabla: {nombre_tabla}")

        # Leer todos los datos de la tabla
        self.data = pd.read_sql_query(
            f"SELECT * FROM {nombre_tabla};", conexion)

        # Imprimir las filas obtenidas
        print(self.data.head())

        # Cerrar la conexión cuando termines
        conexion.close()

    def foo(self, entry_column, target_column):
        entry_nan_count = self.data[entry_column].isna().sum() #Detectar valores inexistentes (NaN) en las columnas seleccionadas

        target_nan_count = self.data[target_column].isna().sum()

        message = ""  # Crear un mensaje para mostrar la información

        if entry_nan_count > 0:
            message += f"La columna de entrada '{entry_column}' tiene {entry_nan_count} valores inexistentes.\n"
        if target_nan_count > 0:
            message += f"La columna objetivo '{target_column}' tiene {target_nan_count} valores inexistentes.\n"

        # Si faltan datos mostrar advertencia al usuario
        if len(message) != 0:
            return False, message
        else:
            return True, message

    def depurate_nan(self, gui, strategy, entry_column, target_column):
        if self.data is None:
            ps.QMessageBox.warning(self, "Error", "No hay datos cargados para procesar.")
        
        d = {entry_column: list(self.data[entry_column]), target_column: list(self.data[target_column])}
        column_data = pd.DataFrame(data=d)
        
        print(column_data)
        entry_nan_count = column_data[entry_column].isna().sum()  # Contar NaN en la columna de entrada
        target_nan_count = column_data[target_column].isna().sum()  # Contar NaN en la columna objetivo

        # Verificar cuál columna tiene NaN y actuar en consecuencia
        if entry_nan_count > 0 and target_nan_count > 0:
            # Preguntar al usuario cuál columna quiere procesar primero
            choice, ok = ps.QInputDialog.getItem(
                gui,
                "Seleccionar columna",
                "Ambas columnas tienen valores inexistentes. ¿Cuál quieres procesar primero?",
                [entry_column, target_column],
                0,
                False)
            if ok and choice:  # Si el usuario selecciona una opción
                selected_column = choice
                other_column = target_column if selected_column == entry_column else entry_column
            else:
                return  # Si el usuario cancela, salir de la función
        elif entry_nan_count > 0:
            selected_column = entry_column
            other_column = None
        elif target_nan_count > 0:
            selected_column = target_column
            other_column = None

        

        self._depuration(gui, column_data, selected_column, strategy)
        self._depuration(gui, column_data, other_column, strategy)
    
        return column_data[entry_column], column_data[target_column]
    

    def _depuration(self, gui, column_data, column, strategy):
        try:
            if column is not None:
                    if column_data[column].isna().sum() > 0:
                        if strategy == "Eliminar filas":
                            column_data.dropna(subset=[column], inplace=True)
                        elif strategy == "Rellenar con media":
                            column_data[column] = column_data[column].fillna(column_data[column].mean())
                        elif strategy == "Rellenar con mediana":
                            column_data[column] = column_data[column].fillna(column_data[column].median())
                        elif strategy == "Rellenar con valor constante":
                            constant_value = self._constant_value_input.text()
                            if constant_value == "":
                                ps.QMessageBox.warning(gui, "Error", "Por favor, introduce un valor constante.")
                                return
                            try:
                                constant_value = float(constant_value)  # Intentar convertir a número
                            except ValueError:
                                ps.QMessageBox.warning(gui, "Error", "El valor constante debe ser un número.")
                                return
                            # Rellena NaN en la columna seleccionada con el valor constante
                            column_data[column] = column_data[column].fillna(constant_value)
                    ps.QMessageBox.information(gui, "Éxito", f"Se aplicó la estrategia '{strategy}' a la columna '{column}'.")
            else:
                pass
        except Exception as e:
            ps.QMessageBox.warning(gui, "Error", f"Ocurrió un error durante el preprocesado: {str(e)}")


    def plot_regression(self, entry_column, target_column):
        """Genera un gráfico de los datos y la recta de ajuste."""
        # Extraer los datos de entrada y salida
        X = entry_column[:].values.reshape(-1, 1)  # Convertir a formato 2D
        y = target_column[:].values

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

if __name__ == "__main__":
    dm = DataManager()
    dm.read()
