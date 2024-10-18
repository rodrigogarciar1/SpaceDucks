import sqlite3 as sq
import pandas as pd
from csv_reader import ProcesadorCSV


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
        print(self._data.head())

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


if __name__ == "__main__":
    dm = DataManager()
    dm.read()
