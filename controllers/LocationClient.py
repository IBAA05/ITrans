import asyncio
import json
import websockets
from datetime import datetime
from location.managers.PositionManager import PositionManager 
from location.managers.LocationManager import LocationManager

from  daos.ConfigDao import ConfigDao
from  daos.RideDao import RideDao

class LocationClient:

    def __init__(self):
        self.location_manager = LocationManager()
        self.position_manager = PositionManager()

    async def main(self):
        
        configDao = ConfigDao()
        wsServerIp = configDao.get_bykey("wsServerIp")
        wsServerPort =  configDao.get_bykey("wsServerPort")

        uri = 'ws://' + str(wsServerIp) + ":" + str(wsServerPort) + "/ws"
        
        async with websockets.connect(uri) as ws:
            
            track_task = asyncio.create_task(self.track_location(ws))
            listen_task = asyncio.create_task(self.listen_for_messages(ws))
        
        #     # Wait for both tasks to complete
            await asyncio.gather(listen_task, track_task)     


    async def listen_for_messages(self, ws):
        
        try:
            while True:
                response = await ws.recv()
                self.filter_response(response)
                response_data = json.loads(response)  # Represent the direction and the line.
                self.handle_message (response_data)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    TRACKING_FREQUENCY = 5
    
    async def track_location(self, ws):
        
        try:
            while True:
              location = self.location_manager.get_location()
              (lat, lng) = location
              if RideDao().has_progressed():
                    if lat and lng :
                         position = self.position_manager.get_position(location)
                         (position_type, position_name) = position
                         if( position_type != self.position_manager.POSITON_TYPE_UNKNOWN) :
                             json_message = prepare_message(location, position)
                             ws.send(json_message) 
                            #TODO: LogDao.insert(json_message)

              await asyncio.sleep(self.TRACKING_FREQUENCY)  # Adjust the sleep duration as needed
        
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}") 
    

    MESSAGE_TYPE = "driving"
    DRIVING_TYPE_START = "start" 
    DRIVING_TYPE_CALIBRATE = "calibrate" 
    DRIVING_TYPE_FINISH = "finish" 

    def handle_message (self, message) :
        if (message['driving'] == self.MESSAGE_TYPE) :
            self.handle_driving_message(message)
        
    def handle_driving_message(self, message):
         print(message) 
    
         content = message['content']
         if(content['driving_type'] == self.DRIVING_TYPE_START):
            self.hanlde_driving_start_message(content)
            
         elif(content['driving_type'] == self.DRIVING_TYPE_CALIBRATE):
            self.hanlde_driving_calibrate_message(content)
         elif(content['driving_type'] == self.DRIVING_TYPE_FINISH):
            self.hanlde_driving_finish_message(content)
         else : 
            pass
            
    def hanlde_driving_start_message(self, content) : 
        #TODO: check line if exists locally
        #TODO: load from ms server and store in local database
        #TODO: finish any progressed ride
        #TODO: create a new progressed ride
        pass 

    def hanlde_driving_calibrate_message(self, content) : 
        #TODO: CalibrationLogDao.insert(location, position)
        pass

    def hanlde_driving_finish_message(self, content) :
        #TODO: finish any progressed ride
        pass
  

def prepare_message(location, position) : 
    
    (lat, lng) = location = location 
    (position_type, position_name) = position
    

    message = {
        "token" : ConfigDao.get_bykey("token"), 
        "type" : "location" , 
        "timestamp" : str(datetime.now()),
        "content " : {
            "location" : {"lat" : lat, "lng": lng} ,
            "position": { "type": position_type, "name": position_name }
        }
    }

    return message


locationClient = LocationClient()
asyncio.run(locationClient.main())