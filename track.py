
def getPosition () :
    
    connection = 2 #we check  the connection from gps through method 
    
    if connection == None :
        #send request to the driver in the case to update manually the station .
        return -1 # Don't do tracking anymore .
    else :
        return # position from the gps 

def track () :
    
    res  = getPosition () 
    
    if res != -1 :
        station  = "" # it can next or current 
        typ = "" # if it's current or next 
        # inside we do a our logique .
        """
         if we get near from the station it will be our current station 
         else we return the next station 
        """

        
        return typ,station 
           