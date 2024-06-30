from daos.Dao import Dao

class ConfigDao (Dao) :
    
    def __init__(self) : 
        super().__init__()
        
    def insert_data (self, key, value):
        
        query = "INSERT INTO config (key, value) VALUES (?, ?) "
        self.cursor.execute(query, (key,value))
        self.conn.commit()
         
    def get_value_by_key (self, key):
         
        try : 
            query = 'SELECT value FROM config WHERE key = ?'
            self.cursor.execute(query,(key,))
            row = self.cursor.fetchone()
            return row[0]

        except Exception  as e:
            print(e)
   