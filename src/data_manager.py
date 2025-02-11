import sqlite3 as sq
import pandas as pd
import PySide6.QtWidgets as ps
import joblib
from PySide6.QtCore import QAbstractTableModel, Qt

class PandasModel(QAbstractTableModel):
    def __init__(self, dataframe):
        super().__init__()
        self._dataframe = dataframe

    def rowCount(self, parent=None):
        return self._dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._dataframe.iat[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return section + 1  # Row numbers starting from 1
        return None
    


class DataManager():
    def __init__(self) -> None:
        self.data = pd.DataFrame()

    def read(self, fn:str):

        if fn.endswith('.xlsx') or fn.endswith('.xls'):
            self.read_xlsx(fn)

        elif fn.endswith('.csv'):
            self.read_csv(fn)

        elif fn.endswith('.db') or fn.endswith('.sqlite'):
            self.read_db(fn)

        elif fn.endswith('.joblib'):
            return self.load_model_with_description(fn)

        else:
            raise ValueError('The chosen file has an invalid extension.')

    def read_xlsx(self, file):
        try:
            data = pd.read_excel(file, sheet_name=None)  # Carga todas las hojas
        except:
            raise FileNotFoundError
        print(f"Archivo '{file}' cargado exitosamente.")

        # Verifica si hay hojas en el archivo
        if len(data)==0:
            print("La tabla no existe o el archivo está vacío.")
            return

        # Si el archivo tiene múltiples hojas, selecciona la primera por defecto
        first_sheet_name = list(data.keys())[0]
        self.data = data[first_sheet_name]

        # Muestra las primeras filas del DataFrame
        print(f"Mostrando las primeras filas de la hoja: {first_sheet_name}")
        print(self.data.head())

    def read_csv(self, file):
        try:
            self.data = pd.read_csv(file)  # Carga todas las hojas
        except:
            raise FileNotFoundError
        
        print(f"Archivo '{file}' cargado exitosamente.")

        # Verifica si hay hojas en el archivo
        if len(self.data)==0:
            print("La tabla no existe o el archivo está vacío.")
            return


        # Muestra las primeras filas del DataFrame
        print(f"Mostrando las primeras filas de la hoja:")
        print(self.data.head())

    def read_db(self, file):
        # Conexión a la base de datos SQLite
        try:
            conexion = sq.connect(f"file:{file}?mode=ro", uri=True)
        except:
            raise FileNotFoundError
        # Crear un cursor para ejecutar consultas SQL
        cursor = conexion.cursor()

        # Ejecutar una consulta (por ejemplo, para leer todas las tablas)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # Obtener los nombres de las tablas
        tablas = cursor.fetchall()
        print("Tablas en la base de datos:", tablas)

        # Suponiendo que queremos leer datos de una tabla en particular
        try:
            nombre_tabla = tablas[0][0]  # Selecciona la primera tabla encontrada
        except:
            raise IndexError
        print(f"Leyendo datos de la tabla: {nombre_tabla}")

        # Leer todos los datos de la tabla
        self.data = pd.read_sql_query(
            f"SELECT * FROM {nombre_tabla};", conexion)

        # Imprimir las filas obtenidas
        print(self.data.head())

        # Cerrar la conexión cuando termines
        conexion.close()

    def count_nan(self, entry_column, target_column):
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
            raise ValueError("No hay datos cargados para procesar.")  # Lanza una excepción en lugar de mostrar solo un mensaje.

        d = {entry_column: list(self.data[entry_column]), target_column: list(self.data[target_column])}
        column_data = pd.DataFrame(data=d)

        entry_nan_count = column_data[entry_column].isna().sum()
        target_nan_count = column_data[target_column].isna().sum()

        if entry_nan_count > 0 and target_nan_count > 0:
            choice, ok = ps.QInputDialog.getItem(
                gui,
                "Seleccionar columna",
                "Ambas columnas tienen valores inexistentes. ¿Cuál quieres procesar primero?",
                [entry_column, target_column],
                0,
                False
            )
            if not ok:  # Si el usuario cancela, se lanza una excepción
                raise RuntimeError("El usuario canceló la selección de columna para procesar NaN.")
            selected_column = choice
            other_column = target_column if selected_column == entry_column else entry_column
        elif entry_nan_count > 0:
            selected_column = entry_column
            other_column = None
        elif target_nan_count > 0:
            selected_column = target_column
            other_column = None
        else:
            ps.QMessageBox.information(gui, "Información", "No se encontraron valores inexistentes para procesar.")
            return column_data, entry_column, target_column

        # Aplica la depuración a las columnas
        self._depuration(gui, column_data, selected_column, strategy)
        if other_column:
            self._depuration(gui, column_data, other_column, strategy)

        return column_data, entry_column, target_column

    

    def _depuration(self, gui, column_data, column, strategy):
        if column is None or column_data[column].isna().sum() == 0:
            return

        try:
            if strategy == "Eliminar filas":
                column_data.dropna(subset=[column], inplace=True)
            elif strategy == "Rellenar con media":
                column_data[column] = column_data[column].fillna(column_data[column].mean())
            elif strategy == "Rellenar con mediana":
                column_data[column] = column_data[column].fillna(column_data[column].median())
            elif strategy == "Rellenar con valor constante":
                constant_value = gui._constant_value_input.text()
                if not constant_value.strip():
                    raise ValueError("El valor constante está vacío.")
                try:
                    constant_value = float(constant_value)
                except ValueError:
                    raise ValueError("El valor constante debe ser un número.")
                column_data[column] = column_data[column].fillna(constant_value)
            else:
                raise ValueError(f"Estrategia desconocida: {strategy}")

            ps.QMessageBox.information(gui, "Éxito", f"Se aplicó la estrategia '{strategy}' a la columna '{column}'.")
        except Exception as e:
            raise RuntimeError(f"Error al procesar la columna '{column}': {str(e)}")



    def save_model_with_description(self, model, description, metrics, formule, filename):
        """
        Save a model with a description using joblib.

        Parameters:
        - model: The trained model to save (e.g., a scikit-learn estimator).
        - description: A string describing the model (e.g., "RandomForest model trained on dataset X").
        - filename: The name of the file to save the model and description to, with .joblib extension.

        Returns:
        None
        """
        # Create a dictionary containing both the model and the description
        data_to_save = {
            'model': model,
            'description': description,
            'metrics': metrics,
            'formule': formule
        }
        
        # Save the dictionary to a joblib file
        joblib.dump(data_to_save, filename)
        print(f"Model and description saved to {filename}")

    def load_model_with_description(self, filename):
        try:
            loaded_data = joblib.load(filename)
        except:
            raise IndexError
        
        try:
            model = loaded_data['model']
            description = loaded_data['description']
            metrics = loaded_data['metrics']
            formule = loaded_data['formule']
        except:
            raise IndexError
        return model, description, metrics, formule

    def clear(self):
        self.data = pd.DataFrame()


