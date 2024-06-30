from daos.Dao import Dao

class CalibrateLogDao (Dao) :
    
    def __init__(self) : 
        super().__init__()
        
    def insert_data(self,location,position) :
        
        try : 
            query = "INSERT INTO calibrate (key, value) VALUES (?, ?) "
            self.cursor.execute(query, (location,position))
            self.conn.commit()
        except Exception as e: 
            print(e) 