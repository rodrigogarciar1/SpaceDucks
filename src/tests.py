import unittest
import pandas as pd
from modelo import entrenar_modelo, hacer_predicciones
from data_manager import DataManager
from sklearn.linear_model import LinearRegression
import os

class TestModelCreation(unittest.TestCase):

    def setUp(self):
        # Crear un DataFrame de ejemplo
        self.data = pd.DataFrame({
            "feature": [1, 2, 3, 4, 5],
            "target": [2, 4, 6, 8, 10]
        })
        self.columnas_entrada = ["feature"]
        self.columna_salida = "target"

    def test_entrenar_modelo(self):
        # Entrenar el modelo y verificar resultados
        formula, r2, ecm, modelo, predicciones = entrenar_modelo(self.data, self.columnas_entrada, self.columna_salida)
        self.assertIsInstance(modelo, LinearRegression)
        self.assertAlmostEqual(r2, 1.0, places=2)  # R² debe ser 1 para datos perfectos
        self.assertAlmostEqual(ecm, 0.0, places=2)  # ECM debe ser 0 para datos perfectos

    def test_hacer_predicciones(self):
        # Entrenar el modelo y realizar predicción
        _, _, _, modelo, _ = entrenar_modelo(self.data, self.columnas_entrada, self.columna_salida)
        prediccion = hacer_predicciones(modelo, 6)
        self.assertAlmostEqual(prediccion, 12.0, places=2)  # Predicción esperada: 12


class TestModelPersistence(unittest.TestCase):

    def setUp(self):
        # Crear un modelo entrenado y descripción
        self.data_manager = DataManager()
        self.modelo = LinearRegression()
        self.modelo.fit([[1], [2], [3]], [2, 4, 6])
        self.description = "Modelo de prueba"
        self.metrics = {"r2": 1.0, "ecm": 0.0}
        self.formule = "y = 2 * x + 0"
        self.filename = "test_model.joblib"

    def tearDown(self):
        # Eliminar el archivo después de la prueba
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_guardar_y_cargar_modelo(self):
        # Guardar modelo
        self.data_manager.save_model_with_description(self.modelo, self.description, self.metrics, self.formule, self.filename)
        self.assertTrue(os.path.exists(self.filename))  # Verificar que el archivo fue creado

        # Cargar modelo
        modelo_cargado, descripcion_cargada, metrics_cargadas, formule_cargada = self.data_manager.load_model_with_description(self.filename)
        self.assertIsInstance(modelo_cargado, LinearRegression)
        self.assertEqual(descripcion_cargada, self.description)
        self.assertEqual(metrics_cargadas, self.metrics)
        self.assertEqual(formule_cargada, self.formule)


class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.data_manager = DataManager()

    def test_read_invalid_file_extension(self):
        with self.assertRaises(ValueError):
            self.data_manager.read("archivo_invalido.txt")

    def test_read_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.data_manager.read("archivo_inexistente.csv")

    def test_clear_data(self):
        self.data_manager.data = pd.DataFrame({"columna": [1, 2, 3]})
        self.data_manager.clear()
        self.assertTrue(self.data_manager.data.empty)


if __name__ == "__main__":
    unittest.main()
