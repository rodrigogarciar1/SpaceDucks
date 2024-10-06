import pandas as pd
import os

def importar_datos_excel(ruta_archivo):
    try:
        # Verificar que el archivo existe
        if not os.path.isfile(ruta_archivo):
            raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")

        # Verificar que el archivo tiene una extensión válida de Excel
        extension = os.path.splitext(ruta_archivo)[1].lower()
        if extension not in [".xlsx", ".xls"]:
            raise ValueError("Formato de archivo no soportado. Por favor, proporciona un archivo de Excel (.xlsx, .xls).")

        # Cargar datos de Excel de forma eficiente
        datos = pd.read_excel(ruta_archivo, engine='openpyxl')

        # Mostrar las primeras filas de los datos cargados para confirmación
        print("Las primeras filas de los datos cargados:")
        print(datos.head())

        return datos

    except FileNotFoundError:
        print("Error: Archivo no encontrado. Por favor, verifica la ruta del archivo.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Se ha producido un error inesperado: {e}")

# Ejecutar la función para importar datos
if __name__ == "__main__":
    # Ajusta la ruta según la ubicación de tu archivo Excel
    ruta_archivo = r"C:\Users\Lucia\Downloads\housing.xlsx"  
    importar_datos_excel(ruta_archivo)