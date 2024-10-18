import sys
import PySide6.QtWidgets as ps
from data_manager import DataManager   # Importa el módulo data_manager correctamente

import sqlite3 as sq
import pandas as pd
from csv_reader import ProcesadorCSV

class DataManager():
    def __init__(self) -> None:
        self.data = pd.DataFrame()
        
    def read(self, fn):
        
        if fn is None:
            return None
        elif fn.endswith('.xlsx') or fn.endswith('.xls'):
            self.read_xlsx(fn)

        elif fn.endswith('.csv'):
            self.read_csv(fn)

        elif fn.endswith('.db') or fn.endswith('.sqlite'):
            self.read_db(fn)

    def read_xlsx(self, file):
        self.data = pd.read_excel(file, sheet_name=None)  # Carga todas las hojas
        print(f"Archivo '{file}' cargado exitosamente.")

        # Verifica si hay hojas en el archivo
        if not self.data:
            print("La tabla no existe o el archivo está vacío.")
            return

        # Si el archivo tiene múltiples hojas, selecciona la primera por defecto
        first_sheet_name = list(self.data.keys())[0]
        self.data = self.data[first_sheet_name]

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



class MainWindow(ps.QMainWindow):
    def __init__(self):
        super().__init__()
        self._file_name = None
        self.initUI()
        self.manager = DataManager()

    def initUI(self):
        self.setWindowTitle("File Viewer")
        self.setGeometry(100, 100, 900, 500)

        layout = ps.QVBoxLayout()

        # Botón para seleccionar archivo
        self.b1 = ps.QPushButton(text="Ver archivos")
        self.b1.clicked.connect(self.add_file)
        layout.addWidget(self.b1)

        # Botón para visualizar archivo
        self.b2 = ps.QPushButton(text="Visualizar archivo")
        self.b2.clicked.connect(self.data_reader)
        layout.addWidget(self.b2)

        # Botón para eliminar archivo
        self.b3 = ps.QPushButton(text="Eliminar archivo")
        self.b3.clicked.connect(self.clear_data)
        layout.addWidget(self.b3)

        # Label para mostrar el nombre del archivo seleccionado
        self._text_box = ps.QLabel("")
        self._text_box.setStyleSheet("background-color: gray; color: blue; max-height: 25px; max-width: 600px; padding: 5px")
        layout.addWidget(self._text_box)

        # QTextEdit para mostrar los datos del DataFrame
        self._text_edit = ps.QTextEdit()
        self._text_edit.setReadOnly(True)  # Hacerlo de solo lectura
        layout.addWidget(self._text_edit)

        central_widget = ps.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_file(self):
        self._file_name, _ = ps.QFileDialog.getOpenFileName(self, "Open File", filter="Accepted Files (*.csv *.xlsx *.xls *.db *.sqlite)")
        self._text_box.setText(self._file_name)

    def data_reader(self):
        if self._file_name:
            self.manager.read(self._file_name)  # Leer el archivo usando DataManager
            self.show_data(self.manager.data)  # Mostrar datos en QTextEdit
        else:
            print("No se ha seleccionado ningún archivo.")
            ps.QMessageBox.warning(self, "Error", "Por favor, selecciona un archivo primero.")

    def show_data(self, data):
        """Muestra el DataFrame en el QTextEdit."""
        if not data.empty:
            self._text_edit.clear()  # Limpiar el QTextEdit
            self._text_edit.setPlainText(data.to_string(index=False))  # Mostrar el DataFrame como texto
        else:
            self._text_edit.setPlainText("No hay datos para mostrar.")

    #eliminar las cosas de la caja de texto aunque no lo quita del todo tecnicamente, todavia lo tiene en memoria
    def clear_data(self):
        if not self._file_name:
            print("No hay archivo seleccionado.")
        else:

            self._text_box.clear()
            self._text_edit.clear()
            self._file_name == None

if __name__ == "__main__":
    app = ps.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()