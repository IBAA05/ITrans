import asyncio
import json
import websockets
from getData import SIM_Manager 
from track import track 
from config import SERVER_PORT
import asyncio
from track import direction


class Controller:

    def __init__(self):
        self.manager = SIM_Manager()

    async def send_gps_data_to_server(self, lat, lon, res):
         
        uri = 'ws://localhost:' + SERVER_PORT + "/ws"
        async with websockets.connect(uri) as websocket:
            message = track((lat,lon))
            # Run send_messages and listen_for_messages concurrently
            send_task = asyncio.create_task(self.send_messages(websocket,message))
            listen_task = asyncio.create_task(self.listen_for_messages(websocket))
        
        # Wait for both tasks to complete
        await asyncio.gather(send_task, listen_task)     
            
    async def listen_for_messages(self,websocket):
        
        try:
            while True:
                # Wait for a response from the server
                response = await websocket.recv()
                self.filter_response(response)
                response_data = json.loads(response) # represent the direction and the line .
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
     
    async def send_messages(self,websocket,message):
        
        try : 
            while True:
                json_message = json.dumps(message)
                
                if direction != None : # Dont send before we get the direction and line .
                    await websocket.send(json_message)
                
                print(f"Sent: {json_message}")
            
            # Wait for a short period before sending the next message
                await asyncio.sleep(5)  # Adjust the sleep duration as needed
        
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}") 
    
    def filter_response (self,response) : 
        
        if (response['type'] == 'driving' and response ['content']['driving_type'] == 'start') : 
            pass 
           # we modify the direction and the ligne . 
            
            
            
    async def main(self):
        if not self.manager.initialize_serial():
            return

        lat, lon = self.manager.get_gps_position()
        if lat and lon:
            print(f'Latitude: {lat}, Longitude: {lon}')
            #res = track((lat, lon))
            res = ["def","blad"]
            await self.send_gps_data_to_server(lat, lon,res)
        else:
            print('Failed to retrieve GPS position')

        self.manager.close()



Controller = Controller()
asyncio.run(Controller.main())