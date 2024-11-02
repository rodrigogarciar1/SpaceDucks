import sys
import PySide6.QtWidgets as ps
from PySide6.QtGui import QPixmap  # Importa QPixmap para manejar imágenes
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
        
        # Estilo general
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0e68c; /* Amarillo pastel */
                font-family: 'Courier New'; /* Fuente retro */
            }
            QLabel {
                font-size: 20px;
                color: #2f4f4f; /* Verde oscuro */
                padding: 10px;
                border: 2px solid #8b4513; /* Marrón */
                border-radius: 10px; /* Bordes redondeados */
                background-color: #fff8dc; /* Fondo color crema */
            }
            QPushButton {
                background-color: #8b0000; /* Rojo oscuro */
                color: #ffffff; /* Texto blanco */
                font-size: 18px;
                padding: 10px;
                border: 2px solid #ff6347; /* Tomate */
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff6347; /* Tomate más brillante */
                border-color: #ffffff; /* Cambio de color del borde */
            }
            QTextEdit {
                border: 2px solid #cd853f; /* Marrón claro */
                border-radius: 5px;
                background-color: #fffaf0; /* Fondo blanco antiguo */
                font-family: 'Courier New'; /* Fuente retro */
            }
        """)

        # Botón para seleccionar archivo
        self.b1 = ps.QPushButton(text="Añadir archivos")
        self.b1.clicked.connect(self.add_file)
        layout.addWidget(self.b1)

        # Botón para visualizar archivo
        self.b2 = ps.QPushButton(text="Visualizar archivo")
        self.b2.clicked.connect(self.data_reader)
        layout.addWidget(self.b2)

        layout_h = ps.QHBoxLayout()
        
        # Label para mostrar el nombre del archivo seleccionado
        self._text_box = ps.QLabel("")
        self._text_box.setStyleSheet("background-color: white; color: blue; max-height: 25px; max-width: 900px; padding: 5px")
        layout_h.addWidget(self._text_box)

        # Botón para eliminar archivo
        self.b3 = ps.QPushButton(text="Eliminar archivo")
        self.b3.clicked.connect(self.clear_data)
        layout_h.addWidget(self.b3)
        layout.addLayout(layout_h)

        # Tabla para mostrar los datos del DataFrame
        self._table_widget = ps.QTableWidget()
        layout.addWidget(self._table_widget)

        # Dropdown para la selección de la columna de datos
        self._entry_column = ps.QComboBox()
        self._entry_column.hide()  # Ocultar inicialmente
        linear_menu.addWidget(self._entry_column)

        # Dropdown para la selección de la columna objetivo
        self._target_column = ps.QComboBox()
        self._target_column.hide()

        # Área de texto para la descripción del modelo
        self._description_edit = ps.QTextEdit()
        self._description_edit.setPlaceholderText("Escribe aquí la descripción del modelo (opcional)")
        layout.addWidget(self._description_edit)

        # Botón para guardar el modelo (incluye descripción)
        self.save_button = ps.QPushButton("Guardar Modelo")
        self.save_button.clicked.connect(self.save_model)
        layout.addWidget(self.save_button)

        central_widget = ps.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_file(self):
        # Método para seleccionar un archivo y guardar su nombre
        self._file_name, _ = ps.QFileDialog.getOpenFileName(self, "Open File", filter="Accepted Files (*.csv *.xlsx *.xls *.db *.sqlite)")
        if self._file_name:
            self._text_box.setText(f"Archivo seleccionado: {self._file_name}")

    def data_reader(self):
        """Función para leer y mostrar los datos."""
        try:
            if self._file_name:
                self._manager.read(self._file_name)  # Leer el archivo usando DataManager

                if self._manager.data.empty:
                    ps.QMessageBox.warning(self, "Error", "El archivo está vacío o no tiene datos.")
                    self.clear_data()
                    return
            
                self.show_data(self._manager.data)  # Mostrar datos en la tabla
                self._table_widget.show()
            else:
                ps.QMessageBox.warning(self, "Error", "Por favor, selecciona un archivo primero.")
        except Exception as e:
            ps.QMessageBox.warning(self, "Error", f"Error inesperado: {str(e)}")

    def show_data(self, data):
        """Muestra los datos en el QTableWidget."""
        self._table_widget.setRowCount(data.shape[0])
        self._table_widget.setColumnCount(data.shape[1])
        self._table_widget.setHorizontalHeaderLabels(data.columns)

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                item = ps.QTableWidgetItem(str(data.iat[i, j]))
                self._table_widget.setItem(i, j, item)

    def clear_data(self):
        """Limpia los datos y la descripción."""
        self._text_box.clear()
        self._description_edit.clear()
        self._file_name = None
        self._table_widget.clear()
        self._table_widget.hide()

    def save_model(self):
        """Guarda el modelo junto con la descripción."""
        # Almacena la descripción del modelo
        self.model_description = self._description_edit.toPlainText()

        # Verifica si la descripción está vacía
        if not self.model_description:
            ps.QMessageBox.information(self, "Aviso", "La descripción está vacía, pero el modelo se guardará de todas formas.")
        else:
            ps.QMessageBox.information(self, "Éxito", "El modelo y la descripción se han guardado correctamente.")

        # Aquí podrías incluir la lógica para guardar el modelo y la descripción juntos
        print("Descripción del modelo:", self.model_description)

if __name__ == "__main__":
    app = ps.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


