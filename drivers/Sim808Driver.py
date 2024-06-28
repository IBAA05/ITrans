import serial
import time
import json

            
def getGPSInfo():
    with open('./../sim808Config.json','r') as file:
        data = json.load(file)
        return data 


class Sim808Driver :

    def __init__(self ,  timeout=2):
        
        try:
            data = getGPSInfo()
            self.port = data['port'] 
            self.baudrate = data ['baudrate']
            self.serial = serial.Serial(self.port, self.baudrate, timeout=timeout)
            print("Serial port initialized successfully.")
        
        except serial.SerialException as e:
            print(f"Error initializing serial port: {e}")
            self.serial = None
        

    def send_at_command(self, command):

        try:
            self.serial.write((command + '\r\n').encode())
            time.sleep(0.5)  # Delay to allow for response
            reply = []
            start_time = time.time()
            
            while (time.time() - start_time) < 1:  # Wait up to 2 seconds for the response
                line = self.serial.readline().decode().strip()
                if line:
                    reply.append(line)
            if not reply:
                print("No data received from the module.")
            return reply
        
        except Exception as e:
            print(f"Error sending AT command: {e}")
            return []

    def close(self):
        if self.serial:
            self.serial.close()
            
    def is_initialized(self):
        if not self.serial:
            print('Failed to initialize serial port')
            return False
        return True 
   
   
    def get_lat_lng(self):

        self.send_at_command('AT')
        self.send_at_command('AT+CGNSPWR=1')
        time.sleep(2) # Allow some time for the GPS to power up
        response = self.send_at_command('AT+CGNSINF')
        print('GPS Info Response:', response)

        for line in response:
            if '+CGNSINF' in line:
                lat, lon = self.parse_lat_lng(line)
                if lat and lon:
                    return lat, lon
        return None, None
   
    def parse_lat_lng(self,data):
        
         parts = data.split(',')
         if len(parts) >= 4:
             lat = parts[3]
             lon = parts[4]
             return lat, lon
         
         return None, None
   