import sys
import PySide6.QtWidgets as ps
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QColor
from data_manager import DataManager   # Importa el módulo data_manager correctamente
from modelo import entrenar_modelo, hacer_predicciones
import pyqtgraph as pg
import os

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
        self._manager = DataManager()
        self._metricas = [0, 0]
        self._formula = ""
        self._current_step = 0
        self.initUI()
        self._steps = [self.main_inner_layout ,self.step_one_layout, self.step_two_layout, self.step_three_layout, self.step_four_layout]
        self.side_bar = [self.step_zero, self.step_one, self.step_two, self.step_three, self.step_four]
        self._read_file = False
       

        for layout in self._steps[1:]:
            layout.setAlignment(Qt.AlignTop)
        
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the file
        sshFile = os.path.join(script_dir, "style.qss")
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

        self.next_step()

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


        # Create a central widget to hold all content
        central_widget = ps.QWidget()
        window_layout = ps.QVBoxLayout(central_widget)

        logo_space = ps.QHBoxLayout()
        self.logo = ps.QLabel(text="SpaceDuck's Linear Regresion Tool")
        self.logo.setObjectName("logo")
        logo_space.addWidget(self.logo)

        self.step_zero = ps.QLabel()
        interactive_layout = ps.QHBoxLayout()

        steps_layout = ps.QVBoxLayout()
        self.step_one = ps.QLabel("1")
        self.step_two = ps.QLabel("2")
        self.step_three = ps.QLabel("3")
        self.step_four = ps.QLabel("4")

        self.add_to_layout(steps_layout, self.step_one, self.step_two, self.step_three, self.step_four)

        for i in range(steps_layout.count()):
            widget = steps_layout.itemAt(i).widget()
            if widget is not None:
                widget.setObjectName("steps")

        main_layout = ps.QVBoxLayout()

        self.main_inner_layout = ps.QVBoxLayout()

        self.step_one_layout = ps.QVBoxLayout()
        # Botón para seleccionar archivo
        
        self.b1 = self.button("Añadir archivos", self.add_file)
        
        self.model_button = self.button("Añadir modelo", self.add_model)
        
        # Label para mostrar el nombre del archivo seleccionado
        self._text_box = ps.QLabel("")
        self._text_box.setObjectName("file_label")

        # Botón para eliminar archivo
        self.b3 = self.button("Eliminar archivo", self.clear_data, hidden=True)

        h1_layout = ps.QHBoxLayout()
        self.add_to_layout(h1_layout, self.b1, self.model_button)

        h2_layout = ps.QHBoxLayout()
        self.add_to_layout(h2_layout, self._text_box, self.b3)

        self.add_to_layout(self.step_one_layout, h1_layout, h2_layout)
        
        self.main_inner_layout.addLayout(self.step_one_layout)


        self.step_two_layout = ps.QVBoxLayout()

        # Tabla para mostrar los datos del DataFrame
        self._table_widget = ps.QTableView()

        linear_menu = ps.QHBoxLayout() #Hace un layout horizontal 

        # Dropdown para la selección de la columna de datos
        self._entry_column = ps.QComboBox()
        self._entry_column.currentIndexChanged.connect(self.change_detected)
        self._entry_column.hide()

        # Dropdown para la selección de la columna objetivo
        self._target_column = ps.QComboBox()
        self._target_column.currentIndexChanged.connect(self.change_detected)
        self._target_column.hide()

        #Botón para procesar el modelo de regresión lineal
        self._accept_button = self.button("Procesar", self.process_data, hidden=True)
        self._accept_button.setStyleSheet("display = inline-box")
        
        self.add_to_layout(linear_menu, self._entry_column, self._target_column, self._accept_button)

        
        
        #Opciones de manejo de valores inexistentes
        self.missing_data_menu = ps.QHBoxLayout()

        self._missing_options = ps.QComboBox()
        self._missing_options.addItems(["-- Selecciona una opcion --","Eliminar filas", "Rellenar con media", "Rellenar con mediana", "Rellenar con valor constante"])
        self._missing_options.model().item(0).setEnabled(False)
        self._missing_options.currentIndexChanged.connect(self.missing_option_changed)
        self._missing_options.hide()  # Deshabilitado inicialmente

        self._constant_value_input = ps.QLineEdit()
        self._constant_value_input.setPlaceholderText("Introduce un valor")
        self._constant_value_input.hide()  #Escondido inicialmente, solo aparece si se selecciona "Rellenar con valor constante"

        self._apply_button = self.button("Aplicar", self.apply_missing_data_strategy, hidden=True)

        self.add_to_layout(self.missing_data_menu, self._missing_options, self._constant_value_input, self._apply_button)

        self.add_to_layout(self.step_two_layout, self._table_widget, linear_menu, self.missing_data_menu)

        self.main_inner_layout.addLayout(self.step_two_layout)



        self.step_three_layout = ps.QVBoxLayout()

        h_layout = ps.QHBoxLayout()
        self._graph = pg.PlotWidget()
        self._graph.setStyleSheet("max-height:600px;")
        self._graph.hide()

        v_layout = ps.QVBoxLayout()
        #Etiqueta para mostrar la fórmula de regresión
        self.formula_label = ps.QLabel("Fórmula de Regresión: ")
        self.formula_label.hide()

        #Etiquetas para mostrar R² y ECM
        self.r2_label = ps.QLabel("R²: ")
        self.ecm_label = ps.QLabel("ECM: ")
        self.ecm_label.hide()
        self.r2_label.hide()
        self.add_to_layout(v_layout, self.formula_label, self.ecm_label, self.r2_label)
        self.add_to_layout(h_layout, self._graph, v_layout)
        self.setWindowTitle("Análisis de Regresión Lineal")

        # Área de texto para la descripción del modelo
        self._description_edit = ps.QTextEdit()
        self._description_edit.setPlaceholderText("Escribe aquí la descripción del modelo (opcional)")
        self._description_edit.hide()
          # Botón para guardar el modelo (incluye descripción)
    
        self.save_button = self.button("Guardar Modelo", self.save_model, hidden=True)

         
        self.add_to_layout(self.step_three_layout, h_layout, self._description_edit, self.save_button)
        
        self.main_inner_layout.addLayout(self.step_three_layout)







        self.step_four_layout = ps.QVBoxLayout()

        self.campo_dinamico = ps.QLineEdit()
        self.campo_dinamico.setPlaceholderText("Introducir número para realizar la predicción")

        self.predict_label = ps.QLabel("Prediction: ")
        self.predict_label.hide()

        self.predict_button = self.button("Predict",self.predict, hidden=True)


        self.add_to_layout(self.step_four_layout,self.predict_button,self.predict_label,self.formula_label,self.campo_dinamico)

        self.main_inner_layout.addLayout(self.step_four_layout)














        next_prev_step_layout = ps.QHBoxLayout()

        self.previous_step_button = self.button("< Anterior", self.prev_step, hidden=True)
        self.next_step_button = self.button("Siguiente >", self.next_step)

        self.previous_step_button.setObjectName("prev")
        self.next_step_button.setObjectName("next")

        self.next_step_button.setDisabled(True)
        self.next_step_button.setToolTip("Introduce un archivo")

        next_prev_step_layout.addWidget(self.previous_step_button)
        next_prev_step_layout.addStretch(1)
        next_prev_step_layout.addWidget(self.next_step_button)

        self.add_to_layout(main_layout, self.main_inner_layout, next_prev_step_layout)


        self.add_to_layout(interactive_layout, steps_layout, main_layout)

        self.add_to_layout(window_layout, logo_space, interactive_layout)

        self.setCentralWidget(central_widget)

        
    def add_model(self):
        file_name, _ = ps.QFileDialog.getOpenFileName(self, "Open Model", filter="Accepted Files (*joblib)")
        if len(file_name)>0:
            self._file_name = file_name
        else:
            return
        
        self._manager.clear()
        self._table_widget.setModel(PandasModel(self._manager.data))
        self._text_box.setText(self._file_name)
        self.next_step_button.setDisabled(False)
        self.next_step_button.setToolTip("Siguiente")
        self._read_file = True
    
    def change_detected(self):
        self._missing_options.setCurrentIndex(0)

        self._hide(self.missing_data_menu)
        return

    def missing_option_changed(self):
        """Mostrar u ocultar la entrada para valor constante dependiendo de la opción seleccionada."""
        if self._missing_options.currentText() == "Rellenar con valor constante":
            self._constant_value_input.show()
        else:
            self._constant_value_input.hide()
        self.next_step_button.setDisabled(True)
        self.next_step_button.setToolTip("Aplica los cambios antes de seguir")
        

    def apply_missing_data_strategy(self):
        """Aplica la estrategia seleccionada para manejar los valores inexistentes."""
        strategy = self._missing_options.currentText()
        entry_column = self._entry_column.currentText()  # Obtener los nombres de las columnas seleccionadas
        target_column = self._target_column.currentText()

        if self._missing_options.currentIndex() == 0:
            ps.QMessageBox.warning(self, "Error", "Por favor, seleccione una de las opciones de estrategia válida.")
            return
        data, entry_column, target_column =self._manager.depurate_nan(self, strategy, entry_column, target_column)

        self.plot_regression(entry_column, target_column, data)
        
        self.next_step_button.setDisabled(False)
        self.next_step_button.setToolTip("Siguiente")
        

    def add_file(self):
        self._graph.hide()
        file_name, _ = ps.QFileDialog.getOpenFileName(self, "Open File", filter="Accepted Files (*.csv *.xlsx *.xls *.db *.sqlite)")
        if len(file_name)<=0:
            return
        
        self._manager.clear()
        self._file_name = file_name
        self._table_widget.setModel(PandasModel(self._manager.data))
        self._text_box.setText(self._file_name)
        self.next_step_button.setDisabled(False)
        self.next_step_button.setToolTip("Siguiente")
        self._read_file = True

    def data_reader(self):
        if self._file_name.endswith(".joblib"):
            try:
                self._modelo, description, self._metricas, self._formula = self._manager.load_model_with_description(self._file_name)
                fn = self._file_name

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

            except:
                raise Exception


        else:
            if self._file_name != "":
                self._manager.read(self._file_name)  #Leer el archivo usando DataManager

            #Verificar si el DataFrame está vacío
                if len(self._manager.data) == 0:
                    self.clear_data()  #Limpiar datos en caso de archivo vacío
                    raise IndexError
            
                self._table_widget.setModel(PandasModel(self._manager.data))  #Mostrar datos en QTextEdit
                self.set_dropdown_content(self._manager.data.keys())
            else:
                print("No se ha seleccionado ningún archivo.")
                ps.QMessageBox.warning(self, "Error", "Por favor, selecciona un archivo primero.")
        


    #eliminar las cosas de la caja de texto aunque no lo quita del todo tecnicamente, todavia lo tiene en memoria
    def clear_data(self):
        if not self._file_name:
            print("No hay archivo seleccionado.")
        else:

            self._text_box.clear()
            self._file_name = ""
            self.next_step_button.setDisabled(True)
            self._manager.clear()
            self._graph.clear()
            self._formula = ""
            self._metricas = [0,0]
            self._hide(self.missing_data_menu)
            self._missing_options.setCurrentIndex(0)
            self._constant_value_input.setText("")

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
            
            self._graph.clear()

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

        self.next_step_button.setDisabled(False)
        self.next_step_button.setToolTip("Siguiente")

        # Llama a plot_regression con las columnas seleccionadas
        columnas_entrada = entry_column
        columna_salida = target_column
        self.plot_regression(columnas_entrada, columna_salida)



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

    def prev_step(self):
        if self._file_name.endswith(".joblib") and self._current_step == 3:
            self._current_step -=2
            step = 2
        else:
            self._current_step -= 1
            step = 1
        self.change_step(self._steps[self._current_step + step], self._steps[self._current_step])
        
    
    def next_step(self):
        # Determine the next step based on the current state
        if self._file_name.endswith(".joblib") and self._current_step == 1:
            step = 2
        else:
            step = 1

        # Update the current step
        self._current_step += step
        print(f"Moving to step: {self._current_step}")
        self.change_step(self._steps[self._current_step - step], self._steps[self._current_step])

    def handle_data_reading(self):
        try:
            self.data_reader()  # Attempt to read data
            print("Data reading successful.")
            return True  # Indicate success
        except (IndexError, FileNotFoundError, PermissionError, ValueError, UnicodeDecodeError, MemoryError) as e:
            # Handle specific exceptions with user feedback
            error_messages = {
                IndexError: "Archivo vacío o sin datos.",
                FileNotFoundError: "No se encontró el archivo.",
                PermissionError: "No tienes permiso para abrir este archivo.",
                ValueError: "Error en el formato del archivo.",
                UnicodeDecodeError: "Error de codificación al leer el archivo.",
                MemoryError: "El archivo es demasiado grande para ser cargado en memoria."
            }
            ps.QMessageBox.warning(self, "Error", error_messages[type(e)])
            self.next_step_button.setDisabled(True)
            self.next_step_button.setToolTip("Introduce un archivo")
            return False  # Indicate failure
        except Exception as e:
            # Handle any unexpected exceptions
            print(f"Caught an unexpected exception: {e}")
            ps.QMessageBox.warning(self, "Error", f"Error inesperado: {str(e)}")
            self.next_step_button.setDisabled(True)
            self.next_step_button.setToolTip("Introduce un archivo")
            return False  # Indicate failure

    def change_step(self, current_phase, next_phase):
        # Check if we need to read data based on the current step and conditions
        if (self._current_step == 2 and len(self._manager.data) == 0) or (self._current_step == 3 and self._file_name.endswith(".joblib")):
            print("Attempting to read data...")
            if not self.handle_data_reading():
                print("Data reading failed, exiting next_step.")
                self._current_step = 1
                return  # Exit if an exception was caught

        print(self._current_step)
        print(self._file_name) 
        # Hide all widgets in the current step
        self._hide(current_phase)

        # Show all widgets in the next phase
        self._show(next_phase)

        

        if self._current_step == 1:
            self.previous_step_button.hide()
        elif self._current_step == 4:
            self.next_step_button.hide()
        else:
            self.previous_step_button.show()
            self.next_step_button.show()
        
        
        self.next_step_button.setDisabled(False)
            
        if self._missing_options.currentIndex() == 0:
                self._hide(self.missing_data_menu)

        if self._current_step == 1 and self._file_name == "":
            self.next_step_button.setDisabled(True)
            self.next_step_button.setToolTip("Introduce un archivo")

        if self._current_step == 2 and self._formula == "":
            self.next_step_button.setDisabled(True)
            self.next_step_button.setToolTip("Procesa los datos antes de continuar")

        if self._current_step == 3 and self._file_name.endswith(".joblib"):  
            self._graph.hide()

        self.change_colors()
        
        if self._read_file:
            ps.QMessageBox.information(self, "Éxito", "El archivo se ha cargado correctamente.")
            self._read_file = False

    def change_colors(self):
        label = self.side_bar[self._current_step]
        label.setStyleSheet("""
        QLabel {
        text-align: center;
        font-size: 16px;
        color: black;
        background-color: #3066BE;
        max-width: 80px;
        min-width: 80px;
        margin-top: -5px;
        margin-left: 0px;
        }""")
        label.setAlignment(Qt.AlignCenter)

        for i in reversed(range(0, self._current_step)):
            label = self.side_bar[i]
            label.setStyleSheet("""
            QLabel {
            text-align: center;
            font-size: 16px;
            color: black;
            background-color: lightgray;
            max-width: 80px;
            min-width: 80px;
            margin-top: -5px;
            margin-left: 0px;
            }""")
            label.setAlignment(Qt.AlignCenter)

        for i in range(self._current_step+1, 5):
            label = self.side_bar[i]
            label.setStyleSheet("""
            QLabel {
            text-align: center;
            font-size: 16px;
            color: black;
            background-color: #B4C5E4;
            max-width: 80px;
            min-width: 80px;
            margin-top: -5px;
            margin-left: 0px;
            }""")
            label.setAlignment(Qt.AlignCenter)

    def _hide(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    # Hide the widget if it's not a layout
                    widget.hide()
                else:
                    # If it's a layout, recursively hide its widgets
                    sub_layout = item.layout()
                    if sub_layout is not None:
                        self._hide(sub_layout)

    def _show(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    # Hide the widget if it's not a layout
                    widget.show()
                else:
                    # If it's a layout, recursively hide its widgets
                    sub_layout = item.layout()
                    if sub_layout is not None:
                        self._show(sub_layout)
            
    def predict(self):
        texto = float(self.campo_dinamico.text())
        a = hacer_predicciones(self._modelo,texto)
        self.predict_label.setText(f"Prediction: {a}")


if __name__ == "__main__":
    app = ps.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

