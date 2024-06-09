import serial
import time
import asyncio
import websockets
import json
from track import track 

def initialize_serial():
    try:
        # Set up serial communication (adjust /dev/serial0 or /dev/ttyAMA0 as needed)
        ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2)
        print("Serial port initialized successfully.")
        return ser
    except serial.SerialException as e:
        print(f"Error initializing serial port: {e}")
        return None

def send_at_command(ser, command):
    
    try:
        ser.write((command + '\r\n').encode())
        time.sleep(0.5)  # Delay to allow for response
        reply = []
        start_time = time.time()
        while (time.time() - start_time) < 2:  # Wait up to 2 seconds for the response
            line = ser.readline().decode().strip()
            if line:
                reply.append(line)
        if not reply:
            print("No data received from the module.")
        return reply
    except Exception as e:
        print(f"Error sending AT command: {e}")
        return []

def parse_gps_data(data):
    # The GPS data is in the format: +CGNSINF: 1,1,YYYYMMDDHHMMSS.000,lat,lon,...
    parts = data.split(',')
    if len(parts) >= 4:
        lat = parts[3]
        lon = parts[4]
        return lat, lon
    return None, None

async def send_gps_data_to_server(lat, lon,res):
    async with websockets.connect('ws://localhost:8080') as websocket:
        data = {'latitude': lat, 'longitude': lon,"nameEN" : res[1],"nameFR" : res[0]}
        await websocket.send(json.dumps(data))
        print(f'Sent GPS data to server: {data}')
        response = await websocket.recv()
        print(f'Received response from server: {response}')

def getPosition (ser) :
    send_at_command(ser, 'AT')
    send_at_command(ser, 'AT+CGNSPWR=1')
    send_at_command(ser, 'AT+CGNSINF')
    
    
async def main():
    ser = initialize_serial()
    if ser is None:
        return

    # Check basic AT command response
    response = send_at_command(ser, 'AT')
    print('AT Command Response:', response)
    if not any('OK' in line for line in response):
        print('Basic AT command failed. Check the module connection and power.')
        ser.close()
        return

    # Enable the GPS
    response = send_at_command(ser, 'AT+CGNSPWR=1')
    print('GPS Power Response:', response)

    # Allow some time for the GPS to power up
    time.sleep(2)

    # Get GPS information
    response = send_at_command(ser, 'AT+CGNSINF')
    print('GPS Info Response:', response)

    # Parse the response to get latitude and longitude
    for line in response:
        if '+CGNSINF' in line:
            lat, lon = parse_gps_data(line)
            if lat and lon:
                print(f'Latitude: {lat}, Longitude: {lon}')
                res = track((lat,lon))  
                await send_gps_data_to_server(lat, lon,res)
            else:
                print('Failed to parse GPS data')
    
    ser.close()

if __name__ == '__main__':
    asyncio.run(main())