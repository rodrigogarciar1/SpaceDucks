import pandas as pd

#poner la ruta del archivo
file_path = 'C:\\Users\\Lucia\\Downloads\\housing.xlsx'

def cargar_datos_excel(file_path):
    try:
        # Intenta cargar el archivo Excel
        data = pd.read_excel(file_path, sheet_name=None)  # Carga todas las hojas
        print(f"Archivo '{file_path}' cargado exitosamente.")
        
        # Verifica si hay hojas en el archivo
        if not data:
            print("La tabla no existe o el archivo está vacío.")
            return

        # Si el archivo tiene múltiples hojas, selecciona la primera por defecto
        first_sheet_name = list(data.keys())[0]
        df = data[first_sheet_name]

        # Muestra las primeras filas del DataFrame
        print(f"Mostrando las primeras filas de la hoja: {first_sheet_name}")
        print(df.head())

    except ValueError as e:
        print(f"Formato de archivo inválido: {e}")
    except FileNotFoundError:
        print("Archivo no encontrado. Por favor, verifica la ruta del archivo.")
    except Exception as e:
        print(f"Ocurrió un error al cargar el archivo: {e}")

cargar_datos_excel(file_path)