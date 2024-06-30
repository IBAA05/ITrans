from Dao  import Dao

class LogDao  (Dao):
    
    def __init__(self) : 
        super().__init__()
     
  
    def insert_data (self,message,sender,receiver,received_at) :
         query = "INSERT INTO log (message,sender,receiver,received_at) VALUES (?,?,?,?)" 
         self.cursor.execute(query,(message,sender,receiver,received_at))  
         self.conn.commit()