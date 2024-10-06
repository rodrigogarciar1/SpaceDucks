import pandas as pd

# Ruta al archivo Excel (ajusta según la ubicación de tu archivo)
file_path = 'C:\\Users\\Lucia\\Downloads\\housing.xlsx'

def cargar_datos_excel(file_path):
    try:
        # Intentar cargar el archivo Excel
        data = pd.read_excel(file_path, sheet_name=None)  # Carga todas las hojas
        print(f"Archivo '{file_path}' cargado exitosamente.")
        
        # Verificar si hay hojas en el archivo
        if not data:
            print("La tabla no existe o el archivo está vacío.")
            return

        # Si el archivo tiene múltiples hojas, seleccionar la primera por defecto
        first_sheet_name = list(data.keys())[0]
        df = data[first_sheet_name]

        # Mostrar las primeras filas del DataFrame
        print(f"Mostrando las primeras filas de la hoja: {first_sheet_name}")
        print(df.head())

    except ValueError as e:
        print(f"Formato de archivo inválido: {e}")
    except FileNotFoundError:
        print("Archivo no encontrado. Por favor, verifica la ruta del archivo.")
    except Exception as e:
        print(f"Ocurrió un error al cargar el archivo: {e}")

# Llamar a la función para cargar y mostrar los datos
cargar_datos_excel(file_path)