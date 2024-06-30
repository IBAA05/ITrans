from Dao import Dao 

class StationDao(Dao):
    
    def __init__(self) : 
        super().__init__()
        
    def insert_data (self,table_name,id,name_ar,name_en,name_fr,lat, lng, order) :
        query = f"INSERT INTO {table_name} (id,name_ar,name_en,name_fr,lat, lng, ord) VALUES (?,?,?,?,?,?,?)"
        self.cursor.execute(query,(id,name_ar,name_en,name_fr,lat, lng,order,))
        self.conn.commit()
        
    def get_stations(self,table_name) :      
        self.cursor.execute(f"""  
                              
            SELECT  *   
            FROM {table_name}   
             ;  
            """)  
        data = self.cursor.fetchall() 
        return data  