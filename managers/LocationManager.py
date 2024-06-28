from location.drivers.Sim808Driver import Sim808Driver

class LocationManager:

    def __init__(self):
        self.driver = Sim808Driver ()
        
    def is_initialized(self):
        if not self.driver.is_initialized():
            print('Failed to initialize driver') 
            return False
        return True 
    

    def get_location(self) :
        
        (lat, lng)  = self.driver.get_lat_lng()
        
        return (lat, lng)