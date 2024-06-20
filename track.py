import math  
import sqlite3 as sqlite   

import sys
sys.path.append('C:/Users/asus/Desktop/ITrans/gps')  # Adjust path accordingly

from gps.getData import SIM_Manager  
  
direction =  None # the defualt direction . 
  
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
          
     
def track () :
    
    """ Track the position of the bus 
       direction  : String represent the direction of the bus we get it from the driver . 
       
    """ 
    db = DataBaseStation()
   
    current_station = db.first_station()  # At the begining of a direction 
    
    next_station = db.next_station(current_station, direction) 
    
    if direction != None : # the driver gives us the direction . 
    
        while next_station != None : # we arrive at the end of a direction .
            
            pos = SIM_Manager().get_gps_position() # get the position . 
            
            current_stationPos = current_station[5],current_station[4] # lat and len
            
            next_stationPos= next_station[5],next_station [4]  # lat and len 
            
            distanceToCurrent = distance_between_position(pos,current_stationPos) # distance from our position to th current or we can say the previous station .
            distanceTo_Next = distance_between_position(pos,next_stationPos)  # distance between current pos and the next station 
            
            if distanceToCurrent < 25 : # we are in the current station . 
                print("sending state that we are in current station")
                return {"state" : 1,"station" : current_station}
                
            elif distanceTo_Next <= 25 : # we arrive at the next station 
                print("sending state that we are in ztation b")
                current_station = next_station
                next_station = db.next_station(current_station,direction)
                return {"state" : 1 , "station" : next_station}
                
            else: # we are in in the road . 
                print("sending state that we are between current and next")
                return { "state" : 2 , "station" : next_station } 
        
    else : # driver doesnt send any direction 
        print("def")
        return {"state" : 0 ,"station" : DataBaseStation().first_station()}        
        
   
    
db = DataBaseStation ()    
res2 = db.next_station("Airport - New terminal","airport")
print(track())