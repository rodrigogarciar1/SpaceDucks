import sqlite3 as sq
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename


class DataManager():
    def __init__(self) -> None:
        data = pd.DataFrame()

    def read(self):
        tk.Tk().withdraw()  # part of the import if you are not using other tkinter functions

        fn = askopenfilename()

        if fn.endswith('.xlsx'):
            self.read_xlsx(fn)

        elif fn.endswith('.csv'):
            self.read_csv(fn)

        elif fn.endswith('.db'):
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
        data = pd.read_csv(file)  # Carga todas las hojas
        print(f"Archivo '{file}' cargado exitosamente.")

        # Verifica si hay hojas en el archivo
        if data.empty:
            print("La tabla no existe o el archivo está vacío.")
            return

        # Si el archivo tiene múltiples hojas, selecciona la primera por defecto
        first_sheet_name = list(data.keys())[0]
        self.data = data[first_sheet_name]

        # Muestra las primeras filas del DataFrame
        print(f"Mostrando las primeras filas de la hoja: {first_sheet_name}")
        print(self.data)

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
