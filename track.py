import math  
import sqlite3 as sqlite   
from getData import SIM_Manager  
  
data  = {"direction" : None} 
  
  
class Station :  
      
    def __init__ (self,nom,position) :  
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
    return abs(round(R * c*1000))  # Distance en mètres        
  
 
class DataBaseStation :  
      
    def __init__(self) :  
        self.connection = sqlite.connect('./stations.db')  
        self.cursor = self.connection.cursor()  
       
    def first_station (self) :  
          
        self.cursor.execute("""  
                              
            SELECT  *   
            FROM direction1   
            LIMIT 1 ;  
            """)  
        data = self.cursor.fetchall() 
        for row in data :    
            return row    # return the all informations of the first station of a direction .   
      
    def last_station (self) :  
          
        self.cursor.execute("""                      
            SELECT  *   
            FROM direction2    
            LIMIT 1 ;  
            """)  
        data = self.cursor.fetchall() 
        for row in data :    
            return row    # return the all informations of the last  station of a direction .   
    
    
    def next_station(self, current_station, direction):
        
        if direction == 'airport':
            self.cursor.setinputsizes(current_station)
            self.cursor.execute("""
                SELECT *
                FROM direction1
                WHERE Id = (
                    SELECT Id + 1
                    FROM direction1
                    WHERE nameEN = ?
                )
            """, (current_station,))
            next_station = self.cursor.fetchone()
            return next_station if next_station else None
        
        # else:
        # # Handle other direction  if necessary
        #     pass
    def close (self) :  
        self.connection.close()       
          
     
def track (direction = 'airoport') :
    
    """ Track the position of the bus 
       direction  : String represent the direction of the bus we get it from the driver . 
       
    """ 
    db = DataBaseStation()
   
    current_station = db.first_station()  # At the begining of a direction 
    
    next_station = db.next_station(current_station, direction) 
    
    while next_station[0] != None : # we arrive at the end of a direction .
        
        pos = SIM_Manager().get_gps_position() # get the position . 
        
        current_stationPos = current_station[5],current_station[4] # lat and len
        
        next_stationPos= next_station[5],next_station [4]  # lat and len 
        
        distanceToCurrent = distance_between_position(pos,current_stationPos) # distance from our position to th current or we can say the previous station .
        distanceTo_Next = distance_between_position(pos,next_stationPos)  # distance between current pos and the next station 
        
        if distanceToCurrent < 25 : # we are in the current station . 
            print("sending state that we are in current station")
            
        elif distanceTo_Next <= 25 : # we arrive at the next station 
            print("sending state that we are in ztation b")
            current_station = next_station
            next_station = db.next_station(current_station,direction)
            
        else: # we are in in the road . 
            print("sending state that we are between current and next")
        
        
        
    # if direction =='airoport':      
    #     db = DataBaseStation()    
    #     current_station=db.first_station()          
    #     pos_first = db.first_station ()   
    #     pos_last = db.last_station ()       
            
      
            
    #     if data['direction'] == None : 
                
    #         if distance_pos_first < 50 : 
    #             data['direction'] = "going" 
    #             return db.first_station() 
                    
    #         elif distance_pos_last < 50 : 
    #             data['direction'] = "returning" 
    #             return db.last_station()  
    #         else : 
    #             return "no station found"  
                
                
    #     elif data ['direction'] == 'going' or  data ['direction'] == 'returning' :  
                
    #         next_station = db.next_station(pos,data['direction']) 
    #         distance = distance_between_position(pos, (next_station[3],next_station[4]) ) 
                    
    #     if ( distance > 100 ) :  
    #         return {"state" : 1 , "message" : "next station  is {near_station.name}"}                   
    #     elif( distance < 50 ) :  
    #         print(f"We'll be arriving soon at station {near_station.name}")  
    #         return {"state" : 2 , "message" : "nextstation  is {near_station.name}" } 
                
    #     elif ( distance < 25 ) :  
    #         print(f" we are in  station {near_station.name}")   
    #         {"state" : 3 , "message" : "next station  is {near_station.name}" }        
    
db = DataBaseStation ()    
res2 = db.next_station("Airport - New terminal","airport")
print(db.first_station())