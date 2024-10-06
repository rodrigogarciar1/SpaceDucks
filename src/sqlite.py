import pandas as pd
import sqlite3 as sq



def read_files():
        """
        Method that reads the given file and stores the data.
        """
        file = input("Enter the name of the file (accepted formats: .db):  ")
        if not file.lower().endswith(".db"): #Checks if the file is in the valid format
            print("ERROR: Invalid format.\n")
            return
        try:
            open(file) #Checks if it exists
        except:
            print("ERROR: File not found.\n")
            return
        
        conn = sq.connect(file)

        # write the data frame to the db

        conn.commit()

        # read back from the database
        print(pd.read_sql(f'select * from {file[:-3]}', conn))

        conn.close()
        
        print("File read succesfully.\n")
        del catalog; del lines; del parts
