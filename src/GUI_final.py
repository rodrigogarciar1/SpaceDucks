import sys
import PySide6.QtWidgets as ps
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from data_manager import DataManager   # Importa el módulo data_manager correctamente
from modelo import entrenar_modelo
import pyqtgraph as pg

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
    

class MainWindow(ps.QMainWindow):
    def __init__(self):
        super().__init__()
        self._file_name = ""
        self.initUI()
        self._manager = DataManager()
        self._metricas = [0, 0]
        self._formula = ""

    def button(self, button_text, function, hidden = False):
        button = ps.QPushButton(text = button_text)
        button.clicked.connect(function)
        if hidden:
            button.hide()
        return button

    def add_to_layout(self, layout, *args):
        if len(args) == 0:
            return ValueError("There must be at least one object to add to the layout")
        
        for element in args:
            if type(element) not in [ps.QVBoxLayout, ps.QHBoxLayout]:
                layout.addWidget(element)
            else:
                layout.addLayout(element)
        return layout

    def initUI(self):
        self.setWindowTitle("Análisis de Regresión Lineal")
        self.setGeometry(100, 100, 900, 500)  # Set initial window size

        # Create a main scroll area that covers the entire window
        main_scroll_area = ps.QScrollArea()
        main_scroll_area.setWidgetResizable(True)
        #main_scroll_area.setStyleSheet(" background-color: #f0e68c; /* Amarillo pastel */ font-family: 'Courier New'; /* Fuente retro */")

        # Create a central widget to hold all content
        central_widget = ps.QWidget()
        layout = ps.QVBoxLayout(central_widget)
            # Estilo general
        
        layout_h1 = ps.QHBoxLayout()
        # Botón para seleccionar archivo
        self.b1 = self.button("Añadir archivos", self.add_file)
        self.model_button = self.button("Añadir modelo", self.add_model)
        
        self.add_to_layout(layout_h1, self.b1, self.model_button)
        
        layout.addLayout(layout_h1)

        # Botón para visualizar archivo
        self.b2 = self.button("Visualizar archivo", self.data_reader)

        layout.addWidget(self.b2)

        layout_h = ps.QHBoxLayout()
        
        # Label para mostrar el nombre del archivo seleccionado
        self._text_box = ps.QLabel("")
        self._text_box.setStyleSheet("background-color: white; color: blue; max-height: 25px; max-width: 900px; padding: 5px")

        # Botón para eliminar archivo
        self.b3 = self.button("Eliminar archivo", self.clear_data)

        self.add_to_layout(layout_h, self._text_box, self.b3)

        layout.addLayout(layout_h)

            # Tabla para mostrar los datos del DataFrame
        self._table_widget = ps.QTableView()
        layout.addWidget(self._table_widget)

        linear_menu = ps.QHBoxLayout() #Hace un layout horizontal 

        # Dropdown para la selección de la columna de datos
        self._entry_column = ps.QComboBox()
        self._entry_column.hide()  # Ocultar inicialmente

        # Dropdown para la selección de la columna objetivo
        self._target_column = ps.QComboBox()
        self._target_column.hide()

        #Botón para procesar el modelo de regresión lineal
        self._accept_button = self.button("Procesar", self.process_data, hidden=True)
        self._accept_button.setStyleSheet("display = inline-box")
        
        self.add_to_layout(linear_menu, self._entry_column, self._target_column, self._accept_button)

        layout.addLayout(linear_menu)
        
        #Opciones de manejo de valores inexistentes
        missing_data_menu = ps.QHBoxLayout()

        self._missing_options = ps.QComboBox()
        self._missing_options.addItems(["Eliminar filas", "Rellenar con media", "Rellenar con mediana", "Rellenar con valor constante"])
        self._missing_options.currentIndexChanged.connect(self.missing_option_changed)
        self._missing_options.hide()  # Deshabilitado inicialmente

        self._constant_value_input = ps.QLineEdit()
        self._constant_value_input.setPlaceholderText("Introduce un valor")
        self._constant_value_input.hide()  #Escondido inicialmente, solo aparece si se selecciona "Rellenar con valor constante"

        self._apply_button = self.button("Aplicar", self.apply_missing_data_strategy, hidden=True)

        self.add_to_layout(missing_data_menu, self._missing_options, self._constant_value_input, self._apply_button)

        layout.addLayout(missing_data_menu)

        self._graph = pg.PlotWidget()
        self._graph.setStyleSheet("min-height:400px")
        self._graph.hide()

        #Etiqueta para mostrar la fórmula de regresión
        self.formula_label = ps.QLabel("Fórmula de Regresión: ")
        self.formula_label.hide()

        #Etiquetas para mostrar R² y ECM
        self.r2_label = ps.QLabel("R²: ")
        self.ecm_label = ps.QLabel("ECM: ")
        self.ecm_label.hide()
        self.r2_label.hide()
        
        self.setWindowTitle("Análisis de Regresión Lineal")
        self.statusBar = ps.QStatusBar()
        self.setStatusBar(self.statusBar)
        

        # Área de texto para la descripción del modelo
        self._description_edit = ps.QTextEdit()
        self._description_edit.setPlaceholderText("Escribe aquí la descripción del modelo (opcional)")
        self._description_edit.setStyleSheet("color: black")
        self._description_edit.hide()
          # Botón para guardar el modelo (incluye descripción)
    
        self.save_button = self.button("Guardar Modelo", self.save_model, hidden=True)

         
        self.add_to_layout(layout, self._graph, self.formula_label, self.r2_label, self.ecm_label, self._description_edit, self.save_button)
        # Layout principal
        layout = ps.QVBoxLayout()

        # Set the central widget as the scroll area's widget
        main_scroll_area.setWidget(central_widget)

        # Set the scroll area as the central widget of the main window
        self.setCentralWidget(main_scroll_area)

    def add_model(self):
        self.b2.show()
        self.b1.hide()
        file_name, _ = ps.QFileDialog.getOpenFileName(self, "Open Model", filter="Accepted Files (*joblib)")
        if len(file_name)>0:
            self._file_name = file_name
        else:
            return
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

        data, entry_column, target_column =self._manager.depurate_nan(self, strategy, entry_column, target_column)

        self.plot_regression(entry_column, target_column, data)

        self.save_button.show()
        self._description_edit.show()
        

    def add_file(self):
        self.b2.show()
        self._graph.hide()
        file_name, _ = ps.QFileDialog.getOpenFileName(self, "Open File", filter="Accepted Files (*.csv *.xlsx *.xls *.db *.sqlite)")
        if len(file_name)>0:
            self._file_name = file_name
        else:
            return
        self._text_box.setText(self._file_name)

    def data_reader(self):
        if self._file_name.endswith(".joblib"):
            try:
                self._modelo, description, self._metricas, self._formula = self._manager.load_model_with_description(self._file_name)
                fn = self._file_name
                self.clear_data()
                self._table_widget.hide()

                self._text_box.setText(fn)
                self.formula_label.setText(f"Fórmula de Regresión: {self._formula}")
                self.r2_label.setText(f"R²: {self._metricas[0]:.4f}")
                self.ecm_label.setText(f"ECM: {self._metricas[1]:.4f}")
                self.r2_label.show()
                self.ecm_label.show()
                self.formula_label.show()
                self._description_edit.setText(description)
                self._description_edit.show()
                self.b2.hide()
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
                
                    self._table_widget.setModel(PandasModel(self._manager.data))  #Mostrar datos en QTextEdit
                    self.set_dropdown_content(self._manager.data.keys())
                    self._table_widget.show()  # Asegúrate de mostrar la tabla aquí
                    self.b2.hide()
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


    #eliminar las cosas de la caja de texto aunque no lo quita del todo tecnicamente, todavia lo tiene en memoria
    def clear_data(self):
        if not self._file_name:
            print("No hay archivo seleccionado.")
        else:

            self._text_box.clear()
            self._file_name = ""
            self._table_widget.setModel(None)

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
            self._graph.hide()

            self.b2.hide()

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

    def plot_regression(self, columnas_entrada, columna_salida, *args):
        """Llama a la función `entrenar_y_graficar_modelo` y muestra los resultados en la interfaz."""
        try:
            if len(args) == 0:
            # Llamada a la función para entrenar el modelo y obtener la fórmula y métricas
                data = self._manager.data
            else:
                data = args[0]

            self._formula, self._metricas[0], self._metricas[1], self._modelo, pred = entrenar_modelo(data, [columnas_entrada], columna_salida)
            # Actualiza las etiquetas con la fórmula y métricas
            self.formula_label.setText(f"Fórmula de Regresión: {self._formula}")
            self.r2_label.setText(f"R²: {self._metricas[0]:.4f}")
            self.ecm_label.setText(f"ECM: {self._metricas[1]:.4f}")

            self._missing_options.hide()
            self._entry_column.hide()
            self._target_column.hide()
            self._table_widget.hide()
            self._accept_button.hide()
            self._apply_button.hide()

            self._graph.show()
            self._graph.clear()
            self.r2_label.show()
            self.ecm_label.show()
            self.formula_label.show()

            pen = pg.mkPen(color=(0, 0, 0))
            self._graph.plot(data[columnas_entrada], list(data[columna_salida]),
                             symbol = "o", pen = pen )
            self._graph.setLabel("left", columnas_entrada)
            self._graph.setLabel("bottom", columna_salida)

            pen = pg.mkPen(color=(255, 0, 0))
            self._graph.plot(data[columnas_entrada], pred, pen = pen)

            self._graph.plotItem.autoRange()


            # Mensaje de éxito
            ps.QMessageBox.information(self, "Éxito", "El modelo de regresión se ha creado correctamente.")
        
        except Exception as e:
            # Muestra un mensaje de error si algo falla
            ps.QMessageBox.critical(self, "Error", f"Ocurrió un error al crear el modelo: {str(e)}")

    def process_data(self):
        """Detecta los NaN e indica dónde, también controla que no se puedan acceder a ciertas 
        funcionalidades del programa si no son necesarias
        """

        self.save_button.hide()
        self._description_edit.hide()

        self.r2_label.hide()
        self.ecm_label.hide()
        self.formula_label.hide()
        self._graph.hide()
        
        if self._entry_column.currentIndex() == 0 or self._target_column.currentIndex() == 0:
            msg = str("La columna " + "de entrada "*(self._entry_column.currentIndex()==0) 
            + "y la "*(self._entry_column.currentIndex()==self._target_column.currentIndex()) + "de salida "*(self._target_column.currentIndex()==0)+
            "no pertenece/n al archivo instertado")

            ps.QMessageBox.warning(self, "Error", msg)

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
        columnas_entrada = entry_column
        columna_salida = target_column
        self.plot_regression(columnas_entrada, columna_salida)
            
         #Muestra el botón para guardar el modelo y el campo de descripción
        self.save_button.show()
        self._description_edit.show()
        self._table_widget.hide()
        self._entry_column.hide()  
        self._target_column.hide()
        self._accept_button.hide()


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

