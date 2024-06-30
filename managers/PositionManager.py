import math
from datetime import datetime
from daos.InterstationDao import InterstationDao
from daos.StationDao import StationDao
from daos.RideDao import RideDao
from daos.ConfigDao import ConfigDao

class PositionManager:

    def __init__(self):
        pass

    def distance_between_locations(self, location1, location2):

        lat1, lng1 = location1
        lat2, lng2 = location2

        R = 6371  # Rayon de la Terre en kilomètres  
        dist_lat = math.radians(lat2 - lat1)
        dist_lng = math.radians(lng2 - lng1)
        a = math.sin(dist_lat / 2) * math.sin(dist_lat / 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dist_lng / 2) * math.sin(dist_lng / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return abs(round(R * c * 1000))  # Distance en mètres        

    POSITON_TYPE_STATION = "station"
    POSITON_TYPE_INTERSTATION = "interstation"
    POSITON_TYPE_UNKNOWN = "unknown"
    STATION_BORDER = ConfigDao().get_bykey("stationBorder")
    INTERSTATION_BORDER  = ConfigDao().get_bykey("interstationBorder")
    
    
    def calculate_position(self, location, stations, interstations):

        station = self.find_station(location, stations)
        if (station):
            return (self.POSITON_TYPE_STATION, station)

        interstation = self.find_interstation(location, interstations)
        if (interstation):
            return (self.POSITON_TYPE_INTERSTATION, interstation)
        return (self.POSITON_TYPE_UNKNOWN, None)

    def find_station(self, location, stations):

        for station in stations:
            lat, lng = station[4], station[5]
            station_location = (lat, lng)
            distance = self.distance_between_locations(location, station_location)
            print(distance)

            if (distance <= self.STATION_BORDER):
                return station  # we find a station

        return None  # in case we dont found .

    def find_interstation(self, location, interstations):

        for interstation in interstations:
            lat, lng = (interstation[1], interstation[2])
            interstation_location = (lat, lng)
            distance = self.distance_between_locations(location, interstation_location)
            
            if (distance <= self.INTERSTATION_BORDER):
                return interstation  # we find an interstation
        return None

    DIRECTION_GOING = 'going'
    DIRECTION_RETURNING = 'returning'

    def get_position(self, location, direction):


        station_dao = StationDao()
        interstation_dao = InterstationDao()
        stations = station_dao.get_all_by_line()
        interstations = interstation_dao.get_all_by_line()

        if direction == self.DIRECTION_GOING:
            stations = station_dao.get_all_by_line("station_going")
            interstations = interstation_dao.get_all_by_line("interstation_going")
        elif direction == self.DIRECTION_RETURNING:
            stations = station_dao.get_all_by_line("station_returning")
            interstations = interstation_dao.get_all_by_line("interstation_returning")

        self.calculate_position(location, stations, interstations)
