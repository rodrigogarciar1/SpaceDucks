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
        self._text_box.setStyleSheet("background-color: gray; color: blue; max-height: 25px; max-width: 600px; padding: 5px")
        layout_h.addWidget(self._text_box)
        # Botón para eliminar archivo
        self.b3 = ps.QPushButton(text="Eliminar archivo")
        self.b3.clicked.connect(self.clear_data)
        layout_h.addWidget(self.b3)
        layout.addLayout(layout_h)


        linear_menu = ps.QHBoxLayout() #Hace un layout horizontal 

        #Dropdown para la selección de la columna de datos
        self._entry_column = ps.QComboBox() 
        self._entry_column.setStyleSheet("display = inline-box")
        self._entry_column.hide() #La esconde de la vista para evitar acciones indevidas
        linear_menu.addWidget(self._entry_column)

        #Dropdown para la selección de la columa objetivo
        self._target_column = ps.QComboBox()
        self._target_column.setStyleSheet("display = inline-box")
        self._target_column.hide()
        linear_menu.addWidget(self._target_column)

        #Botón para procesar el modelo de regresión lineal
        self._accept_button = ps.QPushButton(text="Procesar")
        self._accept_button.setStyleSheet("display = inline-box")
        self._accept_button.hide()
        self._accept_button.clicked.connect(self.process_data)
        linear_menu.addWidget(self._accept_button)

        layout.addLayout(linear_menu)
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
        try: #gestion de errores
            if self._file_name:
                self._manager.read(self._file_name)  # Leer el archivo usando DataManager

            # Verificar si el DataFrame está vacío
                if self._manager.data.empty:
                    ps.QMessageBox.warning(self, "Error", "El archivo está vacío o no tiene datos.")
                    self.clear_data()  # Limpiar datos en caso de archivo vacío
                    return
            
                self.show_data(self._manager.data)  # Mostrar datos en QTextEdit
                self.set_dropdown_content(self._manager.data.keys())
            else:
                print("No se ha seleccionado ningún archivo.")
                ps.QMessageBox.warning(self, "Error", "Por favor, selecciona un archivo primero.")
        except IndexError:
            ps.QMessageBox.warning(self, "Error", "Archivo vacío o sin datos.")
        except FileNotFoundError:
            ps.QMessageBox.warning(self, "Error", "No se encontró el archivo.")
        except PermissionError:
            ps.QMessageBox.warning(self, "Error", "No tienes permiso para abrir este archivo.")
        except ValueError:
            ps.QMessageBox.warning(self, "Error", "Error en el formato del archivo.")
        except UnicodeDecodeError:
            ps.QMessageBox.warning(self, "Error", "Error de codificación al leer el archivo.")
        except MemoryError:
            ps.QMessageBox.warning(self, "Error", "El archivo es demasiado grande para ser cargado en memoria.")
        except Exception as e:
            ps.QMessageBox.warning(self, "Error", f"Error inesperado: {str(e)}")         

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
            self._file_name = None

            self._entry_column.hide() 
            self._entry_column.clear()
            self._target_column.hide()
            self._target_column.clear()
            self._accept_button.hide()

    def set_dropdown_content(self, contents):
        self._entry_column.addItems(contents) #Cambia el contenido de los dropdowns
        self._target_column.addItems(contents)

        #Hace los dropdows y el botón visibles
        self._entry_column.show()
        self._target_column.show()
        self._accept_button.show()

    def process_data(self):
        if self._entry_column.currentIndex() == self._target_column.currentIndex():
            ps.QMessageBox.warning(self, "Error", "La columnas no pueden ser la misma")
        if (self._entry_column.currentIndex() or self._target_column.currentIndex()) == -1:
            ps.QMessageBox.warning(self, "Error", "Selecciona valores válidos")

if __name__ == "__main__":
    app = ps.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()