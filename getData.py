import time
from driver import SIMGPS

class SIM_Manager:
    
    def __init__(self):
        self.driver = SIMGPS
        
    def initialize_serial(self):
        if not self.driver.ser:
            print('Failed to initialize serial port')
            return False
        return True 
    
    def get_gps_position(self):
        
        self.driver.send_at_command('AT')
        self.driver.send_at_command('AT+CGNSPWR=1')
        time.sleep(2) # Allow some time for the GPS to power up
        response = self.driver.send_at_command('AT+CGNSINF')
        print('GPS Info Response:', response)

        for line in response:
            if '+CGNSINF' in line:
                lat, lon = self.driver.parse_gps_data(line)
                if lat and lon:
                    return lat, lon
        return None, None
    def close(self):
        self.driver.close()