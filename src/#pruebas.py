import pandas as pd

def importar_datos_excel():
    try:
        # Ruta al archivo Excel (ajustada correctamente)
        ruta_archivo = r"C:\Users\Lucia\Downloads\housing.xlsx"  # Ajusta según las opciones 1, 2 o 3
        
        # Cargar datos de Excel
        datos = pd.read_excel(ruta_archivo)
        
        # Mostrar las primeras filas de los datos cargados
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
    importar_datos_excel()


