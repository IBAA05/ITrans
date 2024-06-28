from Dao import Dao

class ConfigDao (Dao) :
    
    def __init__(self) : 
        super.__init__()
        
    def insert_data (self,key,value) :
        query  = "INSERT INTO config (key, value) VALUES (?, ?) "
        self.cursor.execute(query, (key,value))
         
    def get_bykey (self,key) :
         
        try : 
            query  = "SELECT * FROM config WHERE key = ?" 
            self.cursor.execute(query,(key,))
            row = self.cursor.fetchone() 
            return row 
        except  Exception:
            return 
   