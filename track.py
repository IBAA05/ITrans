import math
import sqlite3 as sqlite 
from gps import main 


class Station :
    
    def __init__ (self,nom,position) :
        self.nom = nom 
        self.position = position 
        
    def distance_between_position(self,my_pos):
        
        lat1, lon1 =  my_pos
        lat2, lon2  = self.position 
        
        R = 6371  # Rayon de la Terre en kilomètres
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dLon / 2) * math.sin(dLon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return abs(round(R * c * 1000))  # Distance en mètres      

        
class DataBaseStation :
    
    def __init__(self) :
        self.connection = sqlite.connect('./stations.db')
        self.cursor = self.connection.cursor()
    
    def getStations (self,direction) : 
        
        """"
        direction : represent if going or outgoing 
        
        
        """
        
        
        self.cursor.execute("""
                            
                            SELECT  *
                            FROM direction1 AS d1 
                            
                            """
                            )
        
    def first_station (self) :
        
        self.cursor.execute("""
                            
            SELECT  * 
            FROM directions1 
            LIMIT 1 ;
            """)
        
    def last_station (self) :
        
        self.cursor.execute("""                    
            SELECT  * 
            FROM direction2  
            LIMIT 1 ;
            """)
    
    
    def near_station (self,position ) :
        pass


def getPosition () :
    try  :     
        if __name__ == '__main__' :
            lon , lat = main() 
            return lon , lat           
    except Exception :
        return -1 # Don't do tracking anymore .


    
def track () :

    pos  = getPosition () # check if the position can get 


    if pos != -1 :
          
        ds = DataBaseStation()            
                
        near_station = ds.near_station()
       
        while True: # to indicate that this operatin is repeated 
            
            distance = near_station.distance_between_position(pos)
                
            if ( distance > 100 ) :
                return {"state" : 1 , "message" : "next station  is {near_station.name}" }
                
            elif( distance < 50 ) :
                print(f"We'll be arriving soon at station {near_station.name}")
            
            elif ( distance < 25 ) :
                print(f" we are in  station {near_station.name}")        

db = DataBaseStation ()
db.first_station()                