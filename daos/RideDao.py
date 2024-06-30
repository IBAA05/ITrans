from daos.Dao  import Dao
import time 
  
class RideDao  (Dao):
    
    def __init__(self) : 
        super().__init__()
        
    def insert_data(self,line,direction,started_at,finished_at) : 
        query = "INSERT INTO ride (line,direction,started_at,finished_at) VALUES (?,?,?,?)" 
        self.cursor.execute(query,(line,direction,started_at,finished_at))  
        self.conn.commit()
        
    def get_current_direction (self) :
        try :  
          self.cursor.execute ("SELECT direction FROM ride WHERE finished_at  IS NULL ")
          row = self.cursor.fetchone() 
          return (row[0]) # return the direction .
          
        except Exception : 
             return None
   
    def finished_the_ride (self) :
        
        finished_time = int (time.time())
        query =  "UPDATE ride SET finished_at = ? WHERE finished_at IS NULL"
        self.cursor.execute(query, (finished_time)) 
        self.conn.commit()      
        
    def has_progressed(self):
        
        query = "SELECT EXISTS(SELECT 1 FROM ride WHERE finished_at IS NULL LIMIT 1)"
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]  # fetchone() returns a tuple; [0] gets the first column value
        return bool(result)  # Convert 1 or 0 to True or False
