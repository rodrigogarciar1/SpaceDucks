import sys
import PySide6.QtWidgets as ps
from data_manager import DataManager   # Importa el módulo data_manager correctamente

class MainWindow(ps.QMainWindow):
    def __init__(self):
        super().__init__()
        self._file_name = None
        self.initUI()
        self._manager = DataManager()

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
            self._manager.read(self._file_name)  # Leer el archivo usando DataManager
            self.show_data(self._manager.data)  # Mostrar datos en QTextEdit
        else:
            print("No se ha seleccionado ningún archivo.")
            ps.QMessageBox.warning(self, "Error", "Por favor, selecciona un archivo primero.")

    def show_data(self, data):
        """Muestra el DataFrame en el QTextEdit."""
        if len(data) != 0:
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