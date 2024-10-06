import pandas as pd

def importar_datos_excel():
    try:
        # Ruta absoluta al archivo Excel en Descargas
        ruta_archivo = "C:\Users\Lucia\Downloads\housing.xlsx"
        
        # Cargar datos de Excel
        datos = pd.read_excel(ruta_archivo)
        
        # Mostrar las primeras filas de los datos
        print("Las primeras filas de los datos cargados:")
        print(datos.head())
        
        return datos

    except FileNotFoundError:
        print("Error: Archivo no encontrado. Por favor, verifica la ruta del archivo.")
    except ValueError:
        print("Error: Formato de archivo inválido. Por favor, proporciona un archivo de Excel válido.")
    except Exception as e:
        print(f"Se ha producido un error: {e}")

# Ejecutar la función para importar datos
if __name__ == "__main__":
    importar_datos_excel()
