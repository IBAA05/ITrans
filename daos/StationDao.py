from Dao import Dao 

class StationDao():
    
    def __init__(self) : 
        super.__init__()
        
    def insert_data (self,table_name,id,name_ar,name_en,name_fr,lat, long, order) :
        query = f"INSERT INTO {table_name} (id,name_ar,name_en,name_fr,lat, long, order) VALUES (?,?,?,?,?,?,?)" 
        self.cursor.execute(query,(id,name_ar,name_en,name_fr,lat, long, order))
       
    def get_stations(self,table_name) :      
        self.cursor.execute(f"""  
                              
            SELECT  *   
            FROM {table_name}   
             ;  
            """)  
        data = self.cursor.fetchall() 
        return data  