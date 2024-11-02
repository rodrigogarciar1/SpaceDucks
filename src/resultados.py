from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ResultadosWidget(QWidget):
    def __init__(self, formula, r2, ecm):
        super().__init__()

        self.setWindowTitle("Resultados del Modelo")
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Fórmula: {formula}"))
        layout.addWidget(QLabel(f"Coeficiente de determinación (R²): {r2:.4f}"))
        layout.addWidget(QLabel(f"Error Cuadrático Medio (ECM): {ecm:.4f}"))

        self.setLayout(layout)