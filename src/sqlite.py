import sqlite3 as sq

def read_files():

    file = input("Enter the name of the file (accepted formats: .db):  ")
    if not file.lower().endswith(".db"): #Checks if the file is in the valid format
        print("ERROR: Invalid format.\n")
        return

    # Conexión a la base de datos SQLite
    conexion = sq.connect(file)

    # Crear un cursor para ejecutar consultas SQL
    cursor = conexion.cursor()

    # Ejecutar una consulta (por ejemplo, para leer todas las tablas)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # Obtener los nombres de las tablas
    tablas = cursor.fetchall()
    print("Tablas en la base de datos:", tablas)

    # Suponiendo que queremos leer datos de una tabla en particular
    nombre_tabla = tablas[0][0]  # Selecciona la primera tabla encontrada
    print(f"Leyendo datos de la tabla: {nombre_tabla}")

    # Leer todos los datos de la tabla
    cursor.execute(f"SELECT * FROM {nombre_tabla};")
    filas = cursor.fetchall()

    # Imprimir las filas obtenidas
    for fila in filas:
        print(fila)

    # Cerrar la conexión cuando termines
    conexion.close()

read_files()
