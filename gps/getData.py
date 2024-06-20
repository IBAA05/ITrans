import time
from driver import SIMGPS

class SIM_Manager:

    def __init__(self):
        self.driver = SIMGPS ()

    def initialize_serial(self):
        if not self.driver.ser:
            print('Failed to initialize serial port')
            return False
        return True 

    def parse_gps_data(self,data):
    # The GPS data is in the format: +CGNSINF: 1,1,YYYYMMDDHHMMSS.000,lat,lon,...
     parts = data.split(',')
     if len(parts) >= 4:
         lat = parts[3]
         lon = parts[4]
         return lat, lon
     return None, None

    def get_gps_position(self):

        self.driver.send_at_command('AT')
        self.driver.send_at_command('AT+CGNSPWR=1')
        time.sleep(2) # Allow some time for the GPS to power up
        response = self.driver.send_at_command('AT+CGNSINF')
        print('GPS Info Response:', response)

        for line in response:
            if '+CGNSINF' in line:
                lat, lon = self.parse_gps_data(line)
                if lat and lon:
                    return lat, lon
        return None, None