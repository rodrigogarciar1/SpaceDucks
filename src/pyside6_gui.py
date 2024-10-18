import sys
import PySide6.QtWidgets as ps

class MainWindow(ps.QMainWindow):
    def __init__(self):
        super().__init__()

        self._file_name = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Regresión Linear")

        layout = ps.QVBoxLayout()

        self._button = ps.QPushButton(text= "Añadir Archivo")
        self._button.clicked.connect(self.add_file)
        layout.addWidget(self._button)

        self._text_box = ps.QLabel("")
        self._text_box.setStyleSheet("background-color: gray; color: blue; max-height: 25px; max-width: 600px; padding: 5px")
        layout.addWidget(self._text_box)
        
        central_widget = ps.QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        

    def add_file(self):
        self._file_name, fodder = ps.QFileDialog.getOpenFileName(self, str("Open File"),filter= str("Accepted Files (*.csv *.xlsx *.xls *.db *.sqlite)"))
        self._text_box.setText(self._file_name)

        del fodder


app = ps.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()