import math  
import sqlite3 as sqlite   
from datetime import datetime
import subprocess
import json

# Read the JSON file
def read_const (): 
    global STATION_BORDER 
    global INTERSTATION_BORDER
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

        # fill  the constants
        STATION_BORDER = config.get("STATION_BORDER")
        INTERSTATION_BORDER = config.get("INTERSTATION_BORDER")



direction =  None # The default direction . 
      
def distance_between_position(pos1,pos2):  
         
    #lat1, lon1 =  pos1 
    #lat2, lon2  = pos2 
    lat1, lon1 = map(float, pos1)
    lat2, lon2 = map(float, pos2)   
    R = 6371  # Rayon de la Terre en kilomètres  
    dLat = math.radians(lat2 - lat1)  
    dLon = math.radians(lon2 - lon1)  
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
    math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
    math.sin(dLon / 2) * math.sin(dLon / 2)  
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  
    return abs(round(R * c*1000))  # Distance en mètres        
  
 
class DataBaseStation :  
      
    def __init__ (self) :  
        self.connection = sqlite.connect('./stations.db')  
        self.cursor = self.connection.cursor()  
       
    def get_going (self) :      
        self.cursor.execute("""  
                              
            SELECT  *   
            FROM going   
             ;  
            """)  
        data = self.cursor.fetchall() 
        return data 
      
    def get_returning(self) :    
        self.cursor.execute("""                      
            SELECT  *   
            FROM back    
            ;  
            """)  
        data = self.cursor.fetchall() 
        return data    
    
    def get_interstation_go (self) :
        self.cursor.execute("""                      
            SELECT  *   
            FROM interstation1  
            ;  
            """)  
        data = self.cursor.fetchall() 
        return data 
    
    def get_interstation_back (self) :
        self.cursor.execute("""                      
            SELECT  *   
            FROM interstation2  
            ;  
            """)  
        data = self.cursor.fetchall() 
        return data 
    
    # def next_station(self, current_station, direction):
        
    #     if direction == 'airport':
    #         self.cursor.setinputsizes(current_station)
    #         self.cursor.execute("""
    #             SELECT *
    #             FROM direction1
    #             WHERE Id = (
    #                 SELECT Id + 1
    #                 FROM direction1
    #                 WHERE nameEN = ?
    #             )
    #         """, (current_station,))
    #         next_station = self.cursor.fetchone()
    #         return next_station if next_station else None
        
      
    def close (self) :  
        self.connection.close()       
  
 
def find_station (pos,stations) : 
    
    """ find the nearest station to the pos 
      Params  :
         direction : List of tuples represent the stations of a direction .  
         pos : The position represents (lat,lang) .
      Return  : 
         find the station      
    
    """   
    for station in stations : 
        station_pos = (station[4], station[5]) # lat , long 
        distance = distance_between_position(pos,station_pos)
        print(distance)
        
        if (distance <= STATION_BORDER)  :
            return station        # we find a station 
    
    return None # in case we dont found . 
     
     
            
def find_interstation (pos,interstations) : 
    
    """" find the nearest interstation  to the position . 
      Params : 
          pos : the current pos (lat,long)
          interstation : List of tuples represent the interstations .
      Return : 
          find an interstation .        
    """     
    for inter in interstations : 
        inter_pos = (inter[4], inter[5]) # lat , long 
        distance = distance_between_position(pos,inter_pos)
        if (distance <= INTERSTATION_BORDER)  :
            return inter        # we find a station 
    return None 
 
    
         
def track (pos) :
    
    read_const ()
     
    
    db = DataBaseStation ()
    if direction != None : 
        if direction == 'going' : 
            stations = db.get_going () 
            inter_stations = db.get_interstation_go () 
        elif direction == 'returning':
            stations = db.get_returning () 
            inter_stations = db.get_interstation_back () 
    

       
        
        stat_res = find_station(pos,stations) 
        print(stat_res)
        inter_res = find_interstation(pos,inter_stations) 
        
        
        if stat_res != None :
            return send_message(pos,"station",stat_res[2]) #   res[2] the name of station in english . 
        elif inter_res != None : 
            return send_message(pos,"interstation",inter_res[2])
        else : 
            return send_message(pos,"unknown","undefined")     
        
    
    
def send_message(pos,typ,name) : 
    data = {
        "token" : "Geolocation" , 
        "type" : "geolocation" , 
        "timestamp" : str(datetime.now()),
        "content " : {
            "location" : {"lat" : pos[0], "long":pos[1]} ,
            "position": { "type": typ, "name": name }
        }
    }
    return data 
            
            
            
db = DataBaseStation ()    
print(track( (36.3537695,6.6122414)))  
