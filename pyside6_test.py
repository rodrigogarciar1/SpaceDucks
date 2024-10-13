import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Test PySide6")

        layout = QVBoxLayout()

        self._text_field = QLineEdit()
        layout.addWidget(self._text_field)

        self._button = QPushButton(text= "Presiona para ver texto")
        self._button.clicked.connect(self.change_text)
        layout.addWidget(self._button)

        self._text_box = QLabel("")
        layout.addWidget(self._text_box)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        

    def change_text(self):
        if self._text_box.text() == "":
            self._text_box.setText("Haz click al botón para hacerme desaparecer") 
        else:
            self._text_box.setText("")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
