import asyncio
import json
import websockets
from getData import SIM_Manager 

class Controller:
    
    def __init__(self):
        self.manager = SIM_Manager()

    async def send_gps_data_to_server(self, lat, lon, res):
        async with websockets.connect('ws://localhost:8080') as websocket:
            data = {'latitude': lat, 'longitude': lon, 'nameEN': res[1], 'nameFR': res[0]}
            await websocket.send(json.dumps(data))
            print(f'Sent GPS data to server: {data}')
            response = await websocket.recv()
            print(f'Received response from server: {response}')
    async def main(self):
        if not self.manager.initialize_serial():
            return

        lat, lon = self.manager.get_gps_position()
        if lat and lon:
            print(f'Latitude: {lat}, Longitude: {lon}')
            #res = track((lat, lon))
           # await self.send_gps_data_to_server(lat, lon, res)
        else:
            print('Failed to retrieve GPS position')

        self.manager.close()

if __name__ == 'main':
    controller = Controller()
    asyncio.run(controller.main())
