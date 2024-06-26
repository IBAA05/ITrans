import serial
import time
import json



class SIMGPS :

    def __init__(self ,  timeout=2):
        try:
            data = getGPSInfo()
            self.port = data['port'] 
            self.baudrate = data ['baudrate']
            self.ser = serial.Serial(self.port, self.baudrate, timeout=timeout)
            print("Serial port initialized successfully.")
        except serial.SerialException as e:
            print(f"Error initializing serial port: {e}")
            self.ser = None
        

    def send_at_command(self, command):

        try:
            self.ser.write((command + '\r\n').encode())
            time.sleep(0.5)  # Delay to allow for response
            reply = []
            start_time = time.time()
            while (time.time() - start_time) < 1:  # Wait up to 2 seconds for the response
                line = self.ser.readline().decode().strip()
                if line:
                    reply.append(line)
            if not reply:
                print("No data received from the module.")
            return reply
        except Exception as e:
            print(f"Error sending AT command: {e}")
            return []

    def close(self):
        if self.ser:
            self.ser.close()
            
def getGPSInfo():
    with open('./../sim808Config.json','r') as file:
        data = json.load(file)
        return data             
