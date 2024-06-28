from Dao import Dao

class InterstationDao  (Dao):
    
    def __init__(self) : 
        super.__init__()
     
    def insert_data (self,table_name,lat, lng, from_station, to_station) :
        query = f"INSERT INTO {table_name} (lat, long, from_station, to_station) VALUES (?,?,?,?)" 
        self.cursor.execute(query,lat, lng, from_station, to_station)
        
    def get_interstations (self,table_name) :
        self.cursor.execute(f"""                      
            SELECT  *   
            FROM {table_name}  
            ;  
            """)  
        data = self.cursor.fetchall() 
        return data     