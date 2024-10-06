import sqlite3 as sq



def read_files():
        """
        Method that reads the given file and stores the data.
        """
        file = input("Enter the name of the file (accepted formats: .db):  ")
        if not file.lower().endswith(".db"): #Checks if the file is in the valid format
            print("ERROR: Invalid format.\n")
            return

        conn = sq.connect(file)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for table in c.fetchall():
            yield list(c.execute('SELECT * from ?;', (table[0],)))
        
        print("File read succesfully.\n")


read_files()
