from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea

app = QApplication([])

# Widget que contendrá el contenido extenso
content_widget = QWidget()
content_layout = QVBoxLayout()

for i in range(1, 101):
    label = QLabel(f"Etiqueta número {i}")
    content_layout.addWidget(label)

content_widget.setLayout(content_layout)

# Creamos un QScrollArea y le asignamos el widget de contenido
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)  # Permite que el contenido se redimensione con la ventana
scroll_area.setWidget(content_widget)  # Establecemos el widget dentro del área de scroll

# Creamos la ventana principal
window = QWidget()
layout = QVBoxLayout(window)
layout.addWidget(scroll_area)

window.setWindowTitle("Ejemplo de Scroll")
window.resize(300, 200)  # Tamaño de la ventana
window.show()

app.exec()
