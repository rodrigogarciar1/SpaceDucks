import sys

class ProcesadorCSV():
    def __init__(self, archivo_csv):
        """
        Separa el archivo en lineas, obtiene la primera fila y crea una variable para almacenar los datos tras ser procesados
        """
        self.lineas = archivo_csv.split("\n")
        self.caracteristicas = self.lineas[0]
        self.matriz_procesada=[]
    
    def is_float(self,text:str):
        """
        Verifica si un elemento es float o no

        """
        try:
            float(text)
            return True
        except ValueError:
            return False
        
    def separar_comas(self,lista:list):
        """
        Toma un el archivo csv, ya separado por lineas, y lo separa por comas
        """
        for linea in range(len(lista)):
            lista_elementos = lista[linea].split(",")
            lista[linea] = lista_elementos # Aquí reemplaza el str por una lista con los strs pero ya separados por comas
        return lista
    
    def clasificar_datos(self,lista: list):
        """
        Clasifica los datos convirtiendo los elementos numéricos a float.
        """
        for i in range(len(lista)):  
            for j in range(len(lista[i])):  
                elemento = lista[i][j]
                if self.is_float(elemento):  # Verifica si el elemento puede ser convertido a float
                    lista[i][j] = float(elemento)  # Convierte el elemento a float
                if elemento == "" and j != len(lista[i])-1:
                    lista[i][j] = None
        return lista
    
    def procesar_csv(self):
        """
        Utiliza todas las funciones anteriores para crear una matriz ya procesada, almacenarla y devolverla
        """
        csv_sin_comas = self.separar_comas(self.lineas)
        csv_procesado = self.clasificar_datos(csv_sin_comas)
        if csv_procesado[-1] == [''] or csv_procesado[-1] == [""]: #en caso de que se haya dejado una linea en blanco al final del csv
            del csv_procesado[-1]
        self.matriz_procesada = csv_procesado
        return csv_procesado
    
if __name__ == "__main__":
    with open(sys.argv[1]) as f: #pruebas de la clase ProcesadorCSV
        CSV_Doc = f.read()

        print(CSV_Doc[:5])
        a = ProcesadorCSV(CSV_Doc)
        print(a.procesar_csv())

