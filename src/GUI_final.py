import sys
import io
import PySide6.QtWidgets as ps
from PySide6.QtGui import QPixmap  # Importa QPixmap para manejar imágenes
from data_manager import DataManager   # Importa el módulo data_manager correctamente
from modelo import entrenar_y_graficar_modelo
from resultados import ResultadosWidget  # Importa la clase de resultados
import matplotlib.pyplot as plt
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class MainWindow(ps.QMainWindow):
    def __init__(self):
        super().__init__()
        self._file_name = None
        self.initUI()
        self._manager = DataManager()
        self._metricas = [0, 0]
        self._formula = ""

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
        layout_h = ps.QHBoxLayout()
        # Botón para seleccionar archivo
        self.b1 = ps.QPushButton(text="Añadir archivos")
        self.b1.clicked.connect(self.add_file)
        layout_h.addWidget(self.b1)

        self.model_button = ps.QPushButton(text="Añadir modelo")
        self.model_button.clicked.connect(self.add_model)
        layout_h.addWidget(self.model_button)

        layout.addLayout(layout_h)

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


        #Etiqueta para mostrar la fórmula de regresión
        self.formula_label = ps.QLabel("Fórmula de Regresión: ")
        layout.addWidget(self.formula_label)
        self.formula_label.hide()
        #Etiquetas para mostrar R² y ECM
        self.r2_label = ps.QLabel("R²: ")
        self.ecm_label = ps.QLabel("ECM: ")
        self.ecm_label.hide()
        self.r2_label.hide()
        layout.addWidget(self.r2_label)
        layout.addWidget(self.ecm_label)
        
        #Configuración del widget central
        central_widget = ps.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        #Opciones de manejo de valores inexistentes
        missing_data_menu = ps.QHBoxLayout()

        self._missing_options = ps.QComboBox()
        self._missing_options.addItems(["Eliminar filas", "Rellenar con media", "Rellenar con mediana", "Rellenar con valor constante"])
        self._missing_options.currentIndexChanged.connect(self.missing_option_changed)
        
        self._missing_options.hide()  # Deshabilitado inicialmente

        missing_data_menu.addWidget(self._missing_options)

        self._constant_value_input = ps.QLineEdit()
        self._constant_value_input.setPlaceholderText("Introduce un valor")
        self._constant_value_input.hide()  #Escondido inicialmente, solo aparece si se selecciona "Rellenar con valor constante"
        missing_data_menu.addWidget(self._constant_value_input)

        self._apply_button = ps.QPushButton("Aplicar")
        self._apply_button.hide()  #Deshabilitado inicialmente
        self._apply_button.clicked.connect(self.apply_missing_data_strategy)
        missing_data_menu.addWidget(self._apply_button)

        layout.addLayout(missing_data_menu)

        
        self.setWindowTitle("Análisis de Regresión Lineal")
        self.statusBar = ps.QStatusBar()
        self.setStatusBar(self.statusBar)
        

        # Área de texto para la descripción del modelo
        self._description_edit = ps.QTextEdit()
        self._description_edit.setPlaceholderText("Escribe aquí la descripción del modelo (opcional)")
        self._description_edit.setStyleSheet("color: black")
        self._description_edit.hide()
        layout.addWidget(self._description_edit)
          # Botón para guardar el modelo (incluye descripción)
        self.save_button = ps.QPushButton("Guardar Modelo")
        self.save_button.clicked.connect(self.save_model)
        self.save_button.hide()
        layout.addWidget(self.save_button)
        

        # Layout principal
        layout = ps.QVBoxLayout()

    def add_model(self):
        self._file_name, _ = ps.QFileDialog.getOpenFileName(self, "Open Model", filter="Accepted Files (*joblib)")
        self._text_box.setText(self._file_name)
        
    
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

        entry_column, target_column =self._manager.depurate_nan(self, strategy, entry_column, target_column)

        self.show_data(self._manager.data)

        self.save_button.show()
        self._description_edit.show()

    def add_file(self):
        self._file_name, _ = ps.QFileDialog.getOpenFileName(self, "Open File", filter="Accepted Files (*.csv *.xlsx *.xls *.db *.sqlite)")
        self._text_box.setText(self._file_name)

    def data_reader(self):
        if self._file_name.endswith(".joblib"):
            try:
                self._modelo, self.model_description, self._metricas, self._formula = self._manager.load_model_with_description(self._file_name)
                
                self.b1.hide()
                self._table_widget.hide()

                self.formula_label.setText(f"Fórmula de Regresión: {self._formula}")
                self.r2_label.setText(f"R²: {self._metricas[0]:.4f}")
                self.ecm_label.setText(f"ECM: {self._metricas[1]:.4f}")
                self.r2_label.show()
                self.ecm_label.show()
                self.formula_label.show()

                ps.QMessageBox.information(self, "Éxito", "El archivo se ha cargado correctamente.")

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


        else:
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
            self._file_name = None
            self._table_widget.clear()

            self._entry_column.hide() 
            self._entry_column.clear()
            self._target_column.hide()
            self._target_column.clear()
            self._accept_button.hide()

            self._missing_options.hide()
            self._apply_button.hide()

            self.save_button.hide()
            self._description_edit.hide()

            self.r2_label.hide()
            self.ecm_label.hide()
            self.formula_label.hide()


    def set_dropdown_content(self, contents):
        self._entry_column.addItem("-- Columna de entrada --")
        self._entry_column.model().item(0).setEnabled(False)
        self._entry_column.addItems(contents) #Cambia el contenido de los dropdowns

        self._target_column.addItem("-- Columna de objetivo --")
        self._target_column.model().item(0).setEnabled(False)
        self._target_column.addItems(contents)

        #Hace los dropdows y el botón visibles
        self._entry_column.show()
        self._target_column.show()
        self._accept_button.show()

    def plot_regression(self, columnas_entrada, columna_salida):
        """Llama a la función `entrenar_y_graficar_modelo` y muestra los resultados en la interfaz."""
        try:
            # Eliminar gráfica anterior si existe
            if hasattr(self, 'graph_label'):
                self.graph_label.deleteLater()

            # Llamada a la función para entrenar el modelo y obtener la fórmula y métricas
            self._formula, self._metricas[0], self._metricas[1], self._modelo = entrenar_y_graficar_modelo(self._manager.data, columnas_entrada, columna_salida)

            # Actualiza las etiquetas con la fórmula y métricas
            self.formula_label.setText(f"Fórmula de Regresión: {self._formula}")
            self.r2_label.setText(f"R²: {self._metricas[0]:.4f}")
            self.ecm_label.setText(f"ECM: {self._metricas[1]:.4f}")
            self.r2_label.show()
            self.ecm_label.show()
            self.formula_label.show()

            # Genera la gráfica y conviértela en una imagen
            fig, ax = plt.subplots()
            ax.plot(self._manager.data[columnas_entrada], self._manager.data[columna_salida], label="Regresión")
            ax.set_xlabel(columnas_entrada[0])
            ax.set_ylabel(columna_salida)
            ax.legend()

            # Convertir la gráfica a un formato de imagen
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(buf.read())

            # Crear un QLabel para mostrar la gráfica
            self.graph_label = ps.QLabel(self)
            self.graph_label.setPixmap(pixmap)
            #self.graph_label.setAlignment(ps.QAlignmentFlag.AlignCenter)  # Centra la imagen en el QLabel

            # Mensaje de éxito
            ps.QMessageBox.information(self, "Éxito", "El modelo de regresión se ha creado correctamente.")
        
        except Exception as e:
            # Muestra un mensaje de error si algo falla
            ps.QMessageBox.critical(self, "Error", f"Ocurrió un error al crear el modelo: {str(e)}")

    def process_data(self):
        """Detecta los NaN e indica dónde, también controla que no se puedan acceder a ciertas 
        funcionalidades del programa si no son necesarias
        """
        if self._entry_column.currentIndex() == 0 or self._target_column.currentIndex() == 0:
            ps.QMessageBox.warning(self, "Error", "Selecciona valores válidos")
            return
        if self._entry_column.currentIndex() == self._target_column.currentIndex():
            ps.QMessageBox.warning(self, "Error", "La columnas no pueden ser la misma")
            return
        
        
        entry_column = self._entry_column.currentText() #Obtener los nombres de las columnas seleccionadas
        target_column = self._target_column.currentText()

        valid, message = self._manager.count_nan(entry_column, target_column)

        if not valid:
            self._missing_options.show()
            self._apply_button.show()
            ps.QMessageBox.warning(self, "Valores Inexistentes", message)
            return

        # Llama a plot_regression con las columnas seleccionadas
        columnas_entrada = [entry_column]
        columna_salida = target_column
        self.plot_regression(columnas_entrada, columna_salida)
            
         #Muestra el botón para guardar el modelo y el campo de descripción
        self.save_button.show()
        self._description_edit.show()


    def save_model(self):
        """Guarda el modelo junto con la descripción."""
        # Almacena la descripción del modelo
        self.model_description = self._description_edit.toPlainText()

        # Verifica si la descripción está vacía
        if not self.model_description:
            ps.QMessageBox.information(self, "Aviso", "La descripción está vacía, pero el modelo se guardará de todas formas.")
        
        file_path, _ = ps.QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "Accepted Files (*.joblib)")
        self._manager.save_model_with_description(self._modelo, self.model_description, self._metricas, self._formula, file_path)
        # Aquí podrías incluir la lógica para guardar el modelo y la descripción juntos
        print("Descripción del modelo:", self.model_description)
        ps.QMessageBox.information(self, "Éxito", "El modelo y la descripción se han guardado correctamente.")

if __name__ == "__main__":
    app = ps.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


