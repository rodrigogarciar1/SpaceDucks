import sys
import PySide6.QtWidgets as ps
from PySide6.QtGui import QPixmap  # Importa QPixmap para manejar imágenes
from backend.data_manager import DataManager   # Importa el módulo data_manager correctamente
import numpy as np
import pandas as pd
from backend.modelo import entrenar_modelo  # Importa la función del módulo
from backend.resultados import ResultadosWidget  # Importa la clase de resultados


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

        linear_menu = ps.QHBoxLayout() #Hace un layout horizontal 

        # Dropdown para la selección de la columna de datos
        self._entry_column = ps.QComboBox()
        self._entry_column.hide()  # Ocultar inicialmente
        linear_menu.addWidget(self._entry_column)

        # Dropdown para la selección de la columna objetivo
        self._target_column = ps.QComboBox()
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

        # Opciones de manejo de valores inexistentes
        missing_data_menu = ps.QHBoxLayout()

        self._missing_options = ps.QComboBox()
        self._missing_options.addItems(["Eliminar filas", "Rellenar con media", "Rellenar con mediana", "Rellenar con valor constante"])
        self._missing_options.currentIndexChanged.connect(self.missing_option_changed)
        
        self._missing_options.setEnabled(False)  # Deshabilitado inicialmente

        missing_data_menu.addWidget(self._missing_options)

        self._constant_value_input = ps.QLineEdit()
        self._constant_value_input.setPlaceholderText("Introduce un valor")
        self._constant_value_input.hide()  #Escondido inicialmente, solo aparece si se selecciona "Rellenar con valor constante"
        missing_data_menu.addWidget(self._constant_value_input)

        self._apply_button = ps.QPushButton("Aplicar")
        self._apply_button.setEnabled(False)  #Deshabilitado inicialmente
        self._apply_button.clicked.connect(self.apply_missing_data_strategy)
        missing_data_menu.addWidget(self._apply_button)

        layout.addLayout(missing_data_menu)

        central_widget = ps.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Análisis de Regresión Lineal")
        self.statusBar = ps.QStatusBar()
        self.setStatusBar(self.statusBar)
        # Inicializa tu DataFrame df
        self.df = pd.DataFrame()  # Carga tu DataFrame aquí
        self.columnas_entrada = []  # Inicializa las columnas de entrada
        self.columna_salida = "salida"  # Define tu columna de salida

        # Crea un botón para confirmar el preprocesado
        self.boton_confirmar = ps.QPushButton("Confirmar Preprocesado")
        self.boton_confirmar.clicked.connect(self.confirmar_preprocesado)

        # Layout principal
        layout = ps.QVBoxLayout()
        layout.addWidget(self.boton_confirmar)

     

    def confirmar_preprocesado(self):
        if not self.columnas_entrada:
            ps.QMessageBox.warning(self, "Error", "No se han seleccionado columnas de entrada.")
            return

        try:
            # Llama a la función para entrenar el modelo
            formula, r2, ecm = entrenar_modelo(self.df, self.columnas_entrada, self.columna_salida)

            # Muestra los resultados en una nueva ventana
            resultados_widget = ResultadosWidget(formula, r2, ecm)
            resultados_widget.show()

        except Exception as e:
            ps.critical(self, "Error", f"Ocurrió un error: {str(e)}")

    def missing_option_changed(self):
        """Mostrar u ocultar la entrada para valor constante dependiendo de la opción seleccionada."""
        if self._missing_options.currentText() == "Rellenar con valor constante":
            self._constant_value_input.show()
        else:
            self._constant_value_input.hide()


            

    def apply_missing_data_strategy(self):
        """Aplica la estrategia seleccionada para manejar los valores inexistentes."""
        strategy = self._missing_options.currentText()
        entry_column = self._entry_column.currentText()  # Obtener los nombres de las columnas seleccionadas
        target_column = self._target_column.currentText()

        self._manager.depurate_nan(self, strategy, entry_column, target_column)

        self.show_data(self._manager.data)




    def add_file(self):
        self._file_name, _ = ps.QFileDialog.getOpenFileName(self, "Open File", filter="Accepted Files (*.csv *.xlsx *.xls *.db *.sqlite)")
        self._text_box.setText(self._file_name)

    def data_reader(self):
        try: #Gestión de errores
            if self._file_name:
                self._manager.read(self._file_name)  #Leer el archivo usando DataManager

            #Verificar si el DataFrame está vacío
                if self._manager.data.empty:
                    ps.QMessageBox.warning(self, "Error", "El archivo está vacío o no tiene datos.")
                    self.clear_data()  #Limpiar datos en caso de archivo vacío
                    return
            
                self.show_data(self._manager.data)  #Mostrar datos en QTextEdit
                self.set_dropdown_content(self._manager.data.keys())
                self._table_widget.show()  # Asegúrate de mostrar la tabla aquí

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
        """Muestra los datos en el QTableWidget."""
        self._table_widget.setRowCount(data.shape[0])
        self._table_widget.setColumnCount(data.shape[1])
        self._table_widget.setHorizontalHeaderLabels(data.columns)

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                item = ps.QTableWidgetItem(str(data.iat[i, j]))
                self._table_widget.setItem(i, j, item)
    

    #eliminar las cosas de la caja de texto aunque no lo quita del todo tecnicamente, todavia lo tiene en memoria
    def clear_data(self):
        if not self._file_name:
            print("No hay archivo seleccionado.")
        else:

            self._text_box.clear()
            self._text_edit.clear()
            self._file_name = None
            self._table_widget.clear()
            self._table_widget.hide()
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
        """Detecta los NaN e indica dónde, también controla que no se puedan acceder a ciertas 
        funcionalidades del programa si no son necesarias
        """
        if self._entry_column.currentIndex() == self._target_column.currentIndex():
            ps.QMessageBox.warning(self, "Error", "La columnas no pueden ser la misma")
        if (self._entry_column.currentIndex() or self._target_column.currentIndex()) == -1:
            ps.QMessageBox.warning(self, "Error", "Selecciona valores válidos")

        
        entry_column = self._entry_column.currentText() #Obtener los nombres de las columnas seleccionadas
        target_column = self._target_column.currentText()

        valid, message = self._manager.foo(entry_column, target_column)

        self._missing_options.setEnabled(not valid)
        self._apply_button.setEnabled(not valid)

        print(valid)

        if valid is True:
            # Llama al método de graficar después de validar
            self._manager.plot_regression(entry_column, target_column)
        else:
            ps.QMessageBox.warning(self, "Valores Inexistentes", message)
        
if __name__ == "__main__":
    app = ps.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()