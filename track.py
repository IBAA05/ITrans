import math  
import sqlite3 as sqlite   
  
  
data  = {"direction" : None , "station_count" : 0} 
  

class Station :  
      
    def init (self,nom,position) :  
        self.nom = nom   
        self.position = position   
          
def distance_between_position(pos1,pos2):  
         
    lat1, lon1 =  pos1 
    lat2, lon2  = pos2 
         
    R = 6371  # Rayon de la Terre en kilomètres  
    dLat = math.radians(lat2 - lat1)  
    dLon = math.radians(lon2 - lon1)  
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
    math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
    math.sin(dLon / 2) * math.sin(dLon / 2)  
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  
    return abs(round(R * c * 1000))  # Distance en mètres        
  
 
class DataBaseStation :  
      
    def init(self) :  
        self.connection = sqlite.connect('./stations.db')  
        self.cursor = self.connection.cursor()  
      
    def getStations (self,direction) :   
          
        """"  
        direction : represent if going or outgoing   
          
          
        """  
          
          
        # self.cursor.execute("""  
                              
        #                     SELECT  *  
        #                     FROM direction1 AS d1   
                              
        #                     """  
        #                     )  
          
    def first_station (self) :  
          
        self.cursor.execute("""  
                              
            SELECT  *   
            FROM direction1   
            LIMIT 1 ;  
            """)  
        data = self.cursor.fetchall() 
        for row in data :    
            return row    # return the lat,en of the first station   
      
    def last_station (self) :  
          
        self.cursor.execute("""                      
            SELECT  *   
            FROM direction2    
            LIMIT 1 ;  
            """)  
        data = self.cursor.fetchall() 
        for row in data :    
            return row   # return the lat, long of the last station   
        
    # def next_station(self, current_station, direction):
    #     if direction == 'airport':
    #         self.cursor.setinputsizes(current_station)
    #         self.cursor.execute("""
    #             WITH OrderedStations AS (
    #                 SELECT nameEN, 
    #                     ROW_NUMBER() OVER (ORDER BY nameEN) AS rn
    #                 FROM direction1
    #             )
    #             SELECT nameEN
    #             FROM OrderedStations
    #             WHERE rn = (
    #                 SELECT rn + 1
    #                 FROM OrderedStations
    #                 WHERE nameEN = 'Zouaghi Sliman'
    #             )
    #             LIMIT 1
    #         """, (current_station,))
    #         next_station = self.cursor.fetchone()
    #         return next_station[0] if next_station else None
    #     else:
    #     # Handle other directions if necessary
    #         pass
    def next_station(self, current_station, direction):
        if direction == 'airport':
            self.cursor.setinputsizes(current_station)
            self.cursor.execute("""
                SELECT nameEN
                FROM direction1
                WHERE Id = (
                    SELECT Id + 1
                    FROM direction1
                    WHERE nameEN = ?
                )
            """, (current_station,))
            next_station = self.cursor.fetchone()
            return next_station[0] if next_station else None
        else:
        # Handle other directions if necessary
            pass
# def next_station (self, current_pos, direction = 'going') :  
         
    #     if direction == 'going':  
             
    #         sql = """ 
    #         SELECT * 
    #         FROM direction1 
    #         WHERE lat >= ? AND lang >= ? 
    #         ORDER BY lat, lang 
    #         LIMIT 1; 
    #         """ 
    #         self.cursor.execute(sql, (current_pos[0], current_pos[1]))   # the first parameter is latitudew and the second one is the longtitude .             
    #         data = self.cursor.fetchall()  
    #         print(data)  
    
    def close (self) :  
        self.connection.close()       
          
      
def track (pos,direction) :  
         
    if direction =='airoport':      
        db = DataBaseStation()    
        current_station=db.first_station()          
        pos_first = db.first_station ()   
        pos_last = db.last_station ()       
            
        distance_pos_first = distance_between_position(pos,pos_first) 
        distance_pos_last = distance_between_position(pos,pos_last) 
            
        if data['direction'] == None : 
                
            if distance_pos_first < 50 : 
                data['direction'] = "going" 
                return db.first_station() 
                    
            elif distance_pos_last < 50 : 
                data['direction'] = "returning" 
                return db.last_station()  
            else : 
                return "no station found"  
                
                
        elif data ['direction'] == 'going' or  data ['direction'] == 'returning' :  
                
            next_station = db.next_station(pos,data['direction']) 
            distance = distance_between_position(pos, (next_station[3],next_station[4]) ) 
                    
        if ( distance > 100 ) :  
            return {"state" : 1 , "message" : "next station  is {near_station.name}"}                   
        elif( distance < 50 ) :  
            print(f"We'll be arriving soon at station {near_station.name}")  
            return {"state" : 2 , "message" : "nextstation  is {near_station.name}" } 
                
        elif ( distance < 25 ) :  
            print(f" we are in  station {near_station.name}")   
            {"state" : 3 , "message" : "next station  is {near_station.name}" }        

    db = DataBaseStation ()  
    #db.next_station((36.3327333,6.6158633)) 
    res = db.last_station() 
    #print(res)
db = DataBaseStation ()    
res2=db.next_station("Zarzara","airport")
print(res2)